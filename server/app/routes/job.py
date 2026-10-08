import math
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, contains_eager, joinedload

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models import Company, Job, JobStatus, JobType, User, UserRole, WorkMode
from app.schemas.job import JobCreate, JobListResponse, JobResponse, JobUpdate

router = APIRouter()


def _get_owned_job(job_id: int, user: User, db: Session) -> Job:
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if not user.company or job.company_id != user.company.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this job")
    return job

# ---------- Public: browse + search ----------
@router.get("", response_model=JobListResponse)
def list_jobs(
    keyword: str | None = Query(None, description="Matches title, description or company name"),
    location: str | None = None,
    job_type: JobType | None = None,
    work_mode: WorkMode | None = None,
    min_salary: float | None = Query(None, ge=0, description="Jobs whose max salary is at least this"),
    max_experience: int | None = Query(None, ge=0, description="Jobs needing at most this many years"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = (
        db.query(Job)
        .join(Company, Job.company_id == Company.id)
        .options(contains_eager(Job.company))
        .filter(Job.status == JobStatus.open)
    )

    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(
            Job.title.ilike(like),
            Job.description.ilike(like),
            Company.name.ilike(like),
        ))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if work_mode:
        query = query.filter(Job.work_mode == work_mode)
    if min_salary is not None:
        query = query.filter(Job.salary_max >= min_salary)
    if max_experience is not None:
        query = query.filter(Job.experience_required <= max_experience)

    total = query.order_by(None).count()
    items = (
        query.order_by(Job.created_at.desc(), Job.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size),
    }


@router.get("/mine", response_model=list[JobResponse])
def list_my_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.employer)),
):
    if not current_user.company:
        return []
    return (
        db.query(Job)
        .options(joinedload(Job.company))
        .filter(Job.company_id == current_user.company.id)
        .order_by(Job.created_at.desc(), Job.id.desc())
        .all()
    )

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.post("/create", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.employer)),
):
    if not current_user.company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Create your company profile before posting jobs")

    job = Job(company_id=current_user.company.id, **data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.put("/update/{job_id}/", response_model=JobResponse)
def update_job(
    job_id: int,
    data: JobUpdate,
    current_user: User = Depends(require_role(UserRole.employer)),
    db: Session = Depends(get_db)
):
    job = _get_owned_job(job_id, current_user, db)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    if job.salary_min is not None and job.salary_max is not None \
        and job.salary_min > job.salary_max:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="salary_min can not be greater than salary_max")

    db.commit()
    db.refresh(job)
    return job

@router.delete("/delete{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.employer))):

    job = _get_owned_job(job_id, current_user, db)
    db.delete(job)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

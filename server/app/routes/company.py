from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models import Company, User, UserRole
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter()


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.employer)),
):
    print("Current user:", current_user)  # Debugging line to check the current user
    if current_user.company:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You already have a company profile")

    company = Company(owner_id=current_user.id, **data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


# NOTE: "/me" must be declared BEFORE "/{company_id}", otherwise FastAPI
# would try to read the word "me" as a company id.
@router.get("/me", response_model=CompanyResponse)
def get_my_company(current_user: User = Depends(require_role(UserRole.employer))):
    if not current_user.company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You have not created a company profile yet")
    return current_user.company


@router.put("/me", response_model=CompanyResponse)
def update_my_company(
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.employer)),
):
    company = current_user.company
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You have not created a company profile yet")

    # exclude_unset: only change the fields the client actually sent
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company
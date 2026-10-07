from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.schemas.enums import JobStatus, JobType, WorkMode
from app.schemas.company import CompanyResponse
from app.schemas.company import CompanyResponse

class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    location: str | None = Field(default=None, max_length=100)
    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)
    experience_required: int = Field(default=0, ge=0)  # years
    job_type: JobType
    work_mode: WorkMode

    @model_validator(mode="after")
    def check_salary_range(self):
        if self.salary_min is not None and self.salary_max is not None \
                and self.salary_min > self.salary_max:
            raise ValueError("salary_min cannot be greater than salary_max")
        return self


class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=10)
    location: str | None = Field(default=None, max_length=100)
    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)
    experience_required: int | None = Field(default=None, ge=0)
    job_type: JobType | None = None
    work_mode: WorkMode | None = None
    status: JobStatus | None = None  # lets an employer close/reopen a job


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    location: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    experience_required: int
    job_type: JobType
    work_mode: WorkMode
    status: JobStatus
    created_at: datetime | None = None
    company: CompanyResponse


class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
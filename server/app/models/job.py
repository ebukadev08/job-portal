import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class JobType(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    contract = "contract"


class WorkMode(str, enum.Enum):
    remote = "remote"
    on_site = "on_site"


class JobStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"),
                        nullable=False)
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=False)
    location = Column(String(100), index=True)
    salary_min = Column(Numeric(12, 2))
    salary_max = Column(Numeric(12, 2))
    experience_required = Column(Integer, default=0)  # years
    job_type = Column(Enum(JobType), nullable=False, index=True)
    work_mode = Column(Enum(WorkMode), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.open, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job",
                                cascade="all, delete-orphan")
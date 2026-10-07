import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    under_review = "under_review"
    interview_scheduled = "interview_scheduled"
    selected = "selected"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"
    # One application per seeker per job (prevents duplicate applications)
    __table_args__ = (UniqueConstraint("job_id", "seeker_id", name="uq_job_seeker"),)

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"),
                    nullable=False, index=True)
    seeker_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                       nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="SET NULL"))
    cover_letter = Column(Text)
    status = Column(Enum(ApplicationStatus),
                    default=ApplicationStatus.applied, nullable=False)
    applied_at = Column(DateTime, server_default=func.now())

    job = relationship("Job", back_populates="applications")
    seeker = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
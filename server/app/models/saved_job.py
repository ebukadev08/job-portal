from sqlalchemy import Column, DateTime, ForeignKey, Integer, PrimaryKeyConstraint, func

from app.core.database import Base


class SavedJob(Base):
    __tablename__ = "saved_jobs"
    __table_args__ = (PrimaryKeyConstraint("user_id", "job_id"),)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    saved_at = Column(DateTime, server_default=func.now())
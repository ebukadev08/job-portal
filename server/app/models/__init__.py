"""
Importing every model here means that anywhere you do
    from app.models import Base
and call Base.metadata.create_all(engine),
SQLAlchemy knows about ALL the tables, not just the ones imported directly.
"""

from app.core.database import Base

from app.models.user import User, UserRole
from app.models.seeker_profile import SeekerProfile
from app.models.company import Company
from app.models.job import Job, JobType, WorkMode, JobStatus
from app.models.resume import Resume
from app.models.application import Application, ApplicationStatus
from app.models.saved_job import SavedJob
from app.models.notification import Notification

__all__ = [
    "Base",
    "User", "UserRole",
    "SeekerProfile",
    "Company",
    "Job", "JobType", "WorkMode", "JobStatus",
    "Resume",
    "Application", "ApplicationStatus",
    "SavedJob",
    "Notification",
]
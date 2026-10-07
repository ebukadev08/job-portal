import enum


class UserRole(str, enum.Enum):
    job_seeker = "job_seeker"
    employer = "employer"


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


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    under_review = "under_review"
    interview_scheduled = "interview_scheduled"
    selected = "selected"
    rejected = "rejected"
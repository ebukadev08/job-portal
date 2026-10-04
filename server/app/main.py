"""
FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload

Then visit http://127.0.0.1:8000/docs for the auto-generated Swagger UI -
this is the "free interactive API docs" FastAPI gives you.
"""

from fastapi import FastAPI
from app.core.database import engine
from app.models import Base
from app.routes import auth
# from app.routes import companies
# from app.routes import jobs
# from app.routes import resumes
# from app.routes import applications
# from app.routes import saved_jobs
# from app.routes import notifications
# from app.routes import employer


# Creates all tables in MySQL if they don't already exist.
# Safe to run every startup - it won't touch tables that already exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Portal API",
    description="Backend API for a job portal - job seekers, employers, job listings, resumes, applications and tracking.",
    version="0.1.0",
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
# app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
# app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
# app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
# app.include_router(applications.router, prefix="/api", tags=["Applications"])
# app.include_router(saved_jobs.router, prefix="/api", tags=["Saved Jobs"])
# app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
# app.include_router(employer.router, prefix="/api/employer", tags=["Employer Dashboard"])


@app.get("/")
def root():
    return {"message": "Job Portal API is running"}
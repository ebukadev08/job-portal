from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class SeekerProfile(Base):
    __tablename__ = "seeker_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                     unique=True, nullable=False)
    phone = Column(String(30))
    location = Column(String(100))
    headline = Column(String(150))
    skills = Column(Text)
    experience_years = Column(Integer, default=0)

    user = relationship("User", back_populates="profile")
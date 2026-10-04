from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                      unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    website = Column(String(255))
    location = Column(String(100))
    logo_url = Column(String(500))

    owner = relationship("User", back_populates="company")
    jobs = relationship("Job", back_populates="company",
                        cascade="all, delete-orphan")
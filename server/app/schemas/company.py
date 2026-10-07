from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    website: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=100)
    logo_url: str | None = Field(default=None, max_length=500)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    website: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=100)
    logo_url: str | None = Field(default=None, max_length=500)


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    website: str | None = None
    location: str | None = None
    logo_url: str | None = None
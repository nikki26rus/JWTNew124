from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class NewsAdd(BaseModel):
    title: str
    content: str
    image: Optional[str] = None

    class Config:
        from_attributes = True

class News(BaseModel):
    id: int
    title: str
    content: str
    image: Optional[str]

    class Config:
        from_attributes = True


class Study(BaseModel):
    ID: str
    LastUpdate: str
    MedicalCardNumber: Optional[str]
    PatientBirthDate: Optional[str]
    PatientName: Optional[str]
    StudyInstanceUID: Optional[str]

class Series(BaseModel):
    series_id: str
    instance_number: Optional[int]
    series_description: Optional[str]
    number_of_instances: Optional[int]
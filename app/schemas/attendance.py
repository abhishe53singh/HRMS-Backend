from pydantic import BaseModel, validator
from datetime import date
from typing import Optional


class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    status: str  # "Present" or "Absent"

    @validator('status')
    def validate_status(cls, v):
        if v not in ["Present", "Absent"]:
            raise ValueError('Status must be either "Present" or "Absent"')
        return v


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: Optional[str] = None
    
    class Config:
        from_attributes = True


class AttendanceUpdate(BaseModel):
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None and v not in ["Present", "Absent"]:
            raise ValueError('Status must be either "Present" or "Absent"')
        return v

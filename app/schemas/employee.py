from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional


class EmployeeBase(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str

    @validator('employee_id')
    def validate_employee_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Employee ID is required')
        return v.strip()
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Full name is required')
        return v.strip()
    
    @validator('department')
    def validate_department(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Department is required')
        return v.strip()


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None

    @validator('full_name')
    def validate_full_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Full name cannot be empty')
        return v.strip() if v else v
    
    @validator('department')
    def validate_department(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Department cannot be empty')
        return v.strip() if v else v

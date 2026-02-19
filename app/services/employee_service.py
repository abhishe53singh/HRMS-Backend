import re
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def validate_email_format(self, email: str) -> bool:
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def get_all_employees(self) -> List[Employee]:
        """Get all employees from the database"""
        return self.db.query(Employee).all()

    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        """Get employee by employee_id"""
        return self.db.query(Employee).filter(Employee.employee_id == employee_id).first()

    def get_employee_by_email(self, email: str) -> Optional[Employee]:
        """Get employee by email"""
        return self.db.query(Employee).filter(Employee.email == email).first()

    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee"""
        # Check for duplicate employee_id
        existing_employee = self.get_employee_by_id(employee_data.employee_id)
        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee ID already exists"
            )
        
        # Check for duplicate email
        existing_email = self.get_employee_by_email(employee_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Validate email format
        if not self.validate_email_format(employee_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Create new employee
        db_employee = Employee(**employee_data.dict())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        
        return db_employee

    def update_employee(self, employee_id: str, employee_data: EmployeeUpdate) -> Employee:
        """Update an existing employee"""
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        # Check for email update conflicts
        if employee_data.email and employee_data.email != employee.email:
            existing_email = self.get_employee_by_email(employee_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            
            # Validate email format
            if not self.validate_email_format(employee_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email format"
                )
        
        # Update employee fields
        update_data = employee_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(employee, field, value)
        
        self.db.commit()
        self.db.refresh(employee)
        
        return employee

    def delete_employee(self, employee_id: str) -> bool:
        """Delete an employee"""
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        self.db.delete(employee)
        self.db.commit()
        
        return True

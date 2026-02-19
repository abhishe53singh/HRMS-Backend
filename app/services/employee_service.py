import re
from datetime import datetime
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.database.config import get_employee_collection


class EmployeeService:
    def __init__(self):
        try:
            self.collection = get_employee_collection()
            # Test the connection
            self.collection.database.command('ping')
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to MongoDB: {str(e)}"
            )

    def validate_email_format(self, email: str) -> bool:
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def get_all_employees(self) -> List[dict]:
        """Get all employees from the database"""
        employee_records = list(self.collection.find({}))
        
        # Convert MongoDB ObjectId to string and format dates
        employees = []
        for record in employee_records:
            record["id"] = str(record.pop("_id"))
            if isinstance(record.get("created_at"), datetime):
                record["created_at"] = record["created_at"]
            employees.append(record)
        
        return employees

    def get_employee_by_id(self, employee_id: str) -> Optional[dict]:
        """Get employee by employee_id"""
        record = self.collection.find_one({"employee_id": employee_id})
        if record:
            record["id"] = str(record.pop("_id"))
            return record
        return None

    def get_employee_by_email(self, email: str) -> Optional[dict]:
        """Get employee by email"""
        record = self.collection.find_one({"email": email})
        if record:
            record["id"] = str(record.pop("_id"))
            return record
        return None

    def create_employee(self, employee_data: EmployeeCreate) -> dict:
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
        
        # Convert to dict for MongoDB
        employee_dict = employee_data.dict()
        employee_dict["created_at"] = datetime.utcnow()
        
        # Insert into MongoDB
        result = self.collection.insert_one(employee_dict)
        employee_dict["id"] = str(result.inserted_id)
        employee_dict.pop("_id", None)
        
        return employee_dict

    def update_employee(self, employee_id: str, employee_data: EmployeeUpdate) -> dict:
        """Update an existing employee"""
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        # Check for email update conflicts
        if employee_data.email and employee_data.email != employee["email"]:
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
        if update_data:
            from bson.objectid import ObjectId
            self.collection.update_one(
                {"_id": ObjectId(employee["id"])},
                {"$set": update_data}
            )
        
        # Return updated record
        updated_employee = self.get_employee_by_id(employee_id)
        return updated_employee

    def delete_employee(self, employee_id: str) -> bool:
        """Delete an employee"""
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        from bson.objectid import ObjectId
        self.collection.delete_one({"_id": ObjectId(employee["id"])})
        
        return True

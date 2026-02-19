from datetime import datetime
from typing import Optional


class Employee:
    def __init__(self, employee_id: str, full_name: str, email: str, department: str, 
                 id: Optional[str] = None, created_at: Optional[datetime] = None):
        self.id = id
        self.employee_id = employee_id
        self.full_name = full_name
        self.email = email
        self.department = department
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert Employee object to dictionary for MongoDB storage"""
        return {
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Employee object from MongoDB document"""
        return cls(
            employee_id=data["employee_id"],
            full_name=data["full_name"],
            email=data["email"],
            department=data["department"],
            id=str(data["_id"]) if "_id" in data else data.get("id"),
            created_at=data.get("created_at")
        )
    
    def __repr__(self):
        return f"<Employee(id={self.id}, employee_id='{self.employee_id}', name='{self.full_name}')>"

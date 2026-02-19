from datetime import datetime, date
from typing import List, Optional
from fastapi import HTTPException, status

from app.database.config import get_mongo_collection
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


class AttendanceService:
    def __init__(self):
        try:
            self.collection = get_mongo_collection()
            # Test the connection
            self.collection.database.command('ping')
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to MongoDB: {str(e)}"
            )

    def get_all_attendance(self) -> List[dict]:
        """Get all attendance records"""
        attendance_records = list(self.collection.find({}))
        
        # Convert MongoDB ObjectId to string and format dates
        attendances = []
        for record in attendance_records:
            record["id"] = str(record.pop("_id"))
            if isinstance(record.get("date"), str):
                record["date"] = datetime.fromisoformat(record["date"]).date()
            attendances.append(record)
        
        return attendances

    def get_attendance_by_employee(self, employee_id: str) -> List[dict]:
        """Get attendance records for a specific employee"""
        attendance_records = list(self.collection.find({"employee_id": employee_id}))
        
        # Convert MongoDB ObjectId to string and format dates
        attendances = []
        for record in attendance_records:
            record["id"] = str(record.pop("_id"))
            if isinstance(record.get("date"), str):
                record["date"] = datetime.fromisoformat(record["date"]).date()
            attendances.append(record)
        
        return attendances

    def mark_attendance(self, attendance_data: AttendanceCreate) -> dict:
        """Mark attendance for an employee"""
        # Check if attendance already exists for this employee and date
        existing_attendance = self.collection.find_one({
            "employee_id": attendance_data.employee_id,
            "date": attendance_data.date.isoformat()
        })
        
        if existing_attendance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance already marked for this employee on this date"
            )
        
        # Convert to dict for MongoDB
        attendance_dict = attendance_data.dict()
        attendance_dict["date"] = attendance_data.date.isoformat()
        
        # Insert into MongoDB
        result = self.collection.insert_one(attendance_dict)
        attendance_dict["id"] = str(result.inserted_id)
        
        return attendance_dict

    def update_attendance(self, attendance_id: str, attendance_data: AttendanceUpdate) -> dict:
        """Update attendance record"""
        from bson.objectid import ObjectId
        
        try:
            object_id = ObjectId(attendance_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid attendance ID"
            )
        
        # Check if attendance exists
        existing_attendance = self.collection.find_one({"_id": object_id})
        if not existing_attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance record not found"
            )
        
        # Update attendance
        update_data = attendance_data.dict(exclude_unset=True)
        if update_data:
            self.collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
        
        # Return updated record
        updated_attendance = self.collection.find_one({"_id": object_id})
        updated_attendance["id"] = str(updated_attendance.pop("_id"))
        if isinstance(updated_attendance.get("date"), str):
            updated_attendance["date"] = datetime.fromisoformat(updated_attendance["date"]).date()
        
        return updated_attendance

    def delete_attendance(self, attendance_id: str) -> bool:
        """Delete attendance record"""
        from bson.objectid import ObjectId
        
        try:
            object_id = ObjectId(attendance_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid attendance ID"
            )
        
        # Check if attendance exists
        existing_attendance = self.collection.find_one({"_id": object_id})
        if not existing_attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance record not found"
            )
        
        # Delete attendance
        self.collection.delete_one({"_id": object_id})
        
        return True

    def delete_attendance_by_employee(self, employee_id: str) -> int:
        """Delete all attendance records for an employee"""
        result = self.collection.delete_many({"employee_id": employee_id})
        return result.deleted_count

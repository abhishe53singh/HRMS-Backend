from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.services.attendance_service import AttendanceService
from app.schemas.attendance import Attendance, AttendanceCreate, AttendanceUpdate

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"]
)


def get_attendance_service() -> AttendanceService:
    """Dependency to get attendance service instance"""
    return AttendanceService()


@router.get("/", response_model=List[Attendance])
def get_all_attendance(service: AttendanceService = Depends(get_attendance_service)):
    """
    Get all attendance records
    
    Returns a list of all attendance records in the system.
    """
    try:
        attendance_records = service.get_all_attendance()
        return attendance_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance records: {str(e)}"
        )


@router.get("/{employee_id}", response_model=List[Attendance])
def get_employee_attendance(
    employee_id: str,
    service: AttendanceService = Depends(get_attendance_service)
):
    """
    Get attendance records for a specific employee
    
    - **employee_id**: The unique identifier of the employee
    """
    try:
        attendance_records = service.get_attendance_by_employee(employee_id)
        return attendance_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance records: {str(e)}"
        )


@router.post("/", response_model=Attendance, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    attendance_data: AttendanceCreate,
    service: AttendanceService = Depends(get_attendance_service)
):
    """
    Mark attendance for an employee
    
    - **employee_id**: The unique identifier of the employee
    - **date**: The date for which attendance is being marked
    - **status**: Attendance status ("Present" or "Absent")
    """
    try:
        attendance = service.mark_attendance(attendance_data)
        return attendance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark attendance: {str(e)}"
        )


@router.put("/{attendance_id}", response_model=Attendance)
def update_attendance(
    attendance_id: str,
    attendance_data: AttendanceUpdate,
    service: AttendanceService = Depends(get_attendance_service)
):
    """
    Update an existing attendance record
    
    - **attendance_id**: The unique identifier of the attendance record
    - **status**: Updated attendance status ("Present" or "Absent")
    """
    try:
        attendance = service.update_attendance(attendance_id, attendance_data)
        return attendance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attendance: {str(e)}"
        )


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: str,
    service: AttendanceService = Depends(get_attendance_service)
):
    """
    Delete an attendance record
    
    - **attendance_id**: The unique identifier of the attendance record to delete
    """
    try:
        service.delete_attendance(attendance_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attendance: {str(e)}"
        )

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.employee_service import EmployeeService
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)


def get_employee_service() -> EmployeeService:
    """Dependency to get employee service instance"""
    return EmployeeService()


@router.get("/", response_model=List[Employee])
def get_employees(service: EmployeeService = Depends(get_employee_service)):
    """
    Get all employees
    
    Returns a list of all employees in the system.
    """
    try:
        employees = service.get_all_employees()
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve employees: {str(e)}"
        )


@router.get("/{employee_id}", response_model=Employee)
def get_employee(
    employee_id: str,
    service: EmployeeService = Depends(get_employee_service)
):
    """
    Get a specific employee by ID
    
    - **employee_id**: The unique identifier of the employee
    """
    try:
        employee = service.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve employee: {str(e)}"
        )


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service)
):
    """
    Create a new employee
    
    - **employee_id**: Unique employee identifier
    - **full_name**: Full name of the employee
    - **email**: Email address (must be unique and valid)
    - **department**: Department name
    """
    try:
        employee = service.create_employee(employee_data)
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create employee: {str(e)}"
        )


@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service)
):
    """
    Update an existing employee
    
    - **employee_id**: The unique identifier of the employee to update
    - **full_name**: Updated full name (optional)
    - **email**: Updated email address (optional, must be unique and valid)
    - **department**: Updated department name (optional)
    """
    try:
        employee = service.update_employee(employee_id, employee_data)
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update employee: {str(e)}"
        )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: str,
    service: EmployeeService = Depends(get_employee_service)
):
    """
    Delete an employee
    
    - **employee_id**: The unique identifier of the employee to delete
    
    Note: This will also delete all attendance records for this employee.
    """
    try:
        # First, delete all attendance records for this employee
        from app.services.attendance_service import AttendanceService
        attendance_service = AttendanceService()
        attendance_service.delete_attendance_by_employee(employee_id)
        
        # Then delete the employee
        service.delete_employee(employee_id)
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete employee: {str(e)}"
        )

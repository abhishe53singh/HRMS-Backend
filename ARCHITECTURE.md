# HRMS Lite Backend Architecture

## Overview

The HRMS Lite backend follows a clean, modular architecture with proper separation of concerns. The application is structured using FastAPI with function-based routes, service layer pattern, and clear separation between data access, business logic, and API endpoints.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py                 # App initialization
│   ├── main.py                     # FastAPI application setup
│   ├── database/
│   │   ├── __init__.py            # Database exports
│   │   └── config.py              # Database configuration and connections
│   ├── models/
│   │   ├── __init__.py            # Model exports
│   │   └── employee.py            # SQLAlchemy Employee model
│   ├── schemas/
│   │   ├── __init__.py            # Schema exports
│   │   ├── employee.py            # Employee Pydantic schemas
│   │   └── attendance.py          # Attendance Pydantic schemas
│   ├── services/
│   │   ├── __init__.py            # Service exports
│   │   ├── employee_service.py    # Employee business logic
│   │   └── attendance_service.py  # Attendance business logic
│   └── routers/
│       ├── __init__.py            # Router exports
│       ├── employees.py           # Employee API endpoints
│       └── attendance.py          # Attendance API endpoints
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
└── ARCHITECTURE.md               # This file
```

## Architecture Layers

### 1. API Layer (Routers)
**Location**: `app/routers/`

- **Purpose**: Handle HTTP requests and responses
- **Components**:
  - `employees.py`: Employee-related endpoints
  - `attendance.py`: Attendance-related endpoints
- **Responsibilities**:
  - Request validation
  - Response formatting
  - HTTP status codes
  - Error handling at API level

### 2. Service Layer
**Location**: `app/services/`

- **Purpose**: Business logic and data orchestration
- **Components**:
  - `employee_service.py`: Employee business operations
  - `attendance_service.py`: Attendance business operations
- **Responsibilities**:
  - Business rule enforcement
  - Data validation
  - Transaction management
  - Cross-service coordination

### 3. Data Access Layer
**Location**: `app/models/` and `app/database/`

- **Purpose**: Database operations and data modeling
- **Components**:
  - `models/employee.py`: SQLAlchemy models
  - `database/config.py`: Database connections and configuration
- **Responsibilities**:
  - Database schema definition
  - Connection management
  - Query operations

### 4. Schema Layer
**Location**: `app/schemas/`

- **Purpose**: Data validation and serialization
- **Components**:
  - `employee.py`: Employee Pydantic schemas
  - `attendance.py`: Attendance Pydantic schemas
- **Responsibilities**:
  - Request/response validation
  - Data serialization/deserialization
  - Type safety

## Key Design Patterns

### 1. Dependency Injection
FastAPI's dependency injection is used throughout the application:

```python
# Service injection
def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)

# Database injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Service Layer Pattern
Business logic is encapsulated in service classes:

```python
class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        # Business logic here
        pass
```

### 3. Repository Pattern (Implicit)
Service classes act as repositories, abstracting database operations.

### 4. Schema Validation
Pydantic schemas ensure data integrity:

```python
class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str
    
    @validator('employee_id')
    def validate_employee_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Employee ID is required')
        return v.strip()
```

## Database Architecture

### Hybrid Database Approach
The application uses a hybrid database approach:

1. **SQL (SQLite)**: For structured employee data
   - ACID compliance
   - Complex queries
   - Relational integrity

2. **MongoDB**: For flexible attendance data
   - Schema flexibility
   - Fast writes
   - Scalability

### Database Connections

```python
# SQL Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./hrms.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MongoDB
MONGODB_URL = "mongodb://localhost:27017"
MONGODB_DB_NAME = "hrms_attendance"
mongo_client = MongoClient(MONGODB_URL)
mongo_db = mongo_client[MONGODB_DB_NAME]
```

## API Design

### RESTful Endpoints

#### Employee Management
- `GET /employees/` - List all employees
- `GET /employees/{employee_id}` - Get specific employee
- `POST /employees/` - Create new employee
- `PUT /employees/{employee_id}` - Update employee
- `DELETE /employees/{employee_id}` - Delete employee

#### Attendance Management
- `GET /attendance/` - List all attendance records
- `GET /attendance/{employee_id}` - Get employee attendance
- `POST /attendance/` - Mark attendance
- `PUT /attendance/{attendance_id}` - Update attendance
- `DELETE /attendance/{attendance_id}` - Delete attendance

### Error Handling

Comprehensive error handling at multiple levels:

1. **Service Layer**: Business logic validation
2. **API Layer**: HTTP error responses
3. **Global**: Exception handling middleware

```python
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
```

## Security Considerations

### Input Validation
- Pydantic schemas for request validation
- Custom validators for business rules
- SQL injection prevention through SQLAlchemy

### Data Integrity
- Unique constraints on employee_id and email
- Foreign key relationships
- Transaction management

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Strategy

### Unit Testing
- Test service layer logic
- Test schema validation
- Mock database operations

### Integration Testing
- Test API endpoints
- Test database operations
- Test service integration

### API Documentation
- Auto-generated OpenAPI/Swagger docs at `/docs`
- ReDoc documentation at `/redoc`
- Comprehensive endpoint descriptions

## Performance Optimizations

### Database Optimization
- Proper indexing on unique fields
- Efficient query patterns
- Connection pooling

### Caching Strategy
- Future: Redis for session management
- Future: Application-level caching

### Async Operations
- FastAPI's async support
- Non-blocking I/O operations

## Deployment Considerations

### Environment Configuration
- Environment variables for database URLs
- Configuration management
- Secret management

### Scalability
- Horizontal scaling support
- Load balancing ready
- Database scaling considerations

### Monitoring
- Health check endpoint at `/health`
- Structured logging
- Performance metrics

## Future Enhancements

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- Multi-tenant support

### Advanced Features
- Leave management
- Payroll integration
- Reporting and analytics
- Email notifications

### Performance Improvements
- Database query optimization
- Caching layer
- Background job processing

## Development Guidelines

### Code Style
- Follow PEP 8
- Type hints throughout
- Comprehensive docstrings
- Meaningful variable names

### Git Workflow
- Feature branches
- Pull request reviews
- Automated testing

### Documentation
- API documentation
- Code comments
- Architecture decisions

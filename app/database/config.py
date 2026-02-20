from pymongo import MongoClient
import os

# MongoDB Configuration
# MongoDB Atlas connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://abhishek53singh1_db_user:uCiQslGUybFD8QDM@db.pjem0wi.mongodb.net/hrms_attendance?retryWrites=true&w=majority")

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "hrms_attendance")

# Initialize MongoDB client with connection timeout and retry settings
try:
    mongo_client = MongoClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=10000,  # 10 second timeout
        connectTimeoutMS=10000,  # 10 second connection timeout
        socketTimeoutMS=10000,  # 10 second socket timeout
        retryWrites=True,
        w='majority'
    )
    # Test connection
    mongo_db = mongo_client[MONGODB_DB_NAME]
    mongo_db.command('ping')  # Test with the actual database
    print("✅ MongoDB connection successful")
except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)}")
    mongo_client = None
    mongo_db = None

attendance_collection = mongo_db["attendance"] if mongo_db is not None else None
employee_collection = mongo_db["employees"] if mongo_db is not None else None

def get_mongo_collection():
    if attendance_collection is None:
        raise Exception("MongoDB not connected - check MONGODB_URL environment variable")
    return attendance_collection

def get_employee_collection():
    if employee_collection is None:
        raise Exception("MongoDB not connected - check MONGODB_URL environment variable")
    return employee_collection

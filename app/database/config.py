from pymongo import MongoClient
import os

# MongoDB Configuration
# MongoDB Atlas connection
MONGODB_URL = "mongodb+srv://abhishek53singh1_db_user:uCiQslGUybFD8QDM@db.pjem0wi.mongodb.net/hrms_attendance?retryWrites=true&w=majority"

MONGODB_DB_NAME = "hrms_attendance"

# Initialize MongoDB client with connection timeout and retry settings
mongo_client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=5000,  # 5 second timeout
    connectTimeoutMS=10000,  # 10 second connection timeout
    socketTimeoutMS=10000,  # 10 second socket timeout
    retryWrites=True,
    w='majority'
)
mongo_db = mongo_client[MONGODB_DB_NAME]
attendance_collection = mongo_db["attendance"]
employee_collection = mongo_db["employees"]

def get_mongo_collection():
    return attendance_collection

def get_employee_collection():
    return employee_collection

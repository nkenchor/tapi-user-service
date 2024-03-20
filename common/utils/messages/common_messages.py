# messages.py

class ErrorMessage:
    DATABASE_CONNECTION_ERROR = "Error connecting to the database"
    USER_NOT_FOUND = "User not found"
    # Add more error messages...

class DatabaseMessage:
    CONNECTION_SUCCESS = "Database connection established successfully"
    CONNECTION_TERMINATED = "Database connection terminated successfully"

class RedisMessage:
    CONNECTION_SUCCESS = "Redis connection established successfully"
    CONNECTION_TERMINATED = "Redis connection terminated successfully"
  
class VaultMessage:
    CONNECTION_SUCCESS = "Vault connection established successfully"
    CONNECTION_TERMINATED = "Vault connection terminated successfully"
  

class GeneralMessage:
    WELCOME_MESSAGE = "Welcome to our application"
    # Add more general messages...

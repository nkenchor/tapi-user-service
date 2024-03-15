from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    Address = os.getenv("ADDRESS", "localhost")
    Port = int(os.getenv("PORT", "8001"))
    Mode = os.getenv("MODE", "dev")
    Name = os.getenv("NAME", "tapi-user-service")
    Log_file = os.getenv("LOG_FILE", "tapi-user-service.log")
    Log_dir = os.getenv("LOG_DIR", "logs")
    Launch_url = os.getenv("LAUNCH_URL", "swagger")
    App_name = os.getenv("APP_NAME", "tapi-user-service")
    Db_Type = os.getenv("DB_TYPE", "mongodb")
    Db_url = os.getenv("DB_URL", "mongodb://localhost:27017/tapi")
    Db = os.getenv("DB", "tapi")
    Redis_host = os.getenv("REDIS_HOST", "localhost")
    Redis_port = os.getenv("REDIS_PORT", "6379")
    Vault_url = os.getenv("VAULT_URL", "http://localhost:8200")
    Vault_token = os.getenv("VAULT_TOKEN", "")
    Vault_path = os.getenv("VAULT_PATH", "")
    Vault_key = os.getenv("VAULT_KEY", "")
    Jwt_key = os.getenv("JWT_KEY", "default_key")
    Jwt_audience = os.getenv("JWT_AUDIENCE", "tapi")
    Jwt_issuer = os.getenv("JWT_ISSUER", "https://localhost:3003")
    Jwt_expiry = os.getenv("JWT_EXPIRY", "5")

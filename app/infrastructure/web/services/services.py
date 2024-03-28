
import sys
from app.infrastructure.persistence.database.setup.database_setup import Database
from app.infrastructure.system.configuration.configuration import Config
from app.infrastructure.messaging.redis.setup.redis_setup import Redis
from app.infrastructure.secrets.vault.setup.vault_setup import Vault
from app.infrastructure.secrets.vault.utils.helper.vault_helper import VaultHelper
from app.infrastructure.system.logger.utils.helper.logger_helper import log_event
import app.domain.shared.shared_messages as message
from app.application.application_services.tapi_user_application_service import UserApplicationService
from app.application.use_cases.use_case_interactor.tapi_user_interactor import UserUseCase
from app.infrastructure.messaging.publisher.tapi_user_event_publisher import RedisEventPublisher
from app.infrastructure.persistence.repository.tapi_user_repository import UserRepository
from app.infrastructure.web.controller.tapi_user_controller import UserController

async def initialize_database():
    database =  Database.connect()
    print(message.DatabaseMessage.CONNECTION_SUCCESS)
    log_event("INFO", message.DatabaseMessage.CONNECTION_SUCCESS)
    return database

async def initialize_redis():
    redis =  Redis.connect()
    print(message.RedisMessage.CONNECTION_SUCCESS)
    log_event("INFO", message.RedisMessage.CONNECTION_SUCCESS)
    return redis

async def initialize_vault():
    vault = Vault.connect()
    # Get secrets from Vault and set them in Config
    Config.Secret_key = VaultHelper.get_secret(Config.Vault_path, Config.Vault_key)
    print(message.VaultMessage.CONNECTION_SUCCESS)
    log_event("INFO", message.VaultMessage.CONNECTION_SUCCESS)
    return vault
async def initialize_services():
    try:
        # Assuming these are properly defined and return awaitables
        database = await initialize_database()
        redis = await initialize_redis()
        await initialize_vault()  # If this doesn't return anything, no need to assign it to a variable

        # Assuming the below constructors don't await, but the objects are used in async contexts later
        redis_event_publisher = RedisEventPublisher(redis)
        user_repository = UserRepository(database)
        user_use_case = UserUseCase(user_repository, redis_event_publisher)
        user_application_service = UserApplicationService(user_use_case)

        print(f"{Config.App_name} services are set up.")
        log_event("INFO", f"{Config.App_name} services are set up.")

        return user_application_service  # Ensure this is returned
    except Exception as e:
        print(f"Error during {Config.App_name} startup: {e}")
        log_event("ERROR", f"Error during {Config.App_name} startup: {e}")
        sys.exit(1)

async def initialize_controller(user_application_service):
    try:
        # Ensure user_application_service is awaited if necessary and not None
        print(f"{Config.App_name} controllers are starting...")
        log_event("INFO", f"{Config.App_name} controllers are starting...")

        user_controller = UserController(user_application_service)

        print(f"{Config.App_name} controllers are set up.")
        log_event("INFO", f"{Config.App_name} controllers are set up.")
        return user_controller  # Ensure this is returned
    except Exception as e:
        print(f"Error during {Config.App_name} startup: {e}")
        log_event("ERROR", f"Error during {Config.App_name} startup: {e}")
        sys.exit(1)
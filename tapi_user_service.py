import sys
from sanic import Sanic, SanicException
from sanic_ext import Extend
from app.application.application_services.tapi_user_application_service import UserApplicationService
from app.application.use_cases.services.tapi_user_service import UserUseCase
from app.infrastructure.controller.tapi_user_controller import UserController
from app.infrastructure.repository.tapi_user_repository import UserRepository
import common.utils.messages.common_messages as message
from framework.error.setup.error_setup import AppError
from framework.error.utils.handler.exception_handler import (
    app_error_handler,
    catch_all_exception_handler,
    sanic_exception_handler,
)
from configuration.configuration import Config
from framework.database.setup.database_setup import Database
from framework.logger.utils.helper.logger_helper import log_event
from framework.redis.setup.redis_setup import Redis
from framework.logger.middleware.logger_middleware import log_middleware, request_middleware
from framework.vault.setup.vault_setup import Vault
from framework.vault.utils.helper.vault_helper import VaultHelper
from textwrap import dedent

# Initialize the Sanic app
app = Sanic(Config.App_name)

app.config.CORS_ORIGINS = "*"


Extend(app)
app.ext.openapi.describe(
    "Tidal User API",
    version="2.0.1",
    description=dedent(
        """
        # Tidal User API Documentation

        Welcome to the Tidal User API, a comprehensive solution for managing user data within our application. This API is designed to offer developers access to user-related operations, including creation, update, retrieval, and deletion of user records.

        ## Features

        - **Create Users**: Allows for the registration of new users, including essential information such as names, contact details, and credentials.
        - **Update Users**: Supports updating user details post-registration to keep user data current.
        - **Retrieve Users**: Provides mechanisms to fetch user details by unique identifiers or list all users with pagination support.
        - **Delete Users**: Enables the removal of users from the system, ensuring data privacy and compliance.

        ## Getting Started

        To begin using the Tidal User API, you'll need to authenticate using our OAuth2.0 endpoints. Each request must include a valid token in the `Authorization` header.

        ## Error Handling

        The API uses standard HTTP status codes to indicate the success or failure of requests. In the case of errors, a JSON response will detail the issue, including an error reference ID for support purposes.

        **MARKDOWN** is supported in this documentation, allowing for rich text formatting, including bold, italics, and code blocks for clearer communication.

        ### Example Error Response

        ```json
        {
            "error_reference": "unique-error-id-12345",
            "error_type": "VALIDATION_ERROR",
            "errors": ["Invalid email address"],
            "status_code": 400,
            "timestamp": "2024-03-25T10:30:00.000Z"
        }
        ```

        For further assistance or to report issues, please contact our support team at support@example.com.

        Enjoy building with the Tidal User API!
        """
    ),
)


# Register middleware
app.request_middleware.append(request_middleware)
app.response_middleware.append(log_middleware)

# Register exception handlers
app.error_handler.add(SanicException, sanic_exception_handler)
app.error_handler.add(AppError, app_error_handler)
app.error_handler.add(Exception, catch_all_exception_handler)

@app.listener("before_server_start")
async def setup_services(app, loop):
    global database, redis, vault
    log_event("INFO", f"{Config.App_name} server is starting...")
    print(f"{Config.App_name} server is starting...")
    try:
        # Initialize and set up services
        database = Database.connect()
        log_event("INFO", message.DatabaseMessage.CONNECTION_SUCCESS)
        print(message.DatabaseMessage.CONNECTION_SUCCESS)

        redis = Redis.connect()
        log_event("INFO", message.RedisMessage.CONNECTION_SUCCESS)
        print(message.RedisMessage.CONNECTION_SUCCESS)

        vault = Vault.connect()
        log_event("INFO", message.VaultMessage.CONNECTION_SUCCESS)
        print(message.VaultMessage.CONNECTION_SUCCESS)

        # Get secrets from Vault
        Config.Secret_key = VaultHelper.get_secret(Config.Vault_path, Config.Vault_key)

        # Initialize application services
        log_event("INFO", f"Initializing {Config.App_name} services...")
        print(f"Initializing {Config.App_name} services...")
        user_repository = UserRepository(database)
        create_user_use_case = UserUseCase(user_repository)
        user_application_service = UserApplicationService(create_user_use_case)
        user_controller = UserController(user_application_service)


        # Register the route for creating a user
        app.add_route(user_controller.create_user, '/users', methods=['POST'])

        # Register the route for updating a user
        # Note: The placeholder <user_reference> in the route will be passed to the method as an argument
        app.add_route(user_controller.update_user, '/users/<user_reference:str>', methods=['PUT'])

        # Register the route for retrieving a user by reference
        app.add_route(user_controller.get_user_by_reference, '/users/<user_reference:str>', methods=['GET'])

        # Register the route for retrieving all users (with optional pagination)
        app.add_route(user_controller.get_all_users, '/users/<page:int>', methods=['GET'])

        # Register the route for deleting a user
        app.add_route(user_controller.delete_user, '/users/<user_reference:str>', methods=['DELETE'])


        log_event("INFO", f"{Config.App_name} services and routes are set up.")
        print(f"{Config.App_name} services and routes are set up.")
    except Exception as e:
        log_event("ERROR", f"Error during {Config.App_name} startup: {e}")
        print(f"Error during {Config.App_name} startup: {e}")
        sys.exit(1)

@app.listener("after_server_start")
async def notify_server_started(app, loop):
    log_event("INFO", f"{Config.App_name} has successfully started.")
    print(f"{Config.App_name} server has successfully started.")

@app.listener("before_server_stop")
async def notify_server_stopping(app, loop):
    log_event("INFO", f"{Config.App_name} is stopping...")
    print(f"{Config.App_name} is stopping...")

@app.listener("after_server_stop")
async def cleanup_services(app, loop):
    log_event("INFO", f"Disconnecting {Config.App_name} services...")
    print(f"Disconnecting {Config.App_name} services...")
    Database.disconnect()
    Redis.disconnect()
    Vault.disconnect()
    log_event("INFO", f"All {Config.App_name} services disconnected successfully.")
    print(f"All {Config.App_name} services disconnected successfully.")



if __name__ == "__main__":
    try:
        app.go_fast(host=Config.Address, port=Config.Port, auto_reload=False)
    except Exception as e:
        log_event("ERROR", f"An error occurred while running the {Config.App_name} server: {e}")
        print(f"An error occurred while running the {Config.App_name} server: {e}")
        sys.exit(1)

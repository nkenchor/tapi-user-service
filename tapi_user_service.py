import sys
from sanic import Sanic, SanicException, response
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


# Initialize the Sanic app
app = Sanic(Config.App_name)
# Add OpenAPI and Swagger UI blueprints


# Register exception handlers
app.error_handler.add(SanicException, sanic_exception_handler)
app.error_handler.add(AppError, app_error_handler)
app.error_handler.add(Exception, catch_all_exception_handler)

# Register middleware
app.request_middleware.append(request_middleware)
app.response_middleware.append(log_middleware)

@app.listener("before_server_start")
async def before_server_start(app, _):
    try:
        # Initialize and set up services (database, Redis, Vault)
        app.ctx.database = Database.connect()
        print(message.DatabaseMessage.CONNECTION_SUCCESS)
        log_event("INFO", message.DatabaseMessage.CONNECTION_SUCCESS)

        app.ctx.redis = Redis.connect()
        print(message.RedisMessage.CONNECTION_SUCCESS)
        log_event("INFO", message.RedisMessage.CONNECTION_SUCCESS)

        app.ctx.vault = Vault.connect()
        print(message.VaultMessage.CONNECTION_SUCCESS)
        log_event("INFO", message.VaultMessage.CONNECTION_SUCCESS)

        # Get secrets from Vault
        Config.Secret_key = VaultHelper.get_secret(Config.Vault_path, Config.Vault_key)

    except Exception as e:
        print(f"Unknown error occurred during server startup: {e}")
        log_event(f"Unknown error occurred during server startup: {e}")
        sys.exit(1)

@app.listener("after_server_start")
async def after_server_start(app, _):
    log_event("INFO", f"{Config.App_name} successfully started and services are ready.")


@app.listener("after_server_stop")
async def after_server_stop(app, _):
    # Clean up connections
    Database.disconnect()
    Redis.disconnect()
    Vault.disconnect()
    print(message.DatabaseMessage.CONNECTION_TERMINATED)
    print(message.RedisMessage.CONNECTION_TERMINATED)
    print(message.VaultMessage.CONNECTION_TERMINATED)
    log_event("INFO", "All services disconnected successfully.")

# Test route
@app.route("/")
async def test(request):
    log_event("INFO", "Test route accessed.", request=request)
    return response.json({"hello": "world"})

@app.after_server_start
async def setup_services(app, _):
    log_event("INFO", "Setting up application services.")
    # Initialize the repository, use case, and application service
    user_repository = UserRepository(app.ctx.database)
    create_user_use_case = UserUseCase(user_repository)
    user_application_service = UserApplicationService(create_user_use_case)

    # Initialize and set up controller
    app.ctx.user_controller = UserController(user_application_service)
    log_event("INFO", "User services successfully set up.")
    # Register routes
    
    # Register the route for creating a user
    app.add_route(app.ctx.user_controller.create_user, '/users', methods=['POST'])

    # Register the route for updating a user
    # Note: The placeholder <user_reference> in the route will be passed to the method as an argument
    app.add_route(app.ctx.user_controller.update_user, '/users/<user_reference:str>', methods=['PUT'])

    # Register the route for retrieving a user by reference
    app.add_route(app.ctx.user_controller.get_user_by_reference, '/users/<user_reference:str>', methods=['GET'])

    # Register the route for retrieving all users (with optional pagination)
    app.add_route(app.ctx.user_controller.get_all_users, '/users/<page:int>', methods=['GET'])

    # Register the route for deleting a user
    app.add_route(app.ctx.user_controller.delete_user, '/users/<user_reference:str>', methods=['DELETE'])


if __name__ == "__main__":
    app.run(host=Config.Address, port=Config.Port, auto_reload=False)

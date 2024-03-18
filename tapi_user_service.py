import sys
from sanic import Sanic, SanicException, response
from app.application.application_services.tapi_user_application_service import UserApplicationService
from app.application.use_cases.services.tapi_user_service import UserUseCase
from app.infrastructure.controller.tapi_user_controller import UserController
from app.infrastructure.repository.tapi_user_repository import UserRepository
import common.utils.messages as message
from framework.error.setup.error_setup import AppError
from framework.error.utils.handler.exception_handler import (
    app_error_handler,
    catch_all_exception_handler,
    sanic_exception_handler,
)
from configuration.configuration import Config
from framework.database.setup.database_setup import Database
from framework.redis.setup.redis_setup import Redis
from framework.logger.middleware.logger_middleware import log_middleware, request_middleware
from framework.vault.setup.vault_setup import Vault
from framework.vault.utils.helper.vault_helper import VaultHelper

# Initialize the Sanic app
app = Sanic(Config.App_name)

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

        app.ctx.redis = Redis.connect()
        print(message.RedisMessage.CONNECTION_SUCCESS)

        app.ctx.vault = Vault.connect()
        print(message.VaultMessage.CONNECTION_SUCCESS)

        # Get secrets from Vault
        Config.Secret_key = VaultHelper.get_secret(Config.Vault_path, Config.Vault_key)

    except Exception as e:
        print(f"Unknown error occurred during server startup: {e}")
        sys.exit(1)

@app.listener("after_server_stop")
async def after_server_stop(app, _):
    # Clean up connections
    Database.disconnect()
    Redis.disconnect()
    Vault.disconnect()
    print(message.DatabaseMessage.CONNECTION_TERMINATED)
    print(message.RedisMessage.CONNECTION_TERMINATED)
    print(message.VaultMessage.CONNECTION_TERMINATED)

# Test route
@app.route("/")
async def test(request):
    return response.json({"hello": "world"})

@app.after_server_start
async def setup_services(app, _):
    # Initialize the repository, use case, and application service
    user_repository = UserRepository(app.ctx.database)
    create_user_use_case = UserUseCase(user_repository)
    user_application_service = UserApplicationService(create_user_use_case)

    # Initialize and set up controller
    app.ctx.user_controller = UserController(user_application_service)

    # Register routes
    app.add_route(app.ctx.user_controller.create_user, '/users', methods=['POST'])

if __name__ == "__main__":
    app.run(host=Config.Address, port=Config.Port, auto_reload=False)

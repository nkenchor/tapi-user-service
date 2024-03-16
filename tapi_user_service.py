import sys
from sanic import Sanic, SanicException
from sanic.response import json
from sanic.exceptions import SanicException
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

app = Sanic(Config.App_name)

# Registering exception handlers
app.error_handler.add(SanicException, sanic_exception_handler)
app.error_handler.add(AppError, app_error_handler)
app.error_handler.add(Exception, catch_all_exception_handler)


@app.listener("before_server_start")
async def before_server_start(app, loop):
    try:
        # Initialize database connection
        Database.connect()
        print(message.DatabaseMessage.CONNECTION_SUCCESS)

        # Initialize Redis connection
        Redis.connect()
        print(message.RedisMessage.CONNECTION_SUCCESS)

        # Initialize Vault connection
        Vault.connect()
        print(message.VaultMessage.CONNECTION_SUCCESS)
        
        # Getting secrets
        Config.Secret_key = VaultHelper.get_secret(Config.Vault_path,Config.Vault_key)


    except Exception as e:
        error_message = f"Unknown error occurred during server startup: {str(e).splitlines()[0]}"
        print(error_message)
        print("Exiting the application due to an error during server startup.")
        print("Applicaiton stopped.")
        sys.exit(1)  # Exit the application process with a non-zero status code indicating an error


@app.listener("after_server_stop")
async def after_server_stop(app, loop):
    # Clean up database connection
    Database.disconnect()
    print(message.DatabaseMessage.CONNECTION_TERMINATED)

    # Clean up Redis connection
    Redis.disconnect()
    print(message.RedisMessage.CONNECTION_TERMINATED)

    # Clean up Vault connection
    Vault.disconnect()
    print(message.VaultMessage.CONNECTION_TERMINATED)


# Registering middleware
app.request_middleware.append(request_middleware)
app.response_middleware.append(log_middleware)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host=Config.Address, port=Config.Port)

import sys
from sanic import Sanic
from sanic_ext import Extend
from app.infrastructure.system.configuration.configuration import Config
from app.infrastructure.persistence.database.setup.database_setup import Database
from app.infrastructure.system.logger.utils.helper.logger_helper import log_event
from app.infrastructure.messaging.redis.setup.redis_setup import Redis
from app.infrastructure.secrets.vault.setup.vault_setup import Vault
from app.infrastructure.web.routes.routes import setup_routes
from app.infrastructure.web.handlers.handlers import setup_handlers
from app.infrastructure.web.middleware.middleware import setup_middleware
from app.infrastructure.web.services.services import initialize_controller, initialize_services
from app.infrastructure.web.docs.openapi_configuration import setup_openapi

# Initialize the Sanic app
app = Sanic(__name__)
app.config.CORS_ORIGINS = "*"

# Extend the app with Sanic-Ext
Extend(app)

# Use the external OpenAPI description
setup_openapi(app)

# Register middleware
setup_middleware(app)

# Register exception handlers
setup_handlers(app)


@app.listener("before_server_start")
async def setup_services(app, loop):
    user_application_service = await initialize_services()
    user_controller = await initialize_controller(user_application_service)
    # Now setup routes correctly
    setup_routes(app, user_controller)  # Assuming setup_routes doesn't need await

    
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

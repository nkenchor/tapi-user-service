import json
import logging
import time
from sanic import Request
from sanic.response import HTTPResponse
from app.infrastructure.system.configuration.configuration import Config
import app.infrastructure.system.logger.setup.logger_setup as logger_config
from app.infrastructure.system.logger.utils.data.logger_data import prepare_log_data

# Define the logger
logger = logging.getLogger('appLogger')

def create_header(response, key, value):
    if key not in response.headers:
        response.headers[key] = value

def truncate_response(response):
    return response[:300]

async def log_middleware(request: Request, response: HTTPResponse):
    if "/swagger" not in request.path:  # Exclude Swagger paths
        log_data = prepare_log_data(request, response)
        log_message = json.dumps(log_data)
        logger.info(log_message)
        create_header(response, "Content-Type", "application/json")
        create_header(response, "X-Correlation-ID", log_data.get("correlation_id", ""))

async def request_middleware(request: Request):
    if "/swagger" not in request.path:  # Exclude Swagger paths
        request.ctx.start_time = time.time()

# Call the register_logger function to set up the logger
logger_config.register_logger(Config.Log_dir,Config.Log_file)

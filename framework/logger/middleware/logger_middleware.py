import json
import logging
import socket
import time
import traceback
import uuid
from datetime import datetime
from sanic import Request
from sanic.response import HTTPResponse
from configuration.configuration import Config
import framework.logger.setup.logger_setup as logger_config

# Define the logger
logger = logging.getLogger('appLogger')

def create_header(response, key, value):
    if key not in response.headers:
        response.headers[key] = value

def truncate_response(response):
    return response[:300]

async def log_middleware(request: Request, response: HTTPResponse):
    payload = request.body if request.body else ""
    level = "INFO"
    
    if response.status >= 400:
        level = "ERROR"
        
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "method": request.method,
        "status_code": str(response.status),
        "path": str(request.url),
        "forwarded_for": request.headers.get("X-Forwarded-For", ""),
        "response_time": str(time.time() - request.ctx.start_time),
        # "payload": payload,
        # "message": f"{response.status} : {truncate_response(response.body.decode('utf-8'))} ...",
        "version": "1",
        "correlation_id": request.headers.get("X-Correlation-ID", ""),
        "app_name": Config.App_name,
        "application_host": request.host,
        "logger_name": "",
        # Additional fields
        "ip": request.ip,
        "computerName": socket.gethostname(),
        # "requestProtocol": request.protocol, # Exclude request protocol
        "requestHeaders": dict(request.headers),
        "requestQuery": request.query_args,
        "requestBody": request.body.decode("utf-8") if request.body else "",
        "logId": str(uuid.uuid4()),
        "responseHeaders": dict(response.headers),
        "responseBody": response.body.decode("utf-8") if response.body else "",
        "requestDuration": time.time() - request.ctx.start_time,
        "error": "",
        "stack": "",    
    }
    
    if level == "ERROR":
        log_data["error"]= log_data["responseBody"]
        log_data["stack"] = traceback.format_exc()

    log_message = json.dumps(log_data)
    
    # Write log message to the logger
    logger.info(log_message)

    # Ensure necessary headers are added to the response
    create_header(response, "Content-Type", "application/json")
    create_header(response, "X-Correlation-ID", log_data["correlation_id"])

async def request_middleware(request: Request):
    request.ctx.start_time = time.time()

# Call the register_logger function to set up the logger
logger_config.register_logger(Config.Log_dir,Config.Log_file)

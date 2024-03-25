
import socket
import time
import traceback
from typing import Optional
import uuid
from datetime import datetime
from sanic import Request
from sanic.response import HTTPResponse
from app.domain.shared.shared_utils import get_server_ip
from app.infrastructure.system.configuration.configuration import Config


def prepare_log_data(request: Optional[Request] = None, response: Optional[HTTPResponse] = None, 
                     level: str = "INFO", message: str = "", extra_data: dict = None) -> dict:
    if response and response.status >= 400:
        level = "ERROR"
    
    # Determine the current time as the end time for calculating response time
    end_time = time.time()

    # Default start time - only used if no request context is available
    # For non-HTTP operations, this results in a minimal, but non-zero, response time
    default_start_time = end_time - 0.001  # Default to 1 millisecond before end_time

    # Calculate response time based on available context
    response_time = str(end_time - (request.ctx.start_time if request and hasattr(request.ctx, 'start_time') else default_start_time))


    # Basic log data structure
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "method": request.method if request else "EVENT",
        "status_code": str(response.status) if response else "000",
        "path": str(request.url) if request else "127.0.0.1",
        "forwarded_for": request.headers.get("X-Forwarded-For", "") if request else "",
        "response_time": str(time.time() - request.ctx.start_time) if request else response_time,
        "version": "1",
        "correlation_id": request.headers.get("X-Correlation-ID", "") if request else "",
        "app_name": Config.App_name,
        "application_host": request.host if request else socket.gethostname(),
        "ip": request.ip if request else get_server_ip(),
        "computerName": socket.gethostname(),
        "logId": str(uuid.uuid4()),
        "message": message,
        # Additional details can be filled with provided or default values
        "requestHeaders": dict(request.headers) if request else {},
        "requestQuery": request.query_args if request else {},
        "requestBody": request.body.decode("utf-8") if request and request.body else "",
        "responseHeaders": dict(response.headers) if response else {},
        "responseBody": response.body.decode("utf-8") if response and response.body else "",
        "requestDuration": time.time() - request.ctx.start_time if request else 0,
        "error": "",
        "stack": "", 
    }

    # If level is ERROR, include error details and stack trace
    if level == "ERROR":
        log_data["error"] = log_data["responseBody"]
        log_data["stack"] = traceback.format_exc()

    # Include any additional data provided
    if extra_data:
        log_data.update(extra_data)

    return log_data

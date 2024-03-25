import json
import logging
from typing import Optional
from sanic import Request
from app.infrastructure.system.logger.utils.data.logger_data import prepare_log_data

logger = logging.getLogger('appLogger')

def log_event(level: str, message: str, request: Optional[Request] = None, extra_data: dict = None):
    log_data = prepare_log_data(request, level=level, message=message, extra_data=extra_data)
    log_message = json.dumps(log_data)
    logger.log(logging.getLevelName(level.upper()), log_message)

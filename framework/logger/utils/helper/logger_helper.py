import json
import logging
import socket
import time
import traceback
from typing import Optional
import uuid
from datetime import datetime
from sanic import Request
from sanic.response import HTTPResponse
from configuration.configuration import Config
import framework.logger.setup.logger_setup as logger_config
from framework.logger.utils.data.logger_data import prepare_log_data

logger = logging.getLogger('appLogger')

def log_event(level: str, message: str, request: Optional[Request] = None, extra_data: dict = None):
    log_data = prepare_log_data(request, level=level, message=message, extra_data=extra_data)
    log_message = json.dumps(log_data)
    logger.log(logging.getLevelName(level.upper()), log_message)

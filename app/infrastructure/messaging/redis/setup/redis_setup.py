import redis

from app.infrastructure.system.configuration.configuration import Config
from app.infrastructure.system.logger.utils.helper.logger_helper import log_event


class Redis:
    client = None
    isConnected = False

    @staticmethod
    def connect():
        if not Redis.client or not Redis.isConnected:
            Redis.client = redis.StrictRedis(host=Config.Redis_host, port=Config.Redis_port)
            try:
                # Check if the connection is successful
                Redis.client.ping()
                Redis.isConnected = True
                log_event("INFO", "Connected successfully to Redis")
            except Exception as err:
                log_event("ERROR", f"Could not connect to Redis: {err}")
                raise err
        return Redis.client

    @staticmethod
    def disconnect():
        if Redis.client and Redis.isConnected:
            Redis.client.close()
            Redis.isConnected = False
            log_event("INFO", "Disconnected from Redis")

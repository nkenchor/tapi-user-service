from framework.logger.utils.helper.logger_helper import log_event
from framework.redis.setup.redis_setup import Redis

class PublisherHelper:
    @staticmethod
    def publish(channel, message):
        try:
            redis_client = Redis.connect()
            redis_client.publish(channel, message)
            # Use log_event for success logging
            log_event("INFO", f"Message '{message}' published to channel '{channel}'")
        except Exception as e:
            # Use log_event for error logging
            log_event("ERROR", f"Error publishing message to channel '{channel}': {str(e)}")
            raise e

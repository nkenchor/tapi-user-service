
from app.infrastructure.messaging.redis.setup.redis_setup import Redis
from app.infrastructure.system.logger.utils.helper.logger_helper import log_event


class SubscriberHelper:
    def __init__(self, channels, callback):
        self.channels = channels
        self.callback = callback
        self.pubsub = None

    def subscribe(self):
        try:
            redis_client = Redis.connect()
            self.pubsub = redis_client.pubsub()
            self.pubsub.subscribe(self.channels)
            # Log successful subscription
            log_event("INFO", f"Subscribed to channels: {', '.join(self.channels)}")
        except Exception as e:
            # Log error on subscription failure
            log_event("ERROR", f"Error subscribing to channels: {e}")
            raise e

    def listen(self):
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    # Log incoming messages, consider logging level and sensitivity of message content
                    log_event("INFO", f"Message received on channel {message['channel']}: {message['data']}")
                    self.callback(message['channel'], message['data'])
        except Exception as e:
            # Log error on listening failure
            log_event("ERROR", f"Error listening to messages: {e}")
            raise e

    def unsubscribe(self):
        try:
            if self.pubsub:
                self.pubsub.unsubscribe()
                # Log successful unsubscription
                log_event("INFO", "Unsubscribed from channels")
        except Exception as e:
            # Log error on unsubscription failure
            log_event("ERROR", f"Error unsubscribing from channels: {e}")
            raise e

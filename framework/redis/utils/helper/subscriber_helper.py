

from framework.redis.setup.redis_setup import Redis


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
            print(f"Subscribed to channels: {', '.join(self.channels)}")
        except Exception as e:
            print("Error subscribing to channels:", e)
            raise e

    def listen(self):
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    self.callback(message['channel'], message['data'])
        except Exception as e:
            print("Error listening to messages:", e)
            raise e

    def unsubscribe(self):
        try:
            if self.pubsub:
                self.pubsub.unsubscribe()
                print("Unsubscribed from channels")
        except Exception as e:
            print("Error unsubscribing from channels:", e)
            raise e

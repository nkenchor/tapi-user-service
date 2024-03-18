

from framework.redis.setup.redis_setup import Redis


class PublisherHelper:
    @staticmethod
    def publish(channel, message):
        try:
            redis_client = Redis.connect()
            redis_client.publish(channel, message)
            print(f"Message '{message}' published to channel '{channel}'")
        except Exception as e:
            print("Error publishing message:", e)
            raise e

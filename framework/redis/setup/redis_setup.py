import redis
from configuration.configuration import Config

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
                print("Connected successfully to Redis")
            except Exception as err:
                print("Could not connect to Redis:", err)
                raise err
        return Redis.client

    @staticmethod
    def disconnect():
        if Redis.client and Redis.isConnected:
            Redis.client.close()
            Redis.isConnected = False
            print("Disconnected from Redis")

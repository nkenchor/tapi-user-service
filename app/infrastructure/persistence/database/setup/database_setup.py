
from pymongo import MongoClient

from app.infrastructure.system.logger.utils.helper.logger_helper import log_event
from app.infrastructure.system.configuration.configuration import Config

class Database:
    client = None
    isConnected = False

    @staticmethod
    def connect():
        if not Database.client or not Database.isConnected:
            Database.client = MongoClient(Config.Db_url)
            try:
                # In pymongo, calling client.db triggers the connection
                Database.isConnected = True
                log_event("INFO", "Connected successfully to MongoDB")
            except Exception as err:
                log_event("ERROR", f"Could not connect to MongoDB: {err}")
                raise err
        return Database.client[Config.Db]

    @staticmethod
    def disconnect():
        if Database.client and Database.isConnected:
            Database.client.close()
            Database.isConnected = False
            log_event("INFO", "Disconnected from MongoDB")
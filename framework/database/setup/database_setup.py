
from configuration.configuration import Config
from pymongo import MongoClient


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
                print("Connected successfully to MongoDB")
            except Exception as err:
                print("Could not connect to MongoDB", err)
                raise err
        return Database.client[Config.Db]

    @staticmethod
    def disconnect():
        if Database.client and Database.isConnected:
            Database.client.close()
            Database.isConnected = False
            print("Disconnected from MongoDB")

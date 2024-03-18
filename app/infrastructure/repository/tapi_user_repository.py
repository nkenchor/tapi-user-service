from pymongo import MongoClient
from bson import ObjectId

from app.domain.models.tapi_user_model import User
from configuration.configuration import Config
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
class UserRepository:
    def __init__(self, db_client: MongoClient):
        self.collection: Collection = db_client['users']

    def create_user(self, user: User) -> str:
        """
        Create a new user.

        Args:
            user (User): User object containing user data.

        Returns:
            str: The reference ID of the created user.
        """
        try:
            self.collection.insert_one(user.__dict__)
            return str(user.user_reference)
        except PyMongoError as e:
            print(f"Error adding user: {e}")
            # Handle or re-raise the error as appropriate for your application
            raise e

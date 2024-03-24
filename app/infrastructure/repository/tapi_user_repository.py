from typing import List
from pymongo import MongoClient
from app.application.repository_port.tapi_user_respository_port import (
    IUserRepositoryPort,
)
from app.domain.models.tapi_user_model import User
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from framework.logger.utils.helper.logger_helper import (
    log_event,
)  # Ensure correct import path


class UserRepository(IUserRepositoryPort):
    def __init__(self, db_client: MongoClient):
        self.collection: Collection = db_client["users"]

    def create_user(self, user: User) -> str:
        try:
            self.collection.insert_one(user.__dict__)
            log_event("INFO", f"User {user.user_reference} created successfully.")
            return str(user.user_reference)
        except PyMongoError as e:
            log_event("ERROR", f"Error adding user: {e}")
            raise e

    def update_user(self, user_reference: str, user_data: User) -> str:
        try:
            self.collection.update_one(
                {"user_reference": user_reference}, {"$set": user_data.__dict__}
            )
            log_event("INFO", f"User {user_reference} updated successfully.")
            return user_reference
        except PyMongoError as e:
            log_event("ERROR", f"Error updating user: {e}")
            raise e

    def get_user_by_reference(self, user_reference: str) -> User:
        try:
            user_data = self.collection.find_one({"user_reference": user_reference})
            if user_data:
                log_event("INFO", f"User {user_reference} retrieved successfully.")
                return User(**user_data)
            else:
                log_event("WARNING", f"User {user_reference} not found.")
                return None
        except PyMongoError as e:
            log_event("ERROR", f"Error retrieving user: {e}")
            raise e

    def get_all_users(self, page: int, per_page: int = 10) -> List[User]:
        try:
            users = self.collection.find().skip((page - 1) * per_page).limit(per_page)
            log_event("INFO", "Users retrieved successfully.")
            return [User(**user_data) for user_data in users]
        except PyMongoError as e:
            log_event("ERROR", f"Error retrieving users: {e}")
            raise e

    def get_users_by_query(
        self, query_params: dict, page: int, per_page: int = 10
    ) -> List[User]:
        try:
            users = (
                self.collection.find(query_params)
                .skip((page - 1) * per_page)
                .limit(per_page)
            )
            log_event("INFO", "Users retrieved by query successfully.")
            return [User(**user_data) for user_data in users]
        except PyMongoError as e:
            log_event("ERROR", f"Error retrieving users by query: {e}")
            raise e

    def delete_user(self, user_reference: str) -> bool:
        try:
            result = self.collection.delete_one({"user_reference": user_reference})
            if result.deleted_count > 0:
                log_event("INFO", f"User {user_reference} deleted successfully.")
            return result.deleted_count > 0
        except PyMongoError as e:
            log_event("ERROR", f"Error deleting user: {e}")
            raise e

    def soft_delete_user(self, user_reference: str) -> bool:
        try:
            result = self.collection.update_one(
                {"user_reference": user_reference}, {"$set": {"is_active": False}}
            )
            if result.modified_count > 0:
                log_event("INFO", f"User {user_reference} soft deleted successfully.")
            return result.modified_count > 0
        except PyMongoError as e:
            log_event("ERROR", f"Error soft deleting user: {e}")
            raise e

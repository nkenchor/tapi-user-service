from abc import ABC, abstractmethod
from typing import List
from app.domain.models.tapi_user_model import User


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user_data: User) -> str:
        """Create a new user and return its reference."""
        pass

    @abstractmethod
    def update_user(self, user_reference: str, user_data: User) -> str:
        """Update an existing user and return its reference."""
        pass

    @abstractmethod
    def get_user_by_reference(self, user_reference: str) -> User:
        """Get a user by reference."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        """Get a user by  email."""
        pass

    @abstractmethod
    def get_all_users(self, page: int) -> List[User]:
        """
        Retrieve a paginated list of all users.

        Parameters:
            page (int): The page number to retrieve.

        Returns:
            List[User]: A list of User objects representing the users on the specified page.
        """
        pass

    @abstractmethod
    def get_users_by_query(self, query_params: dict, page: int) -> List[User]:
        """
        Retrieve a paginated list of users based on query parameters.

        Parameters:
            query_params (dict): A dictionary containing query parameters.
            page (int): The page number to retrieve.

        Returns:
            List[User]: A list of User objects representing the users matching the query parameters.
        """
        pass

    @abstractmethod
    def delete_user(self, user_reference: str) -> bool:
        """
        Delete a user permanently.

        Parameters:
            user_reference (str): The reference of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def soft_delete_user(self, user_reference: str) -> bool:
        """
        Soft delete a user.

        Parameters:
            user_reference (str): The reference of the user to soft delete.

        Returns:
            bool: True if the user was successfully soft deleted, False otherwise.
        """
        pass

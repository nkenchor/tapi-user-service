from app.application.use_cases.service_port.tapi_user_service_port import IUserUseCasePort
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.dtos.tapi_user_update_dto import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User
from typing import List

class UserApplicationService:
    def __init__(self, user_use_case: IUserUseCasePort):
        self.user_use_case = user_use_case

    def create_user(self, user_dto: UserCreateDTO) -> str:
        """
        Create a new user based on the provided UserCreateDTO.

        Args:
            user_dto (UserCreateDTO): DTO containing user data.

        Returns:
            str: The reference ID of the created user.
        """
        # No need to convert UserCreateDTO to User here if the use case expects a UserCreateDTO.
        # The use case itself should handle any transformations and business logic.
        return self.user_use_case.create_user(user_dto)

    def update_user(self, user_reference: str, user_dto: UserUpdateDTO) -> str:
        """
        Update an existing user based on the provided UserUpdateDTO.

        Args:
            user_reference (str): The reference ID of the user to be updated.
            user_dto (UserUpdateDTO): DTO containing updated user data.

        Returns:
            str: The reference ID of the updated user.
        """
        return self.user_use_case.update_user(user_reference, user_dto)

    def get_user_by_reference(self, user_reference: str) -> User:
        """
        Retrieve a user by its reference ID.

        Args:
            user_reference (str): The reference ID of the user to retrieve.

        Returns:
            User: The retrieved user object.
        """
        return self.user_use_case.get_user_by_reference(user_reference)

    def get_all_users(self, page: int) -> List[User]:
        """
        Retrieve all users, paginated.

        Args:
            page (int): The page number of the user list to retrieve.

        Returns:
            List[User]: A list of User objects on the specified page.
        """
        return self.user_use_case.get_all_users(page)

    def delete_user(self, user_reference: str) -> bool:
        """
        Delete a user permanently.

        Args:
            user_reference (str): The reference ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        return self.user_use_case.delete_user(user_reference)

    def soft_delete_user(self, user_reference: str) -> bool:
        """
        Soft delete a user, marking it as inactive or deleted without permanently removing it.

        Args:
            user_reference (str): The reference ID of the user to soft delete.

        Returns:
            bool: True if the user was successfully soft deleted, False otherwise.
        """
        return self.user_use_case.soft_delete_user(user_reference)

    # You can add more methods here following the same pattern if your IUserUseCasePort defines more functionalities.

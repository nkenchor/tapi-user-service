from app.application.use_cases.service_port.tapi_user_service_port import IUserUseCasePort
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO

class UserApplicationService:
    def __init__(self, create_user_use_case: IUserUseCasePort):
        self.create_user_use_case = create_user_use_case

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
        return self.create_user_use_case.create_user(user_dto)

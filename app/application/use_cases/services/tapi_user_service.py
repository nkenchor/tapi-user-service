from app.application.repository_port.tapi_user_respository_port import IUserRepositoryPort
from app.application.use_cases.service_port.tapi_user_service_port import IUserUseCasePort
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.models.tapi_user_model import User



class UserUseCase(IUserUseCasePort):
    def __init__(self, user_repository: IUserRepositoryPort):
        self.user_repository = user_repository

    def create_user(self, user_dto: UserCreateDTO) -> str:
        """
        Create a new user.

        Args:
            user_dto (UserCreateDTO): DTO containing user data.

        Returns:
            str: The reference ID of the created user.
        """
        # Create a domain model User object from the DTO
        user = User(
            user_reference = user_dto.user_reference,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            mobile_number=user_dto.mobile_number,
            email=user_dto.email,
            address=user_dto.address,
            companies=user_dto.companies,
            notification_options={},  # Assuming it's provided elsewhere or defaulted
            is_verified_email=False,  # Assuming initial verification status
            is_verified_phone=False,  # Assuming initial verification status
            is_active=True,  # Assuming newly created users are active
        )

        # Save the user to the repository and return the reference ID
        return self.user_repository.create_user(user)

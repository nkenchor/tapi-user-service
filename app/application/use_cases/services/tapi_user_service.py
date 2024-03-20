import uuid
from app.application.repository_port.tapi_user_respository_port import IUserRepositoryPort
from app.application.use_cases.service_port.tapi_user_service_port import IUserUseCasePort
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.dtos.tapi_user_update_dto import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User
from typing import List

class UserUseCase(IUserUseCasePort):
    def __init__(self, user_repository: IUserRepositoryPort):
        self.user_repository = user_repository

    def create_user(self, user_dto: UserCreateDTO) -> str:
        user = User(
            user_reference=str(uuid.uuid4()),  # Assuming user_reference is generated here
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            mobile_number=user_dto.mobile_number,
            email=user_dto.email,
            address=user_dto.address,
            companies=user_dto.companies,
            notification_options={},  # Adjust as needed
            is_verified_email=False,
            is_verified_phone=False,
            is_active=True,
        )
        return self.user_repository.create_user(user)

    def update_user(self, user_reference: str, user_dto: UserUpdateDTO) -> str:
        user = User(
            user_reference=user_reference,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            mobile_number=user_dto.mobile_number,
            email=user_dto.email,
            address=user_dto.address,
            companies=user_dto.companies,
            notification_options=user_dto.notification_options,  # Assuming these are part of the update DTO
            # Keep other fields that may not be updated directly
        )
        return self.user_repository.update_user(user_reference, user)

    def get_user_by_reference(self, user_reference: str) -> User:
        return self.user_repository.get_user_by_reference(user_reference)

    def get_all_users(self, page: int) -> List[User]:
        return self.user_repository.get_all_users(page)

    def delete_user(self, user_reference: str) -> bool:
        return self.user_repository.delete_user(user_reference)

    def soft_delete_user(self, user_reference: str) -> bool:
        return self.user_repository.soft_delete_user(user_reference)

    # Implement other methods as required by your application logic

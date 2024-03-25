from datetime import datetime
import uuid
from app.domain.repository_interfaces.tapi_user_respository_interface import IUserRepository
from app.application.use_cases.use_case_interfaces.tapi_user_service_interface import IUserUseCase
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.dtos.tapi_user_update_dto import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User
from typing import List


class UserUseCase(IUserUseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create_user(self, user_dto: UserCreateDTO,current_user_reference:str) -> str:
        user = User(
            user_reference=str(uuid.uuid4()),  # Assuming user_reference is generated here
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            mobile_number=user_dto.mobile_number,
            email=user_dto.email,
            organisations={},
            is_verified_email=False,
            is_verified_phone=False,
            is_active=True,
            created_at_timestamp = datetime.now().isoformat(),
            updated_at_timestamp = datetime.now().isoformat(),
            created_by_user_reference = current_user_reference,
            updated_by_user_reference = current_user_reference,
            consent_preferences= user_dto.consent_preferences
        )
        return self.user_repository.create_user(user)

    def update_user(self, user_reference: str, user_dto: UserUpdateDTO,current_user_reference:str) -> str:
        user = User(
            user_reference=user_reference,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            mobile_number=user_dto.mobile_number,
            email=user_dto.email,
            organisations={},
            is_verified_email=False,
            is_verified_phone=False,
            is_active=True,
            created_at_timestamp = datetime.now().isoformat(),
            updated_at_timestamp = datetime.now().isoformat(),
            created_by_user_reference = current_user_reference,
            updated_by_user_reference = current_user_reference,
            consent_preferences= user_dto.consent_preferences
        )
        return self.user_repository.update_user(user_reference, user)

    def get_user_by_reference(self, user_reference: str) -> User:
        return self.user_repository.get_user_by_reference(user_reference)
    
    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)


    def get_all_users(self, page: int) -> List[User]:
        return self.user_repository.get_all_users(page)

    def delete_user(self, user_reference: str) -> bool:
        return self.user_repository.delete_user(user_reference)

    def soft_delete_user(self, user_reference: str) -> bool:
        return self.user_repository.soft_delete_user(user_reference)

    

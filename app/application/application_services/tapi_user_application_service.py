
from app.application.use_cases.use_case_interfaces.tapi_user_interface import (
    IUserUseCase,
)
from app.domain.dtos.tapi_user_create import UserCreateDTO
from app.domain.dtos.tapi_user_organisation import UserAddOrganisationDTO, UserRemoveOrganisationDTO
from app.domain.dtos.tapi_user_update import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User
from typing import List




class UserApplicationService:
    def __init__(
        self, user_use_case: IUserUseCase
    ):
        self.user_use_case = user_use_case

    def create_user(self, user_dto: UserCreateDTO) -> str:
        return self.user_use_case.create_user(user_dto)

       
    def update_user(self, user_reference: str, user_dto: UserUpdateDTO, current_user_reference) -> str:
        return self.user_use_case.update_user(user_reference, user_dto, current_user_reference)
       
    
    def remove_user_from_organisation(self, user_reference: str, organisation_remove_dto: UserRemoveOrganisationDTO, current_user_reference) -> str:
        return self.user_use_case.remove_user_from_organisation(user_reference, organisation_remove_dto, current_user_reference)
       
    def add_user_to_organisation(self, user_reference: str, user_dto: UserAddOrganisationDTO, current_user_reference) -> str:
        return self.user_use_case.add_user_to_organisation(user_reference, user_dto, current_user_reference)

    def get_user_by_reference(self, user_reference: str) -> User:
        return self.user_use_case.get_user_by_reference(user_reference)

    def get_all_users(self, page: int) -> List[User]:
        return self.user_use_case.get_all_users(page)

    def delete_user(self, user_reference: str) -> bool:
        return self.user_use_case.delete_user(user_reference)

    def soft_delete_user(self, user_reference: str) -> bool:
        return self.user_use_case.soft_delete_user(user_reference)

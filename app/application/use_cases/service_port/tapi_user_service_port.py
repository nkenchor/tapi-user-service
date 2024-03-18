from abc import ABC, abstractmethod
from app.domain.dtos.tapi_user_create_dto import UserCreateDTO
from app.domain.models.tapi_user_model import User

class IUserUseCasePort(ABC):
    @abstractmethod
    def create_user(self, user_dto: UserCreateDTO) -> str:
        """Create a new user."""
        pass

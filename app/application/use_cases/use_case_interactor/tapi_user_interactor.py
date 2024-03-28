

from datetime import datetime
from app.application.events.etos.eto import Event
from app.application.events.event_publisher_interfaces.tapi_user_event_publisher_interface import IUserEventPublisher
from app.domain.dtos.tapi_user_organisation import UserAddOrganisationDTO, UserRemoveOrganisationDTO
from app.domain.repository_interfaces.tapi_user_respository_interface import (
    IUserRepository,
)
from app.application.use_cases.use_case_interfaces.tapi_user_interface import (
    IUserUseCase,
)
from app.domain.dtos.tapi_user_create import UserCreateDTO
from app.domain.dtos.tapi_user_update import UserUpdateDTO  # Assuming this exists
from app.domain.models.tapi_user_model import User
from typing import List

from app.domain.shared.shared_errors import DomainError, ErrorType


class UserUseCase(IUserUseCase):
    def __init__(self, user_repository: IUserRepository,user_event_publisher: IUserEventPublisher):
        self.user_repository = user_repository
        self.user_event_publisher = user_event_publisher

    def create_user(self, user_dto: UserCreateDTO) -> str:
         # Check if a user with the same email already exists
        existing_user = self.user_repository.get_user_by_email(user_dto.email)
        #  If the user exists by email
        if existing_user:
            # If the user exists, raise a conflict error
            raise DomainError(
                ErrorType.ConflictError,
                f"A user with the email {user_dto.email} already exists.",
        )
        # check if the user exists by user reference
        existing_user = self.user_repository.get_user_by_reference(user_dto.user_reference)

        if existing_user:
            # If the user exists, raise a conflict error
            raise DomainError(
                ErrorType.ConflictError,
                f"A user with the reference {user_dto.user_reference} already exists.",
        )

        #  map dto to user object
        user = User.from_create_dto(user_dto)
        #  create user
        user_reference =  self.user_repository.create_user(user)
        
         # Create a user created event
        user_created_event = Event(
            "UserCreatedEvent", "UserEvent", user_reference, user_dto.to_json()
        ).serialize()

        # publish user created event
        self.user_event_publisher.publish_user_created_event(user_created_event)
        
        return user_reference


    def update_user(self, user_reference: str, user_dto: UserUpdateDTO, current_user_reference: str) -> str:
        
        # check if is logged in
       
        if not user_reference == current_user_reference:
            # If the user exists, raise a conflict error
            raise DomainError(
                ErrorType.UnAuthorized, "You are not authorized to update this user details"
            )
        # check if user exists
        user = self.user_repository.get_user_by_reference(user_reference)
        if not user:
            # If the user exists, raise a conflict error
            raise DomainError(
                ErrorType.NotFound, 
                f"A user record with the reference {user_reference} does not exist.",
            )

        user.first_name = user_dto.first_name
        user.last_name = user_dto.last_name
        user.mobile_number = user_dto.mobile_number
        user.updated_at_timestamp = user_dto.updated_at_timestamp
        user.consent_preferences = user_dto.consent_preferences
        
        self.user_repository.update_user(user_reference, user)
      # Create a user updated event
        user_updated_event = Event(
            "UserUpdatedEvent", "UserEvent", user_reference, user.to_json()
        ).serialize()

        # publish user updated event
        self.user_event_publisher.publish_user_updated_event(user_updated_event)

        return user_reference

    def add_user_to_organisation(
        self, user_reference: str, user_dto: UserAddOrganisationDTO, current_user_reference: str
    ) -> str:
        
         # check if is logged in
       
        if not user_reference == current_user_reference:
            # If the user exists, raise a conflict error
            raise DomainError(
                ErrorType.UnAuthorized, "You are not authorized to update this user details"
            )
        
        #  check if user exists
        user = self.user_repository.get_user_by_reference(user_reference)
        if not user:
            # The target user for the update does not exist
            raise DomainError(
                ErrorType.NotFound, 
                f"A user record with the reference {user_reference} does not exist.",
            )

        # Check if the user already belongs to the specified organization
        # by comparing a unique identifier like organisation_name or organisation_id
        if any(organisation.organisation_name == user_dto.organisation.organisation_name for organisation in user.organisations):
            # The user already belongs to this organisation
            raise DomainError(
                ErrorType.ConflictError, 
                f"User already belongs to organisation: {user_dto.organisation.organisation_name}.",
            )
            
        # Add the new organisation to the user's list of organisations
        user.organisations.append(user_dto.organisation)
        user.updated_at_timestamp = user_dto.updated_at_timestamp

        # Update the user record in the repository
        self.user_repository.update_user(user_reference, user)
        
         # Create an event
        user_updated_event = Event(
            "UserAddedToOrganisationEvent", "UserEvent", current_user_reference, user.to_json()
        ).serialize()

        # publish user updated event
        self.user_event_publisher.publish_user_added_to_organisation_event(user_updated_event)

        return user_reference

    def remove_user_from_organisation(
        self, user_reference: str, organisation_remove_dto: UserRemoveOrganisationDTO, current_user_reference: str) -> str:
        
          # check if is logged in
       
        if not user_reference == current_user_reference:
            # If the user exists, raise a conflict error
            raise DomainError(
                ErrorType.UnAuthorized, "You are not authorized to update this user details"
            )
        

        user = self.user_repository.get_user_by_reference(user_reference)
        if not user:
            # The target user for the update does not exist
            raise DomainError(
                ErrorType.NotFound, 
                f"A user record with the reference {user_reference} does not exist.",
            )

        # Check if the user belongs to the specified organization
        organisation = next((org for org in user.organisations if org.organisation_reference == organisation_remove_dto.organisation_reference), None)
        if not organisation:
            # The user does not belong to this organisation
            raise DomainError(
                ErrorType.ConflictError, 
                f"User does not belong to the organisation with reference: {organisation_remove_dto.organisation_reference}.",
            )
            
        # Remove the specified organisation from the user's list of organisations
        user.organisations.remove(organisation)
        user.updated_at_timestamp = datetime.now().isoformat()

        # Update the user record in the repository
        self.user_repository.update_user(user_reference, user)
        
          # Create a user updated event
        user_updated_event = Event(
            "UserRemovedFromOrganisationEvent", "UserEvent", current_user_reference, user.to_json()
        ).serialize()

        # publish user updated event
        self.user_event_publisher.publish_user_added_to_organisation_event(user_updated_event)

        return user_reference

        
    def get_user_by_reference(self, user_reference: str) -> User:
        user =  self.user_repository.get_user_by_reference(user_reference)
        if not user:
            raise DomainError(
                ErrorType.NotFound, 
                f"A user record with the reference {user_reference} does not exist.",
            )
        return user

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)

    def get_all_users(self, page: int) -> List[User]:
        return self.user_repository.get_all_users(page)

    def delete_user(self, user_reference: str) -> bool:
        return self.user_repository.delete_user(user_reference)

    def soft_delete_user(self, user_reference: str) -> bool:
        return self.user_repository.soft_delete_user(user_reference)

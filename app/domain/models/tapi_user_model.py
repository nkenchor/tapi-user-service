from typing import List,  Optional


from app.domain.models.tapi_organisation_model import Organisation
import app.domain.shared.shared_validation as validator

class User:
    def __init__(
        self,
        user_reference: str,
        first_name: str,
        last_name: str,
        mobile_number: str,
        email: str,
        organisations: List[Organisation],
        is_verified_email: bool,
        is_verified_phone: bool,
        is_active: bool,
        created_at_timestamp: Optional[str] = "",
        updated_at_timestamp: Optional[str] = "",
        created_by_user_reference: Optional[str] = "",
        updated_by_user_reference: Optional[str] = "",
        consent_preferences: dict = None,
        **kwargs  # Accept any additional keyword arguments
    ):
        self.user_reference = user_reference
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{self.first_name} {self.last_name}"  # Updated for a more common full name format
        self.mobile_number = mobile_number
        self.email = email
        self.organisations = organisations
        self.is_verified_email = is_verified_email
        self.is_verified_phone = is_verified_phone
        self.is_active = is_active
        self.created_at_timestamp = created_at_timestamp
        self.updated_at_timestamp = updated_at_timestamp
        self.created_by_user_reference = created_by_user_reference
        self.updated_by_user_reference = updated_by_user_reference
        self.consent_preferences = consent_preferences or {}



        validator.validate_non_empty_string(self.first_name, "First name")
        validator.validate_non_empty_string(self.last_name, "Last name")
        validator.validate_email_format(self.email)
        validator.validate_mobile_number_format(self.mobile_number)

        # Optionally log or handle unexpected kwargs
        if kwargs:
            pass

    def serialize(self):
        # Basic serialization for top-level, simple attributes
        data = {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('_')}

        # Custom handling for complex attributes like 'address' and 'organisations'
        if hasattr(self, 'address') and callable(getattr(self.address, 'serialize', None)):
            data['address'] = self.address.serialize()
        if hasattr(self, 'organisations'):
            data['organisations'] = [company.serialize() for company in self.organisations if callable(getattr(company, 'serialize', None))]

        return data
from typing import List, Dict, Optional
import uuid


from .tapi_organisation_model import Organisation
from .tapi_address_model import Address
import app.domain.validation.tapi_user_validation as validator

class User:
    def __init__(
        self,
        user_reference:str,
        first_name: str,
        last_name: str,
        mobile_number: str,
        email: str,
        address: Address,
        companies: List[Organisation],
        notification_options: Dict,
        is_verified_email: bool,
        is_verified_phone: bool,
        is_active: bool,
        date_of_birth: Optional[str] = None,
        last_login_timestamp: Optional[str] = None,
        last_updated_timestamp: Optional[str] = None,
        updated_by_user_reference: Optional[uuid.UUID] = None,
        consent_preferences: Dict = None,
    ):
  
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_number = mobile_number
        self.email = email
        self.address = address
        self.companies = companies
        self.notification_options = notification_options
        self.is_verified_email = is_verified_email
        self.is_verified_phone = is_verified_phone
        self.is_active = is_active
        self.date_of_birth = date_of_birth
        self.last_login_timestamp = last_login_timestamp
        self.last_updated_timestamp = last_updated_timestamp
        self.updated_by_user_reference = updated_by_user_reference
        self.consent_preferences = consent_preferences or {}

        self.user_reference = user_reference
        self.full_name = f"{self.first_name}, {self.last_name}"

        validator.validate_non_empty_string(self.first_name, "First name")
        validator.validate_non_empty_string(self.last_name, "Last name")
        validator.validate_email_format(self.email)
        validator.validate_mobile_number_format(self.mobile_number)

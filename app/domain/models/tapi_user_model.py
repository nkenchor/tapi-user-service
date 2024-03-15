
import uuid
from typing import List, Dict
from .tapi_company_model import Company
from .tapi_address_model import Address

class User:
    """
    Represents a user, including personal information, security settings,
    notification preferences, roles, and permissions.
    """
    def __init__(
        self,
        user_reference: uuid.UUID,
        user_credential_reference: uuid.UUID,
        first_name: str,
        last_name: str,
        mobile_number: str,
        email: str,
        address: Address,
        companies: List[Company],
        roles: List[str],
        permissions: List[str],
        notification_options: Dict,  # Key-value pairs for user notification settings
        is_verified_email: bool,
        is_verified_phone: bool,
        is_active: bool,
    ):
        # Identification and Personal Information
        self.user_reference = user_reference
        self.user_credential_reference = user_credential_reference
        self.first_name = first_name
        self.last_name = last_name
        
        self.full_name = f"{self.first_name}, {self.last_name}"
        self.mobile_number = mobile_number
        self.email = email
        self.address = address

        # Company Affiliations
        self.companies = companies

        # Security and Access
        self.roles = roles
        self.permissions = permissions
        self.is_verified_email = is_verified_email
        self.is_verified_phone = is_verified_phone
        self.is_active = is_active

        # Preferences
        self.notification_options = notification_options

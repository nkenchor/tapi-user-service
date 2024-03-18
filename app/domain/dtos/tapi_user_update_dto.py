from dataclasses import dataclass, field, asdict
from typing import List, Optional
from app.domain.models.tapi_address_model import Address
from app.domain.models.tapi_organisation_model import Organisation
import app.domain.validation.tapi_user_validation as validator


@dataclass
class UserUpdateDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[Address] = None
    companies: Optional[List[Organisation]] = field(default_factory=list)
    is_active: Optional[bool] = None

    def __post_init__(self):
        validator.validate_non_empty_string(self.first_name, "First name")
        validator.validate_non_empty_string(self.last_name, "Last name")
        validator.validate_email_format(self.email)
        validator.validate_mobile_number_format(self.mobile_number)
        
    def to_dict(self):
        return asdict(self)

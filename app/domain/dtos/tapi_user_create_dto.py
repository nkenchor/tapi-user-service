
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from app.domain.models.tapi_address_model import Address
from app.domain.models.tapi_company_model import Company
from app.domain.models.tapi_permission_model import Permission
from app.domain.models.tapi_role_model import Role
import app.domain.validation.tapi_user_validation as validator

@dataclass
class UserCreateDTO:
    first_name: str
    last_name: str
    mobile_number: str
    email: str
    address: Optional[Address] = None
    companies: Optional[List[Company]] = field(default_factory=list)
    roles: Optional[List[Role]] = field(default_factory=list)
    permissions: Optional[List[Permission]] = field(default_factory=list)


    def __post_init__(self):
        validator.validate_non_empty(self.first_name, "First name")
        validator.validate_non_empty(self.last_name, "Last name")
        validator.validate_email_format(self.email)
        validator.validate_mobile_number_format(self.mobile_number)

    def to_dict(self):
        return asdict(self)


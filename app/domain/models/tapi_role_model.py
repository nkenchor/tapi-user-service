

from dataclasses import dataclass
from typing import Optional
import uuid
import app.domain.validation.tapi_user_validation as validator


@dataclass
class Role:
    role_reference: uuid.UUID
    role_name: str
    
    def __post_init__(self):
        validator.validate_non_empty(self.permission_reference, "role reference")
        validator.validate_non_empty(self.permission_name, "role name")
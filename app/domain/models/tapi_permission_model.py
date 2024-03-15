

from dataclasses import dataclass
from typing import Optional
import uuid
import app.domain.validation.tapi_user_validation as validator


@dataclass
class Permission:
    permission_reference: uuid.UUID
    permission_name: str

    def __post_init__(self):
        validator.validate_non_empty(self.permission_reference, "permission reference")
        validator.validate_non_empty(self.permission_name, "permission name")

from dataclasses import dataclass
import uuid
import app.domain.validation.tapi_user_validation as validator

@dataclass
class Company:
    company_reference: uuid.UUID
    company_name:str
    
    def __post_init__(self):
        validator.validate_non_empty(self.company_reference, "company reference")
        validator.validate_non_empty(self.company_name, "company name")
     
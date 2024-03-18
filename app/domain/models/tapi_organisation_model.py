import uuid
from app.domain.models.tapi_department_model import Department
import app.domain.validation.tapi_user_validation as validator

class Organisation:
    def __init__(self, organisation_reference: str, organisation_name: str, department: Department):
        self.organisation_reference = organisation_reference
        self.organisation_name = organisation_name
        self.department = department
        
        validator.validate_uuid_format(self.organisation_reference, "organisation reference")
        validator.validate_non_empty_string(self.organisation_reference, "organisation reference")
        validator.validate_non_empty_string(self.organisation_name, "organisation name")

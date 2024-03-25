
from app.domain.models.tapi_address_model import Address
from app.domain.models.tapi_department_model import Department
import app.domain.shared.shared_validation as validator

class Organisation:
    def __init__(self, organisation_reference: str, organisation_name: str, department: Department, address: Address):
        self.organisation_reference = organisation_reference
        self.organisation_name = organisation_name
        self.department = department if department is not None else {}
        self.address = address if address is not None else {}
        
        validator.validate_uuid_format(self.organisation_reference, "organisation reference")
        validator.validate_non_empty_string(self.organisation_reference, "organisation reference")
        validator.validate_non_empty_string(self.organisation_name, "organisation name")
        validator.validate_non_empty_string(self.department, "department")
        validator.validate_non_empty_string(self.address,"address")

    def serialize(self):
        return {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('_')}
    
    
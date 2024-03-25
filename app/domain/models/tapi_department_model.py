
import app.domain.shared.shared_validation as validator

class Department:
    def __init__(self, department_reference: str, department_name: str):
        self.department_reference = department_reference
        self.department_name = department_name
        
        validator.validate_uuid_format(self.department_reference, "department reference")
        validator.validate_non_empty_string(self.department_reference, "department reference")
        validator.validate_non_empty_string(self.department_name, "department name")

    def serialize(self):
        return {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('_')}

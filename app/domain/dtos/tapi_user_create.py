from dataclasses import asdict, dataclass
from datetime import datetime
import app.domain.shared.shared_validation as validator

@dataclass
class UserCreateDTO:
    def __init__(
        self,
        user_reference: str,
        email: str,
    ):
        # Generate a unique user reference
 
        # Direct validation without preliminary checks
        validator.validate_email_format(email)
        validator.validate_uuid_format(user_reference,"User Reference")

        # Consent preferences validation - ensure all values are boolean and required consents are provided
        self.user_reference = user_reference

        # Assign provided values with transformations where applicable
        self.email = email
        self.created_at_timestamp=datetime.now().isoformat()
        self.updated_at_timestamp=datetime.now().isoformat()
    
   

    def to_json(self):
        # Converts the UserCreateDTO and its nested objects to a dictionary
        return asdict(self)


import uuid
import app.domain.validation.tapi_user_validation as validator

class UserCreateDTO:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        mobile_number: str,
        email: str,
    ):
        self.user_reference = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_number = mobile_number
        self.email = email

        # Perform validation checks
        validator.validate_non_empty_string(self.first_name, "First name")
        validator.validate_non_empty_string(self.last_name, "Last name")
        validator.validate_email_format(self.email)
        validator.validate_mobile_number_format(self.mobile_number)

    def to_dict(self):
        # Converts the UserCreateDTO and its nested objects to a dictionary
        return {
            "user_reference": self.user_reference,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mobile_number": self.mobile_number,
            "email": self.email,
        }


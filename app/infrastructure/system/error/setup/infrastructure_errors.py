import json
from sanic import HTTPResponse
from app.domain.shared.shared_errors import CustomError, DomainError, ErrorType
import uuid
from datetime import datetime

class InfrastructureError:
    def __init__(self, error_type: ErrorType, message: str = "An error occurred.", errors: dict = None):
        # Direct instantiation with specific details
        self.error_reference = str(uuid.uuid4())
        self.error_type = error_type  # This should be an enum value
        self.errors = errors if errors else {"message":[message]}  # Additional errors or detail messages
        self.status_code = CustomError[error_type]
        self.timestamp = datetime.now().isoformat()

    @classmethod
    def from_domain_error(cls, domain_error: DomainError):
        """
        Alternative constructor for creating an instance from a DomainError.
        """
        return cls(
            error_type=domain_error.error_type,
            errors=domain_error.errors,  # Assuming DomainError has an errors list
         
        )

    def to_response(self) -> HTTPResponse:
        # Convert to a Sanic HTTPResponse
        error_details = {
            'error_reference': self.error_reference,
            'error_type': self.error_type.value if isinstance(self.error_type, ErrorType) else "Error",
            'errors': self.errors,
            'status_code': self.status_code,
            'timestamp': self.timestamp,
        }
        return HTTPResponse(
            status=self.status_code,
            body=json.dumps(error_details),
            content_type="application/json"
        )

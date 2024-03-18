import json
import uuid
from datetime import datetime
from enum import Enum
from sanic import HTTPResponse

# Enumeration of custom error types for consistent error handling across the application
class ErrorType(Enum):
    # Each error type corresponds to a specific kind of error that can occur within the application
    ValidationError = 'VALIDATION_ERROR'
    RedisSetupError = 'REDIS_SETUP_ERROR'
    NoRecordError = 'NO_RECORD_FOUND_ERROR'
    NotFound = 'NOT_FOUND_ERROR'
    CreateError = 'CREATE_ERROR'
    UpdateError = 'UPDATE_ERROR'
    LogError = 'LOG_ERROR'
    MongoDBError = 'MONGO_DB_ERROR'
    InvalidResource = 'INVALID_RESOURCE_ERROR'
    InvalidKey = 'INVALID_KEY_ERROR'
    InvalidUser = 'INVALID_User_ERROR'
    RedisError = 'REDIS_ERROR'
    BadRequestError = 'BAD_REQUEST_ERROR'
    ServerError = 'SERVER_ERROR'
    ConflictError = 'CONFLICT_ERROR'
    UnAuthorized = 'UNAUTHORIZED_ERROR'
    AuthenticationError = 'AUTHENTICATION_ERROR'
    ForbiddenError = 'FORBIDDEN_ERROR'
    RateLimitExceeded = 'RATE_LIMIT_EXCEEDED'
    PayloadTooLarge = 'PAYLOAD_TOO_LARGE'
    MethodNotAllowed = 'METHOD_NOT_ALLOWED'
    NotAcceptable = 'NOT_ACCEPTABLE'
    Timeout = 'TIMEOUT'
    UnsupportedMediaType = 'UNSUPPORTED_MEDIA_TYPE'
    PreconditionFailed = 'PRECONDITION_FAILED'
    TooManyRequests = 'TOO_MANY_REQUESTS'
    RequestHeaderFieldsTooLarge = 'REQUEST_HEADER_FIELDS_TOO_LARGE'
    InternalError = 'INTERNAL_ERROR'
    PaymentError = 'PAYMENT_ERROR'
    Prohibited = 'PROHIBITED_ERROR'

CustomError = {
    ErrorType.ValidationError: 400,
    ErrorType.RedisSetupError: 500,
    ErrorType.NoRecordError: 404,
    ErrorType.NotFound: 404,
    ErrorType.CreateError: 500,
    ErrorType.UpdateError: 500,
    ErrorType.LogError: 500,
    ErrorType.MongoDBError: 500,
    ErrorType.InvalidResource: 422,
    ErrorType.InvalidKey: 400,
    ErrorType.InvalidUser: 400,
    ErrorType.RedisError: 500,
    ErrorType.BadRequestError: 400,
    ErrorType.ServerError: 500,
    ErrorType.ConflictError: 409,
    ErrorType.UnAuthorized: 401,
    ErrorType.AuthenticationError: 401,
    ErrorType.ForbiddenError: 403,
    ErrorType.RateLimitExceeded: 429,
    ErrorType.PayloadTooLarge: 413,
    ErrorType.MethodNotAllowed: 405,
    ErrorType.NotAcceptable: 406,
    ErrorType.Timeout: 408,
    ErrorType.UnsupportedMediaType: 415,
    ErrorType.PreconditionFailed: 412,
    ErrorType.TooManyRequests: 429,
    ErrorType.RequestHeaderFieldsTooLarge: 431,
    ErrorType.InternalError: 500,
    ErrorType.PaymentError: 402,
    ErrorType.Prohibited: 451,
}


class ErrorResponse:
    def __init__(self, error_type: ErrorType, message: str):
        self.error_reference = str(uuid.uuid4())
        self.error_type = error_type
        self.time_stamp = datetime.now().isoformat()
        self.code = CustomError[error_type]
        self.errors = [message]

def error_message(error_type: ErrorType, message: str) -> ErrorResponse:
    return ErrorResponse(error_type, message)



class AppError(Exception):
    def __init__(self, error_type: ErrorType, message: str, errors: list = None):
        super().__init__(message)
        self.status_code = CustomError[error_type]
        self.error_type = error_type
        self.error_reference = str(uuid.uuid4())
        self.time_stamp = datetime.now().isoformat()
        # If a list of errors is provided, use it; otherwise, wrap the message in a list
        self.errors = errors if errors else [message]

    def to_json(self):
        # Convert error details into a JSON-serializable dictionary
        return {
            'statusCode': self.status_code,
            'errorType': self.error_type.value,
            'errorReference': self.error_reference,
            'timeStamp': self.time_stamp,
            'errors': self.errors,
        }

    def to_response(self) -> HTTPResponse:
        # Convert the AppError to a Sanic HTTPResponse
        return HTTPResponse(
            status=self.status_code,
            body=json.dumps({
                'errorReference': self.error_reference,
                'errorType': self.error_type.value,
                'errors': self.errors,
                'statusCode': self.status_code,
                'timeStamp': self.time_stamp,
              
            }),
            content_type="application/json"
        )
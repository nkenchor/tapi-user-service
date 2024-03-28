from textwrap import dedent

from sanic import Sanic


def setup_openapi(app: Sanic):
    app.ext.openapi.describe(
        title="Tidal User API",
        version="2.0.1",
        description=dedent(
            """
            # Tidal User API Documentation

            Welcome to the Tidal User API, a comprehensive solution for managing user data within our application. This API is designed to offer developers access to user-related operations, including creation, update, retrieval, and deletion of user records.

            ## Features

            - **Create Users**: Allows for the registration of new users, including essential information such as names, contact details, and credentials.
            - **Update Users**: Supports updating user details post-registration to keep user data current.
            - **Retrieve Users**: Provides mechanisms to fetch user details by unique identifiers or list all users with pagination support.
            - **Delete Users**: Enables the removal of users from the system, ensuring data privacy and compliance.

            ## Getting Started

            To begin using the Tidal User API, you'll need to authenticate using our OAuth2.0 endpoints. Each request must include a valid token in the `Authorization` header.

            ## Error Handling

            The API uses standard HTTP status codes to indicate the success or failure of requests. In the case of errors, a JSON response will detail the issue, including an error reference ID for support purposes.

            **MARKDOWN** is supported in this documentation, allowing for rich text formatting, including bold, italics, and code blocks for clearer communication.

            ### Example Error Response

            ```json
            {
                "error_reference": "unique-error-id-12345",
                "error_type": "VALIDATION_ERROR",
                "errors": ["Invalid email address"],
                "status_code": 400,
                "timestamp": "2024-03-25T10:30:00.000Z"
            }
            ```

            For further assistance or to report issues, please contact our support team at support@example.com.

            Enjoy building with the Tidal User API!
        """
        ),
    )

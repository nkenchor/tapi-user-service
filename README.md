# TAPI User Service

The TAPI User Service is an exemplary Python microservice that leverages the Sanic Framework's capabilities for asynchronous and non-blocking programming. This project aims to showcase the efficiency and scalability of using Sanic in building high-performance web applications. Adhering to the principles of Clean Architecture as outlined by Robert C. Martin, this service maintains a separation of concerns by organizing the code into distinct layers, thereby enhancing maintainability and testability.

This service also integrates with essential technologies such as MongoDB for persistence, Vault for secrets management, and Redis for caching and message brokering, making it a comprehensive example of a modern Python-based microservice.

## Installation

Follow these instructions to get the project up and running on your machine for development, testing, or production purposes.

### Prerequisites

Before installing the TAPI User Service, ensure you have the following installed on your system:

- Python 3.11.8 or higher
- MongoDB
- Vault
- Redis
- pyenv (recommended for managing Python versions)

### Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/nkenchor/tapi-user-service.git
cd tapi-user-service
```

### Python Environment Setup

It is recommended to use pyenv for managing the Python version. Install pyenv and set the local Python version:

```bash
pyenv install 3.11.8
pyenv local 3.11.8
```

### Virtual Environment

Create a virtual environment using pyenv and activate it:

```bash
pyenv virtualenv 3.11.8 tapi-user-service-env
pyenv activate tapi-user-service-env
```

### Install Dependencies

With the virtual environment activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

### MongoDB, Vault, and Redis Setup

Ensure that MongoDB, Vault, and Redis are installed and running on your system. The service requires these technologies to function properly:

- **MongoDB**: Follow the official MongoDB documentation to install and start the MongoDB server on your system.
- **Vault**: Install HashiCorp's Vault for secrets management and start the Vault server.
- **Redis**: Install and launch the Redis server for caching and message brokering.

### Configuration

Configure the service by setting the necessary environment variables or modifying the `config.py` file as needed. This includes database URIs, Vault connection settings, and Redis server details.

## Usage

To run the TAPI User Service, execute the following command in the root directory of the project:

```bash
python -m sanic app.app --host=0.0.0.0 --port=8000
```

This will start the Sanic server, making the service available on `localhost:8000`.

## Architecture

The TAPI User Service is designed around Clean Architecture principles, focusing on the separation of concerns into layers. The architecture is divided into the following core layers:

- **Domain Models**: The business objects of the application.
- **Use Cases and Interactors**: Application-specific business rules.
- **Interface Adapters**: Convert data between the most convenient form for use cases and entities to the most convenient form for external agencies such as databases and the web.
- **infrastructure**: External interfaces like databases, web frameworks, and UIs.

This organization ensures that business logic and application rules can be independent of UIs, databases, and other external elements, allowing for more flexible and maintainable code.

## Contributing

Contributions to the TAPI User Service are welcome. Please submit pull requests with clear descriptions of changes and updates. Ensure that your code adheres to the project's coding standards and includes tests where applicable.

## License

This project is licensed under [MIT License](LICENSE.md). Feel free to use, modify, and distribute the code as you see fit.

## Acknowledgments

- Sanic Framework for providing a powerful asynchronous web server and framework.
- MongoDB, Vault, and Redis for offering scalable and flexible solutions for persistence, secrets management, and caching/message brokering, respectively.
- Robert C. Martin for the Clean Architecture principles that guided the design of this service.
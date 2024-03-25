from sanic import Sanic

from app.infrastructure.web.controller.tapi_user_controller import UserController


def setup_routes(app: Sanic, user_controller: UserController):
    """
    Registers all endpoint routes for the application.

    :param app: The Sanic application instance.
    """

    # User routes
    app.add_route(user_controller.create_user, '/users', methods=['POST'])
    app.add_route(user_controller.update_user, '/users/<user_reference:str>', methods=['PUT'])
    app.add_route(user_controller.get_user_by_reference, '/users/<user_reference:str>', methods=['GET'])
    app.add_route(user_controller.get_all_users, '/users', methods=['GET'])  # Adjusted to not include <page:int> for simplicity
    app.add_route(user_controller.delete_user, '/users/<user_reference:str>', methods=['DELETE'])
    app.add_route(user_controller.get_current_user, '/users/current', methods=['GET'])

    # You can add more route setups here for other parts of your application

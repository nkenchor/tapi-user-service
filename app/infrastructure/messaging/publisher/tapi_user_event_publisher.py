from typing import Any
from app.application.events.event_publisher_interfaces.tapi_user_event_publisher_interface import (
    IUserEventPublisher,
)
from app.infrastructure.messaging.redis.setup.redis_setup import Redis
from app.infrastructure.messaging.redis.utils.helper.publish_helper import (
    PublisherHelper,
)


class RedisEventPublisher(IUserEventPublisher):
    def __init__(self, redis: Redis):
        self.redis_client = redis

    def publish_user_created_event(self, event_data: Any):
        PublisherHelper.publish("UserCreatedEvent", event_data)

    def publish_user_updated_event(self, event_data: Any):
        PublisherHelper.publish("UserUpdatedEvent", event_data)
    
    def publish_user_added_to_organisation_event(self, event_data: Any):
        PublisherHelper.publish("UserAddedToOrganisationEvent", event_data)

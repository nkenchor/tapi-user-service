# app/application/events/event_publisher_interface.py

from abc import ABC, abstractmethod
from typing import Any


class IUserEventPublisher(ABC):
    @abstractmethod
    def publish_user_created_event(self, event_data: Any):
        pass
    
    @abstractmethod
    def publish_user_updated_event(self, event_data: Any):
        pass

    @abstractmethod
    def publish_user_added_to_organisation_event(self, event_data: Any):
        pass

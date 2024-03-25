import json
from datetime import datetime
from typing import Any
import uuid

from app.infrastructure.system.configuration.configuration import Config

class Event:
    def __init__(self, event_name: str, 
                 event_type: str,event_user_reference: str, 
                 event_data: Any):
        self.event_reference = str(uuid.uuid4())
        self.event_name = event_name
        self.event_date = datetime.now().isoformat()  # Consider using datetime object for internal representation
        self.event_type = event_type
        self.event_source = Config.App_name
        self.event_user_reference = event_user_reference
        self.event_data = event_data  # Arbitrary data associated with the event

    def serialize(self) -> str:
        """Serializes the event to a JSON string."""
        event_dict = {
            'event_reference': self.event_reference,
            'event_name': self.event_name,
            'event_date': self.event_date,  # Assumes event_date is a string; consider formatting if datetime
            'event_type': self.event_type,
            'event_source': self.event_source,
            'event_user_reference': self.event_user_reference,
            # Event data serialization might require custom handling based on its structure
            'event_data': self.event_data if isinstance(self.event_data, (dict, list)) else str(self.event_data),
        }
        return json.dumps(event_dict)

    @staticmethod
    def deserialize(data: str):
        """Deserializes a JSON string back into an Event object."""
        obj = json.loads(data)
        return Event(
            event_reference=obj['event_reference'],
            event_name=obj['event_name'],
            event_date=obj['event_date'],
            event_type=obj['event_type'],
            event_source=obj['event_source'],
            event_user_reference=obj['event_user_reference'],
            event_data=obj['event_data'],  # Further parsing may be required based on expected structure
        )
from dataclasses import dataclass, asdict
from datetime import datetime
from app.domain.models.tapi_organisation_model import Organisation


@dataclass
class UserAddOrganisationDTO:
    def __init__(
        self,
        organisation: Organisation,
    ):
        # Generate a unique user reference


        self.organisation = organisation
        self.updated_at_timestamp=datetime.now().isoformat()
    

    def to_json(self):
        # Use asdict to convert all fields, including Optional ones, to a dictionary
        return asdict(self)


@dataclass
class UserRemoveOrganisationDTO:
    def __init__(
        self,
        organisation_reference: str,
    ):
        # Generate a unique user reference


        self.organisation_reference = organisation_reference
        self.updated_at_timestamp=datetime.now().isoformat()
    

    def to_json(self):
        # Use asdict to convert all fields, including Optional ones, to a dictionary
        return asdict(self)



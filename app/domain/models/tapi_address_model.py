
from dataclasses import dataclass
from typing import Optional
import app.domain.validation.tapi_user_validation as validator


@dataclass
class Address:
    house_name_or_number: str
    address_line_1: str
    address_line_2: Optional[str] = None
    street:str
    city :str
    county :str
    postcode: str
    country: str
    
    
    def __post_init__(self):
        validator.validate_non_empty(self.house_name_or_number, "house name or number")
        validator.validate_non_empty(self.address_line_1, "address line 1")
        validator.validate_non_empty(self.street, "street")
        validator.validate_non_empty(self.city, "city")
        validator.validate_non_empty(self.county, "county")
        validator.validate_non_empty(self.postcode, "post Code")
        validator.validate_non_empty(self.country, "country")
        
   
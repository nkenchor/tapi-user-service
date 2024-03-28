
import app.domain.shared.shared_validation as validator


class Address:
    def __init__(
        self,
        house_name_or_number: str,
        address_line_1: str,
        city: str,
        county: str,
        postcode: str,
        country: str,
        street: str,
        address_line_2: str,
    ):
        self.house_name_or_number = house_name_or_number
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.county = county
        self.postcode = postcode
        self.country = country
        self.street = street
       
        
        validator.validate_non_empty_string(self.house_name_or_number, "house name or number")
        validator.validate_non_empty_string(self.address_line_1, "address line 1")
        
        validator.validate_non_empty_string(self.street, "street")
        if self.address_line_2 is not None or not "":
            validator.validate_non_empty_string(self.address_line_2, "address line 2")
        validator.validate_non_empty_string(self.city, "city")
        validator.validate_non_empty_string(self.county, "county")
        validator.validate_non_empty_string(self.postcode, "post Code")
        validator.validate_non_empty_string(self.country, "country")

    def to_json(self):
        return {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('_')}

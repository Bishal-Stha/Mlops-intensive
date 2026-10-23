from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allegies: List[str]
    email:EmailStr
    contact_details: Dict[str,str]

    @field_validator("email")
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['nabil.com','nicasia.com']
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")

        return value

patient_info = {"name":"Bishal","age":20,"weight":90.5,"email":"bishal@gmail.com"}

patient1 = Patient(**patient_info)
print(patient1)
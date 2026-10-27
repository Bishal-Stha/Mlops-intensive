from pydantic import BaseModel, field_validator, computed_field, Field
from typing import Annotated, Literal
from config.city_teir import tier_1_cities, tier_2_cities

# Pydantic Model to validate incoming data
class UserInput(BaseModel):
    age: Annotated[int, Field(...,gt=0,lt=120, description="Age of the user")]
    weight: Annotated[float, Field(...,gt=0, description="Weight of the user")]
    height: Annotated[float, Field(...,gt=0,lt=2.5, description="Height of the user in Meter")]
    income_lpa: Annotated[float, Field(...,gt=0, description="Annual slary of the user in LPA")]
    smoker: Annotated[bool, Field(..., description="Is user a smoker")]
    city: Annotated[str, Field(...,description="the city user belongs to")]
    occupation: Annotated[ Literal['retired','freelancer','student','government_job','business_owner','unemployed','private_job'] , Field(..., description="User's occupation")]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height **2),2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:

        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

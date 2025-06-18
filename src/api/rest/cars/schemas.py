from pydantic import BaseModel


class CarSchema(BaseModel):
    name: str
    mileage: int

    class Config:
        json_schema_extra = {
            "example":
            {
                "name": "verna",
                "mileage": 134_200, 
            }
        }

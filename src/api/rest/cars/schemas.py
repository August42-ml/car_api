from pydantic import BaseModel


class CarSchema(BaseModel):
    id: int
    name: str
    mileage: int

    class Config:
        json_schema_extra = {
            "example":
            {
                "id": 0,
                "name": "verna",
                "mileage": 134_200, 
            }
        }

from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional

class Car(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    year: int
    gearbox: str = Field(regex='^(акпп|мкпп)$')
    mileage: int
    #все пробеги для каждого расходника
    mileage_for_gearbox_oil: int
    mileage_for_engine_oil: int
    mileage_for_engine_belts_and_timing: int
    mileage_for_antifreeze_liquid: int
    mileage_for_air_engine_filter: int
    mileage_for_air_cabin_filter: int
    mileage_for_spark_plug: int
    #марки жидкостей
    gearbox_oil: str
    engine_oil: str
    #следующая замена расходников
    next_gearbox_oil_swap: int
    next_engine_oil_swap: int
    next_engine_belts_and_timing_swap: int
    next_antifreeze_liquid_swap: int
    next_air_engine_filter_swap: int
    next_air_cabin_filter_swap: int
    next_spark_plug_swap: int

    class Config:
        json_schema_extra = {
            "example":
            {
                "name": "verna",
                "year": 2006,
                "gearbox": "акпп",
                "mileage": 134_200, 
                "mileage_for_gearbox_oil": 7_000,
                "mileage_for_engine_oil": 35_000,
                "mileage_for_engine_belts_and_timing": 50_000,
                "mileage_for_antifreeze_liquid": 45_000,
                "mileage_for_air_engine_filter": 10_000,
                "mileage_for_air_cabin_filter": 15_000,
                "mileage_for_spark_plug": 15_000,
                "gearbox_oil": "ATF SP III 4л.",
                "engine_oil": "5W40 TEBOIL GOLD S"
            }
        }

class Service(SQLModel, table=True):
    id: int = Field(primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    mileage: int
    date: str = Field(regex='[0-9]{2}/[0-9]{2}/[0-9]{4}')
    #контроль замены основных расходников
    gearbox_oil_changing: bool = Field(default=False)
    engine_oil_changing: bool = Field(default=False)
    engine_belts_and_timing_changing: bool = Field(default=False)
    antifreeze_liquid_changing: bool = Field(default=False)
    mileage_for_spark_plug_changing: bool = Field(default=False)
    comment: str = Field(default="Добавлено без комментария")
    total_price: int

    class Config:
        json_schema_extra = {
            "example":
            {
                "car_id": 1,
                "gearbox_oil_changing": True,
                "comment": "Починил омывайку", 
                "mileage": 136_000,
                "total_price": 12_000,
                "date": "29/05/2025"   
            }
        }

class Detail(SQLModel, table=True):
    id: int = Field(primary_key=True)
    #так как деталь может быть поменята мной, то в заезде на СТО нет необходимости
    service_id: Optional[int] = Field(default=None, foreign_key="service.id")
    car_id: int = Field(foreign_key="car.id")
    gain_date: str = Field(regex='[0-9]{2}/[0-9]{2}/[0-9]{4}')
    quantity: int
    name: str
    price_per_unit: int

    class Config:
        json_schema_extra = {
            "example":
            {
                "service_id": 1,
                "car_id": 1,
                "quantity": 2,
                "name": "Левая рулевая тяга",
                "price_per_unit": 3_000,
                "gain_date": "29/05/2025"
            }
        }

class DetailToAdd(BaseModel):
    quantity: int
    gain_date: str = Field(regex='[0-9]{2}/[0-9]{2}/[0-9]{4}')
    name: str
    price_per_unit: int 

    class Config:
        json_schema_extra = {
            "example":
            {   
                "quantity": 2,
                "gain_date": "29/05/2025",
                "name": "Левая рулевая тяга",
                "price_per_unit": 3_000
            }
        }

class DetailsToAdd(BaseModel):
    details: list[DetailToAdd]

    class Config:
        json_schema_extra = {
            "example": { 
                "details":  [
                        {   
                        "quantity": 2,
                        "name": "Левая рулевая тяга",
                        "price_per_unit": 3_000,
                        "gain_date": "29/05/2025"
                        }, 

                        {   
                        "quantity": 1,
                        "name": "Тормозные колодки",
                        "price_per_unit": 2_000,
                        "gain_date": "29/05/2025"
                        } 
                ]
            }
        }

class DetailToChange(BaseModel):
    name: str = Field(regex='^(фильтр салона|фильтр двигателя)$')

    class Config:
        json_schema_extra = {
            "example":
            {
                "name": "фильтр салона"
            }
        }

class DetailsToChange(BaseModel):
    details: list[DetailToChange]

    class Config:
        json_schema_extra = {
            "example":
            {
                "details": [

                    {
                        "name": "фильтр салона"
                    },
                    {
                        "name": "фильтр двигателя"
                    }
                ]
            }
        }
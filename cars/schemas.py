from pydantic import BaseModel


class Car(BaseModel):
    id: int 
    name: str
    year: int
    gearbox: str
    mileage: int
    #все пробеги для каждого расходника
    # mileage_for_gearbox_oil: int
    # mileage_for_engine_oil: int
    # mileage_for_engine_belts_and_timing: int
    # mileage_for_antifreeze_liquid: int
    # mileage_for_air_engine_filter: int
    # mileage_for_air_cabin_filter: int
    # mileage_for_spark_plug: int
    # #марки жидкостей
    # gearbox_oil: str
    # engine_oil: str
    # #следующая замена расходников
    # next_gearbox_oil_swap: int
    # next_engine_oil_swap: int
    # next_engine_belts_and_timing_swap: int
    # next_antifreeze_liquid_swap: int
    # next_air_engine_filter_swap: int
    # next_air_cabin_filter_swap: int
    # next_spark_plug_swap: int

    class Config:
        json_schema_extra = {
            "example":
            {
                "id": 1,
                "name": "verna",
                "year": 2006,
                "gearbox": "акпп",
                "mileage": 134_200, 
            }
        }


                # "mileage_for_gearbox_oil": 7_000,
                # "mileage_for_engine_oil": 35_000,
                # "mileage_for_engine_belts_and_timing": 50_000,
                # "mileage_for_antifreeze_liquid": 45_000,
                # "mileage_for_air_engine_filter": 10_000,
                # "mileage_for_air_cabin_filter": 15_000,
                # "mileage_for_spark_plug": 15_000,
                # "gearbox_oil": "ATF SP III 4л.",
                # "engine_oil": "5W40 TEBOIL GOLD S"
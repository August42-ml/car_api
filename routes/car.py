from fastapi import APIRouter, Body, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import select
from typing import Optional

from models.car import Car, Service, Detail, DetailsToAdd, DetailsToChange
from database.connection import get_session
from .notification import send_warning_by_bot

car_router = APIRouter(tags=["Cars"])

@car_router.post("/add_car")
async def add_car(car: Car = Body(...), session = Depends(get_session)) -> dict:
    #подсчет пробега, для замены расходников
    car.next_gearbox_oil_swap = car.mileage + car.mileage_for_gearbox_oil
    car.next_engine_oil_swap = car.mileage + car.mileage_for_engine_oil
    car.next_engine_belts_and_timing_swap = car.mileage + car.mileage_for_engine_belts_and_timing
    car.next_antifreeze_liquid_swap = car.mileage + car.mileage_for_antifreeze_liquid
    car.next_air_engine_filter_swap = car.mileage + car.mileage_for_air_engine_filter
    car.next_air_cabin_filter_swap = car.mileage + car.mileage_for_air_cabin_filter
    car.next_spark_plug_swap = car.mileage + car.mileage_for_spark_plug
    session.add(car)
    session.commit()
    return {"msg": "Car was added succesfully"}

@car_router.get("/{car_name}")
async def get_car_by_name(car_name: str, session = Depends(get_session)) -> Car:
    statement = select(Car).where(Car.name==car_name)
    car = session.exec(statement).first()
    if car:
        return car    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have this car in your car list")

@car_router.put("/{car_name}/change_mileage")
async def change_mileage(background_tasks: BackgroundTasks, mileage: int, car_name: str, session = Depends(get_session)) -> dict:
    car = await get_car_by_name(car_name=car_name, session=session)
    session.add(car)
    car.mileage = mileage
    car_instance_for_background = Car(**car.dict())
    session.commit()
    background_tasks.add_task(check_mileage_for_details, car_instance_for_background)
    return {"msg": "Car's mileage was changed succesfully"}


@car_router.put("/{car_name}/change_mileage_detail")
async def change_mileage_for_detail(car_name: str, details_to_change: DetailsToChange, session=Depends(get_session)) -> dict:
    car = await get_car_by_name(car_name=car_name, session=session)
    session.add(car)
    details = details_to_change.details
    for detail in details:
        if detail.name == "фильтр салона":
            car.next_air_cabin_filter_swap = car.next_air_cabin_filter_swap = car.mileage + car.mileage_for_air_cabin_filter
        if detail.name == "фильтр двигателя":
            car.next_air_engine_filter_swap = car.mileage + car.mileage_for_air_engine_filter
    session.commit()
    session.close()
    return {"msg": "Mileage for your details was chenged succesfully"}

@car_router.post("/{car_name}/add_details")
async def add_details(car_name: str, details_to_add: DetailsToAdd = Body(...), session = Depends(get_session), service_id: Optional[int] = None) -> dict:
    car = await get_car_by_name(car_name=car_name, session=session)
    details = details_to_add.details
    for detail in details:
        if service_id:
            detail = Detail(car_id=car.id, service_id=service_id, quantity=detail.quantity, name=detail.name, price_per_unit=detail.price_per_unit, gain_date=detail.gain_date)
        else:
            detail = Detail(car_id=car.id, quantity=detail.quantity, name=detail.name, price_per_unit=detail.price_per_unit, gain_date=detail.gain_date)
        session.add(detail)
    session.commit()
    return {"msg": "Detail was added succesfully"}

@car_router.post("/{car_name}/add_services")
async def add_service(car_name: str, car_services: Service = Body(...), details_to_add: DetailsToAdd = Body(...), session = Depends(get_session)) -> dict:
    car = await get_car_by_name(car_name=car_name, session=session)
    session.add(car)
    session.add(car_services)
    car.mileage = car_services.mileage

    if car_services.gearbox_oil_changing:
        car.next_gearbox_oil_swap = car.mileage + car.mileage_for_gearbox_oil
    if car_services.engine_oil_changing:
        car.next_engine_oil_swap = car.mileage + car.mileage_for_engine_oil
    if car_services.engine_belts_and_timing_changing:
        car.next_engine_belts_and_timing_swap = car.mileage + car.mileage_for_engine_belts_and_timing
    if car_services.antifreeze_liquid_changing:
        car.next_antifreeze_liquid_swap = car.mileage + car.mileage_for_antifreeze_liquid
    if car_services.mileage_for_spark_plug_changing:
        car.next_spark_plug_swap = car.mileage + car.mileage_for_spark_plug
      
    await add_details(car_name=car_name, details_to_add=details_to_add, service_id=car_services.id, session=session) # тут сеанс коммитнится
    session.close()
    return {"msg": "Car changes was writen succesfully"}

@car_router.get("/{car_name}/outcomes")
async def get_outcome_info(car_name: str, session = Depends(get_session)) -> dict:
    car = await get_car_by_name(car_name=car_name, session=session)

    #запчасти, которые покупал сам
    details_on_my_own_statement = select(Detail).where(Detail.car_id==car.id and Detail.service_id==None)
    details_on_my_own = session.exec(details_on_my_own_statement).all()

    services_statemnet = select(Service).where(Service.car_id==car.id)
    services = session.exec(services_statemnet).all()

    details_outcomes, service_outcomes = 0, 0
    for detail in details_on_my_own:
        details_outcomes += detail.price_per_unit * detail.quantity
    for service in services:
        details_current_service_statement = select(Detail).where(Detail.car_id==car.id and Detail.service_id==service.id)
        details_current_service = session.exec(details_current_service_statement).all()
        for detail_current_service in details_current_service:
            details_outcomes_current_service = detail_current_service.price_per_unit * detail_current_service.quantity
            details_outcomes += details_outcomes_current_service
        service_outcomes += service.total_price - details_outcomes_current_service

    session.close()
    return {"Total outcomes for details": details_outcomes, "Total outcomes for service": service_outcomes, "total_outcomes": details_outcomes + service_outcomes}

async def check_mileage_for_details(car: Car) -> None:
    summary = ""
    summary += await make_summary(car.mileage, car.next_engine_oil_swap, "engine oil")
    summary += await make_summary(car.mileage, car.next_gearbox_oil_swap, "gearbox oil")
    summary += await make_summary(car.mileage, car.next_engine_belts_and_timing_swap, "engine belts and timmig")
    summary += await make_summary(car.mileage, car.next_antifreeze_liquid_swap, "antifreeze liquid")
    summary += await make_summary(car.mileage, car.next_air_cabin_filter_swap, "air cabin filter")
    summary += await make_summary(car.mileage, car.next_air_engine_filter_swap, "air engine filter")
    summary += await make_summary(car.mileage, car.next_spark_plug_swap, "spark plugs")
    if not summary:
       await send_warning_by_bot(warning=f"{car.name}'s details are good")
    await send_warning_by_bot (warning=summary)


async def make_summary(current_mileage: int, mileage_to_swap: int, detail: str) -> str | None:
    if mileage_to_swap <= current_mileage:
         return f"Need to swap {detail}: mileage with this one without swapping is {current_mileage - mileage_to_swap}\n"
    return ''


    





    



from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import Car
from .service import car_service
from .exception import CarAlreadyExistsError, CarDoesNotExistError

car_router = APIRouter(prefix="/cars", tags=["Cars"])

@car_router.post("/add")
def add_car(car: Car) -> dict:
    try:
        car_service.add(car)
    except CarAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {"msg": "Car was added successfully"}

@car_router.get("/{car_id}")
def get_car(car_id: int) -> Car:
    try:
        return car_service.get(car_id)
    except CarDoesNotExistError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    

@car_router.put("/{car_id}")
def update_car(car_id: int, car: Car) -> dict:
    try:
        car_service.update(car_id, car)
    except CarDoesNotExistError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {"msg": "Car was updated successfully"}

@car_router.delete("/{car_id}")
def delete_car(car_id: int) -> dict:
    try:
        car_service.delete(car_id)
    except CarDoesNotExistError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    return {"msg": "Car was deleted successfully"}
    


    #подсчет пробега, для замены расходников
    # car.next_gearbox_oil_swap = car.mileage + car.mileage_for_gearbox_oil
    # car.next_engine_oil_swap = car.mileage + car.mileage_for_engine_oil
    # car.next_engine_belts_and_timing_swap = car.mileage + car.mileage_for_engine_belts_and_timing
    # car.next_antifreeze_liquid_swap = car.mileage + car.mileage_for_antifreeze_liquid
    # car.next_air_engine_filter_swap = car.mileage + car.mileage_for_air_engine_filter
    # car.next_air_cabin_filter_swap = car.mileage + car.mileage_for_air_cabin_filter
    # car.next_spark_plug_swap = car.mileage + car.mileage_for_spark_plug
    # session.add(car)
    # session.commit()
    # session.close()
    # return {"msg": "Car was added succesfully"}

# @car_router.get("/{car_name}")
# async def get_car_by_name(car_name: str, session = Depends(get_session)) -> Car:
#     statement = select(Car).where(Car.name==car_name)
#     car = session.exec(statement).first()
#     if car:
#         return car    
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have this car in your car list")

# @car_router.patch("/{car_name}/change_mileage")
# async def change_mileage(mileage: int, car_name: str, session = Depends(get_session)) -> dict:
#     car = await get_car_by_name(car_name=car_name, session=session)
#     session.add(car)
#     car.mileage = mileage
#     session.commit()
#     session.close()
#     return {"msg": "Car's mileage was changed succesfully"}

# #REMAKE FOR ALL DETAILS
# @car_router.patch("/{car_name}/change_mileage_detail")
# async def change_mileage_for_detail(car_name: str, details_to_change: DetailsToChange, session=Depends(get_session)) -> dict:
#     car = await get_car_by_name(car_name=car_name, session=session)
#     session.add(car)
#     details = details_to_change.details
#     for detail in details:
#         if detail.name == "фильтр салона":
#             car.next_air_cabin_filter_swap = car.next_air_cabin_filter_swap = car.mileage + car.mileage_for_air_cabin_filter
#         if detail.name == "фильтр двигателя":
#             car.next_air_engine_filter_swap = car.mileage + car.mileage_for_air_engine_filter
#     session.commit()
#     session.close()
#     return {"msg": "Mileage for your details was chenged succesfully"}

# # quantity=detail.quantity, name=detail.name, price_per_unit=detail.price_per_unit, gain_date=detail.gain_date
# @car_router.post("/{car_name}/add_details")
# async def add_details(car_name: str,
#                         details_to_add: DetailsToAdd = Body(...),
#                         session = Depends(get_session),
#                         service_id: Optional[int] = None,
#                         car_id: Optional[int] = None) -> dict:
#     details = details_to_add.details

#     if car_id:
#         for detail in details:
#             detail = Detail(car_id=car_id, service_id=service_id, **detail.dict())
#             session.add(detail)
#         session.commit()
#     else:
#         car = await get_car_by_name(car_name=car_name, session=session)
#         for detail in details:
#             detail = Detail(car_id=car.id, **detail.dict())
#             session.add(detail)
#         session.commit()
#         session.close()

#     return {"msg": "Detail was added succesfully"}

# @car_router.post("/{car_name}/add_services")
# async def add_service(car_name: str,
#                         car_services: Service = Body(...),
#                         details_to_add: DetailsToAdd = Body(...),
#                         session = Depends(get_session)) -> dict:
#     car = await get_car_by_name(car_name=car_name, session=session)

#     session.add(car)
#     session.add(car_services)
#     car.mileage = car_services.mileage

#     #обновляем пробеги расходников, если меняли
#     if car_services.gearbox_oil_changing:
#         car.next_gearbox_oil_swap = car.mileage + car.mileage_for_gearbox_oil
#     if car_services.engine_oil_changing:
#         car.next_engine_oil_swap = car.mileage + car.mileage_for_engine_oil
#     if car_services.engine_belts_and_timing_changing:
#         car.next_engine_belts_and_timing_swap = car.mileage + car.mileage_for_engine_belts_and_timing
#     if car_services.antifreeze_liquid_changing:
#         car.next_antifreeze_liquid_swap = car.mileage + car.mileage_for_antifreeze_liquid
#     if car_services.mileage_for_spark_plug_changing:
#         car.next_spark_plug_swap = car.mileage + car.mileage_for_spark_plug
        
#     session.commit()
#     await add_details(car_name=car_name, details_to_add=details_to_add, service_id=car_services.id, session=session, car_id=car.id) # тут сеанс коммитнится
#     session.close()
#     return {"msg": "Car changes was writen succesfully"}

# @car_router.get("/{car_name}/outcomes")
# async def get_outcome_info(car_name: str, session = Depends(get_session)) -> OutcomesSummary:
#     car = await get_car_by_name(car_name=car_name, session=session)

#     #запчасти, которые покупал сам
#     details_on_my_own_statement = select(Detail).where(Detail.car_id==car.id and Detail.sersvice_id==None)
#     details_on_my_own = session.exec(details_on_my_own_statement).all()

#     services_statemnet = select(Service).where(Service.car_id==car.id)
#     services = session.exec(services_statemnet).all()

#     details_outcomes, service_outcomes = 0, 0
#     for detail in details_on_my_own:
#         details_outcomes += detail.price_per_unit * detail.quantity
#     for service in services:
#         details_current_service_statement = select(Detail).where(Detail.car_id==car.id and Detail.service_id==service.id)
#         details_current_service = session.exec(details_current_service_statement).all()
#         for detail_current_service in details_current_service:
#             details_outcomes_current_service = detail_current_service.price_per_unit * detail_current_service.quantity
#             details_outcomes += details_outcomes_current_service
#         service_outcomes += service.total_price - details_outcomes_current_service

#     session.close()

#     total_outcomes = service_outcomes + details_outcomes
#     return OutcomesSummary(total_outcomes=total_outcomes, service_outcomes=service_outcomes, details_outcomes=details_outcomes)

# @car_router.get('/{car_name}/check_detail_mileage')
# async def check_mileage_for_details(car_name: str, session = Depends(get_session)) -> DetailsMileageSummary:
#     car = await get_car_by_name(car_name=car_name, session=session)
    
#     summary = DetailsMileageSummary(
#                                 engine_oil_mileage_left=car.next_engine_oil_swap - car.mileage,
#                                 gearbox_oil_mileage_left=car.next_gearbox_oil_swap - car.mileage,
#                                 engine_belts_and_timmig_mileage_left=car.next_engine_belts_and_timing_swap - car.mileage,
#                                 antifreeze_liquid_mileage_left=car.next_antifreeze_liquid_swap - car.mileage,
#                                 air_cabin_filter_mileage_left=car.next_air_cabin_filter_swap - car.mileage,
#                                 air_engine_filter_mileage_left=car.next_air_engine_filter_swap - car.mileage,
#                                 spark_plugs_mileage_left=car.next_spark_plug_swap - car.mileage)
#     return summary

    





    



from fastapi import HTTPException, status
from typing import List
from . import models
from datetime import datetime


async def create_new_address(request, database, current_user) -> models.Address:
    new_address = models.Address(shipping_address=request.shipping_address,
                                 user_id=current_user.id, created_date=datetime.now())
    database.add(new_address)
    database.commit()
    database.refresh(new_address)
    return new_address


async def add_bulk_address(request, database, current_user) -> List[models.Address]:

    # objects = []
    # for address in request:
    #     db_item = models.Address(shipping_address=address.shipping_address,
    #                              user_id=current_user.id, created_date=datetime.now())
    #     objects.append(db_item)

    # database.bulk_save_objects(objects)
    # database.commit()
    # database.refresh(objects)
    return "jumbo"


async def get_address_listing(database) -> List[models.Address]:
    addresses = database.query(models.Address).all()
    return addresses


async def get_address_by_id(address_id, user_id, database):
    address = database.query(models.Address).filter_by(
        id=address_id, user_id=user_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address Not Found !"
        )
    return address


async def delete_address_by_id(address_id, user_id, database):
    database.query(models.Address).filter(
        models.Address.id == address_id and models.Address.user_id == user_id).delete()
    database.commit()


async def update_address_by_id(request, address_id, user_id, database):
    address = database.query(models.Address).filter_by(
        id=address_id, user_id=user_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address Not Found !"
        )
    address.shipping_address = request.shipping_address if request.shipping_address else address.shipping_address
    database.commit()
    database.refresh(address)
    return address

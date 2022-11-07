from typing import List
from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.orm import Session
from account.jwt import get_current_user
from account.models import Account

import db

from .import schema
from .import services


router = APIRouter(
    tags=["Address"],
    prefix='/address'
)


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schema.AddressBase)
async def create_new_address(request: schema.AddressBase, database: Session = Depends(db.get_db), 
    current_user: Account = Depends(get_current_user)):
    user = database.query(Account).filter(Account.email == current_user.email).first()
    result = await services.create_new_address(request, database, user)
    return result


@router.post('/multi', status_code=status.HTTP_201_CREATED)
async def create_multiple_addresses(data, database: Session = Depends(db.get_db)):
    # user = database.query(Account).filter(Account.email == current_user.email).first()
    # result = await services.add_bulk_address(request.addresses, database, user)
    print(data)
    return 'jumbo doc'


@router.get('/', status_code=status.HTTP_200_OK,
            response_model=List[schema.AddressList])
async def address_list(database: Session = Depends(db.get_db),
                      current_user: Account = Depends(get_current_user)):
    result = await services.get_address_listing(database)
    return result


@router.get('/{address_id}', status_code=status.HTTP_200_OK, response_model=schema.AddressBase)
async def get_address_by_id(address_id: int, database: Session = Depends(db.get_db),
                                current_user: Account = Depends(get_current_user)):                            
    return await services.get_address_by_id(address_id, current_user.id, database)


@router.delete('/{address_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_address_by_id(address_id: int,
                                database: Session = Depends(db.get_db),
                                current_user: Account = Depends(get_current_user)):
    return await services.delete_address_by_id(address_id, current_user.id, database)


@router.patch('/{address_id}', status_code=status.HTTP_200_OK, response_model=schema.AddressBase)
async def update_address_by_id(request: schema.AddressUpdate, address_id: int, database: Session = Depends(db.get_db),
                                current_user: Account = Depends(get_current_user)):                            
    return await services.update_address_by_id(request, address_id, current_user.id, database)

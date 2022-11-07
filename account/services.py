from fastapi import HTTPException, status
from typing import List, Optional

from . import schema
from . import models


async def new_user_register(request: schema.Account, database) -> models.Account:

    new_user = models.Account(username=request.username, email=request.email,
                           password=request.password,
                           firstName=request.firstName,
                           lastName=request.lastName)
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


async def all_users(database) -> List[models.Account]:
    users = database.query(models.Account).all()
    return users


async def get_user_by_id(user_id, database) -> Optional[models.Account]:
    user_info = database.query(models.Account).get(user_id)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found!"
        )

    return user_info


async def get_profile(database, current_user) -> models.Account:
    user = database.query(models.Account).filter(models.Account.email == current_user.email).first()
    return user


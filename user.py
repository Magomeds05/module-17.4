from fastapi import APIRouter
from fastapi import APIRouter, Depends, status, HTTPException
from backend.db_depends import get_db
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from user2 import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)],
                     user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        return user
    raise HTTPException(status_code=404, detail="User was not found")

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)],
                      user_create_model: CreateUser):
    db.execute(insert(User).values(username = user_create_model.username,
                                   firstname = user_create_model.firstname,
                                   lastname = user_create_model.lastname,
                                   age = user_create_model.age,
                                   slug = slugify(user_create_model.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)],
                      update_user: UpdateUser, user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(
        username=update_user.username,
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age,
        slug=slugify(update_user.username)))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      delete_user: UpdateUser, user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(
        username=update_user.username,
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age,
        slug=slugify(update_user.username)))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}




#В модуле user.py напишите APIRouter с префиксом '/user' и тегом 'user', а также следующие маршруты, с пустыми функциями:
#get '/' с функцией all_users.
#g#et '/user_id' с функцией user_by_id.
#post '/create' с функцией create_user.
#put '/update' с функцией update_user.
#delete '/delete' с функцией delete_user.
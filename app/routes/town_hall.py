from fastapi import APIRouter, status
from app.config.queries import *
from app.config.functions import response_modelx
from app.core.modules import UsersManager
from app.schemas.schemas import KeyUser, ResponseModel, SubKeyUser, SubUserCreate, TownHallCreate, UserModel, UserCreate, UserSignIn
from app.core.security.hashing import HashingManager


twn_hall_router= APIRouter()


@twn_hall_router.post("/register", response_model=UserModel)
async def admin_register_town_hall(town_hall: TownHallCreate):
    if not town_hall.user_token or not town_hall.title or not town_hall.description or not town_hall.community or not town_hall.email:
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
    
    #>> Obtiene los datos del owner-usuario mediante el keyuser.
    res_get_keyuser = await query_authenticate_keyuser(town_hall.user_token)
    if res_get_keyuser.error is True:
        return response_modelx(res_get_keyuser.status, True, res_get_keyuser.message, None)
    
    #>> Obtiene datos importantes del owner-usuario desde User.
    res_get_user= await query_get_user_by_userid_or_username(res_get_keyuser.res.user_id)
    if res_get_user.error is True:
        return response_modelx(res_get_user.status, True, res_get_user.message, None)
    
    #>> Verify the user is authorized
    if not await UsersManager().user_is_active(res_get_user.res):
        return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "El usuario esta inactivo.", None)
    
    #>> Verify the user is authorized as owner or admin
    if not await UsersManager().user_is_owner(res_get_user.res) or not await UsersManager().user_is_admin(res_get_user.res):
        return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "El usuario no esta autorizado para acceder a este recurso.", None)
    
    res_insert_town_hall = await query_insert_new_town_hall(town_hall)
    if res_insert_town_hall.error is True:
        return response_modelx(res_insert_town_hall.status, True, res_insert_town_hall.message, None)
    
    return response_modelx(status.HTTP_200_OK, False, "Se ha registrado el nuevo town hall exitosamente.", None)



@twn_hall_router.get("/get_all")
async def get_all_town_hall():
    res_get_all_town_hall = await query_get_all_town_hall()
    if res_get_all_town_hall.error is True:
        return response_modelx(res_get_all_town_hall.status, True, res_get_all_town_hall.message, None)
    
    return response_modelx(status.HTTP_200_OK, False, "Ayuntamientos obtenidas exitosamente.", res_get_all_town_hall.res)


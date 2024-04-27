from fastapi import APIRouter, status
from app.config.queries import *
from app.config.functions import response_modelx
from app.core.modules import UsersManager
from app.schemas.schemas import KeyUser, ResponseModel, SubKeyUser, SubUserCreate, UserModel, UserCreate, UserSignIn
from app.core.security.hashing import HashingManager


user_router = APIRouter()


#region: Me and SignIn
@user_router.post("/me", response_model=UserInternalData)
async def get_me(user: KeyUser):
    try:
        if not user.user_token:
            return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
        
        #>> Obtiene los datos del owner-usuario mediante el keyuser.
        res_get_keyuser: ResponseModel = await query_authenticate_keyuser(user.user_token)
        if res_get_keyuser.error is True:
            return response_modelx(res_get_keyuser.status, True, res_get_keyuser.message, None)
        
        query_response: ResponseModel= await query_get_user_by_userid_or_username(res_get_keyuser.res.user_id)
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        
        if not await UsersManager().user_is_active(query_response.res):
            return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "El usuario esta inactivo.", None)

        return response_modelx(status.HTTP_200_OK, False, "Usuario obtenido exitosamente.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Oops! Lo sentimos, se produjo un error al procesar la peticion. Intentalo de nuevo en un momento.", None)


@user_router.post("/sign_in")
async def login_user(user: UserSignIn):
    #try:
    if not user.username_or_email or not user.password:
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
    
    #>> Se hashea la contraseña
    password = await HashingManager().hash_password(user.password)
    
    #>> Obtiene los datos del usuario mediante el username o email y el password.
    response_get_user: ResponseModel = await query_authenticate_user(user.username_or_email, password)
    if response_get_user.error is True:
        return response_modelx(response_get_user.status, True, response_get_user.message, None)
    
    #>> Genera un token de seguridad para el usuario, y se inserta el usuario en la db.
    response_key_user: ResponseModel = await query_insert_key_user(response_get_user.res.user_id, response_get_user.res.owner_id)
    if response_key_user.error is True:
        return response_modelx(response_get_user.status, True, response_key_user.message, None)
    
    #>> Devuelve el token de seguridad.
    return response_modelx(status.HTTP_200_OK, False, "Inicio de sesion exitoso.", response_key_user.res)
    #except:
        #return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Se produjo un error al procesar la peticion.", None)


#Administration
#endregion


#region: Sub-Users
@user_router.post("/subs/get")
async def get_sub_user(user: SubKeyUser):
    #try
    if not user.user_token or not user.username:
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
    
    #>> Obtiene los datos del owner-usuario mediante el keyuser.
    response_get_keyuser: ResponseModel = await query_authenticate_keyuser(user.user_token)
    if response_get_keyuser.error is True:
        return response_modelx(response_get_keyuser.status, True, response_get_keyuser.message, None)
    
    #>> Obtiene datos importantes del owner-usuario desde User.
    response_get_user: ResponseModel= await query_get_user_by_userid_or_username(response_get_keyuser.res.user_id)
    if response_get_user.error is True:
        return response_modelx(response_get_user.status, True, response_get_user.message, None)
    
    if not await UsersManager().user_is_active(response_get_user.res):
        return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "El usuario esta inactivo.", None)

    if not await UsersManager().user_is_owner(response_get_user.res):
        return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "No tienes permisos para acceder a este recurso.", None)

    #>> Obtiene el usuario especificado por username desde owner-usuario.
    response_get_sub_user: ResponseModel= await query_get_sub_user(user.username, response_get_user.res.owner_id)
    if response_get_sub_user.error is True:
        return response_modelx(response_get_sub_user.status, True, response_get_sub_user.message, None)
    
    return response_modelx(status.HTTP_200_OK, False, "Sub-usuario obtenido exitosamente.", response_get_sub_user.res)
    #except:
        #return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Se produjo un error al procesar la peticion.", None)


@user_router.post("/subs/get_all")
async def get_all_sub_user(user: KeyUser):
    if not user.user_token:
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
        
    try:
        #>> Obtiene los datos del owner-usuario mediante el keyuser.
        response_get_keyuser: ResponseModel = await query_authenticate_keyuser(user.user_token)
        if response_get_keyuser.error is True:
            return response_modelx(response_get_keyuser.status, True, response_get_keyuser.message, None)
        
        #>> Obtiene datos importantes del owner-usuario desde User.
        res_get_user: ResponseModel= await query_get_user_by_userid_or_username(response_get_keyuser.res.user_id)
        if res_get_user.error is True:
            return response_modelx(res_get_user.status, True, res_get_user.message, None)
        
        if not await UsersManager().user_is_active(res_get_user.res):
            return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "El usuario esta inactivo.", None)
        
        if not await UsersManager().user_is_owner(res_get_user.res):
            return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "No tienes permisos para acceder a este recurso.", None)
        
        #>> Obtiene todos los sub-usuarios del owner-usuario.
        response_get_sub_users: ResponseModel= await query_get_all_sub_users(res_get_user.res.owner_id)
        if response_get_sub_users.error is True:
            return response_modelx(response_get_sub_users.status, True, response_get_sub_users.message, None)
        
        return response_modelx(status.HTTP_200_OK, False, f"Sub-usuarios del usuario {res_get_user.res.username}.", response_get_sub_users.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Se produjo un error al procesar la peticion.", None)


#region: Registration
@user_router.post("/register", response_model=UserModel)
async def register_user(user: UserCreate):
    try:
        if not user.username or not user.password or not user.email or not user.full_name:
            return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
        
        #>> Verifica si el usuario ya existe.
        res_user_exists: ResponseModel = await query_owner_user_exists(user.username, user.email)
        if res_user_exists.error is True:
            return response_modelx(res_user_exists.status, True, res_user_exists.message, None)
        
        #>> Inserta a la db un nuevo usuario de tipo owner.
        query_response: ResponseModel= await query_insert_new_user(user)
        if query_response.error is True:
            return response_modelx(status.HTTP_400_BAD_REQUEST, True, "El usuario no pudo ser registrado.", None)
        
        return response_modelx(status.HTTP_201_CREATED, False, "Usuario creado exitosamente.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Oops! Se produjo un inconveniente al procesar la peticion.", None)


@user_router.post("/register/sub", response_model=UserModel)
async def register_sub_user(user: SubUserCreate):
    if not user.owner_username or not user.username or not user.password or not user.email or not user.full_name:
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Existen campos vacíos.", None)
    
    try:    
        #>> Obtiene los datos del owner-usuario mediante el keyuser.
        response_get_keyuser: ResponseModel = await query_authenticate_keyuser(user.user_token)
        if response_get_keyuser.error is True:
            return response_modelx(response_get_keyuser.status, True, response_get_keyuser.message, None)
        
        #>> Obtiene datos importantes del owner-usuario desde User.
        res_get_user: ResponseModel= await query_get_user_by_userid_or_username(response_get_keyuser.res.user_id)
        if res_get_user.error is True:
            return response_modelx(res_get_user.status, True, res_get_user.message, None)
        
        #>> Verificando si el usuario esta activo.
        if not await UsersManager().user_is_active(res_get_user.res):
            return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "El usuario esta inactivo.", None)
        
        #>> Verificando si el owner-usuario tiene permisos para crear sub-usuarios.
        if not await UsersManager().user_is_owner(res_get_user.res):
            return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "No tienes permisos para acceder a este recurso.", None)
        
        sub_user= UserCreate(username=user.username, password=user.password, email=user.email, full_name=user.full_name)

        query_response: ResponseModel= await query_insert_new_subuser(query_response.res, sub_user)
        if query_response.error is True:
            return response_modelx(status.HTTP_400_BAD_REQUEST, True, "El sub-usuario no pudo ser registrado.", None)
        
        return response_modelx(status.HTTP_201_CREATED, False, "Sub-usuario creado exitosamente.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Oops! Lo sentimos, se produjo un error al procesar la peticion.", None)

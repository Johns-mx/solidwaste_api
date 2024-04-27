from fastapi import APIRouter, status
from app.config.functions import response_modelx
from app.config.queries import *
from app.schemas.schemas import KeyUser, ResponseModel


subuser_router = APIRouter()


@subuser_router.get("/me")
async def get_user(key_user: KeyUser):
    query_response: ResponseModel= await query_get_full_user("johnsmx", "123456789", is_owner=False)
    if query_response.error is True:
        return response_modelx(query_response.status, True, query_response.message, None)
    return response_modelx(status.HTTP_200_OK, False, "Usuario obtenido exitosamente.", query_response.res)

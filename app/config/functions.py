from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.db.models import User
from app.schemas.schemas import UserUpdateInternal, VersionAPI


#>> Metodo para enviar respuesta 200, 300, 400, 500 ~
def response_modelx(status_code, error: bool, message: str, res, headers=None):
    """[method]: Devuelve un JSONResponse en cada solicitud a la API, para mostrar la respuesta al usuario."""
    response_headers = {"Content-Type": "application/json"}
    if headers:
        response_headers.update(headers)

    return JSONResponse(
        status_code=status_code,
        headers=response_headers,
        content=jsonable_encoder({
            "error": error,
            "message": message,
            "res": res,
            "version": VersionAPI().version
        }),
    )


async def updating_user_data(user_to_update: User, new_user_data: UserUpdateInternal) -> User:
    """[method]: Actualiza el usuario (user_to_update) con los nuevos datos proporcionados en new_user_data."""
    for field, value in new_user_data.__dict__.items():
        if hasattr(user_to_update, field) and (value is not None and value != user_to_update.__dict__[field]):
            setattr(user_to_update, field, value)
    return user_to_update


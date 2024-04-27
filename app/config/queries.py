from fastapi import status
from sqlalchemy import and_, exists, or_
from sqlalchemy.orm import defer
from app.db.models import TownHall, User, SubUser, KeyUser
from app.db.connection import SessionLocal
from app.schemas.schemas import KeyUserData, KeyUserInternalData, ResponseModel, TownHallCreate, TownHallInternalModel, UserInternalData, UserCreate
from app.core.security.hashing import generate_token_keyuser, generate_uuid, HashingManager


#region: Create User
async def query_insert_new_user(user: UserCreate) -> ResponseModel:
    """(🟢 in production): Create a new user."""
    try:
        with SessionLocal() as session:
            try:
                owner_id = generate_uuid()
                password = await HashingManager().hash_password(user.password)
                new_user = User(username=user.username, password=password, email=user.email, full_name=user.full_name, is_owner=True, is_active=True, owner_id=owner_id, is_admin=False)
                session.add(new_user)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(new_user)
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Usuario creado exitosamente.", res=new_user)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="Usuario no pudo ser registrado.", res=None)


async def query_insert_new_subuser(user: UserInternalData | User, sub_user: UserCreate) -> ResponseModel:
    """(🟢 in production): Create a new sub-user."""
    try:
        with SessionLocal() as session:
            try:
                password = await HashingManager().hash_password(sub_user.password)
                new_user = SubUser(username=sub_user.username, password=password, email=sub_user.email, full_name=sub_user.full_name, is_owner=False, is_active=True, owner_id=user.owner_id)
                session.add(new_user)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(new_user)
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Usuario creado exitosamente.", res=new_user)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="Usuario no pudo ser registrado.", res=None)


async def query_insert_new_town_hall(town_hall: TownHallCreate | TownHallInternalModel) -> ResponseModel:
    """(🟢 in production): Create a new Town Hall."""
    try:
        with SessionLocal() as session:
            try:
                new_town_hall = TownHall(title=town_hall.title, description=town_hall.description, community=town_hall.community, location=town_hall.location.__dict__, contacts=town_hall.contacts.__dict__, email=town_hall.email, is_active=True, is_available=True)
                session.add(new_town_hall)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(new_town_hall)
        return ResponseModel(status=status.HTTP_201_CREATED, error=False, message="Ayuntamiento creado exitosamente.", res=new_town_hall)
    except:
        return ResponseModel(status=status.HTTP_400_BAD_REQUEST, error=True, message="Ayuntamiento no pudo ser registrado.", res=None)
#endregion


#region: Authentication
async def query_authenticate_user(username_or_email: str, password: str) -> ResponseModel:
    """(🟢 in production): Authenticate a user."""
    try:
        with SessionLocal() as session:
            user_data = session.query(User).filter(and_(or_(User.email == username_or_email, User.username == username_or_email), User.password == password)).with_entities(User.user_id, User.username, User.email, User.full_name, User.owner_id).first()
            if not user_data:
                user_data = session.query(SubUser).filter(and_(or_(SubUser.email == username_or_email, SubUser.username == username_or_email), SubUser.password == password)).with_entities(SubUser.user_id, SubUser.username, SubUser.email, SubUser.full_name, SubUser.owner_id).first()
            
            if not user_data:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            
            full_user = UserInternalData(*user_data)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=full_user)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_authenticate_keyuser(user_token: str) -> ResponseModel:
    """(🟢 in production): Authenticate a keyuser."""
    try:
        with SessionLocal() as session:
            key_data = session.query(KeyUser).filter(KeyUser.keyuser == user_token).with_entities(KeyUser.key_id, KeyUser.user_id, KeyUser.owner_id).first()
            if not key_data:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Keyuser no existente.", res=None)
            
            keyuser_data = KeyUserData(*key_data)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Keyuser encontrada.", res=keyuser_data)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener la Keyuser.", res=None)


async def query_keyuser_exists(user_token: str) -> ResponseModel:
    """(🔴 NOT in production): Check if a keyuser exists."""
    try:
        with SessionLocal() as session:
            key_data = session.query(exists().where(KeyUser.keyuser == user_token)).scalar()
            if not key_data: #>> puedo no ser necesario.
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Keyuser no existente.", res=False)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Keyuser encontrada.", res=True)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener la Keyuser.", res=None)



async def query_insert_key_user(user_id: int, owner_id: str=None) -> ResponseModel:
    """(🟢 in production): Create a new keyuser."""
    try:
        with SessionLocal() as session:
            try:
                keyuser= await generate_token_keyuser()
                new_keyuser = KeyUser(user_id=user_id, owner_id=owner_id, keyuser=keyuser)
                session.add(new_keyuser)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                session.refresh(new_keyuser)
        return ResponseModel(status=status.HTTP_200_OK, error=False, message="KeyUser registrada correctamente.", res=keyuser)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al registrar la keyuser del usuario.", res=None)



async def query_get_full_user(username: str, password: str, is_owner: bool=True) -> ResponseModel:
    """(🔴 NOT in production): Get owner-user by username and password.
    * Returns: ResponseModel.res -> UserInternalData"""
    try:
        with SessionLocal() as session:
            if is_owner:
                user_data = session.query(User).filter(User.username == username, User.password == password).options(defer(User.password)).first()
            else:
                user_data = session.query(SubUser).filter(SubUser.username == username, SubUser.password == password).options(defer(SubUser.password)).first()
            
            if not user_data:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=user_data)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_get_user_by_username(username: str) -> ResponseModel:
    """(🔴 NOT in production): Get owner-user by username.
    * Returns: ResponseModel.res -> UserInternalData"""
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.username == username).with_entities(User.user_id, User.username, User.email, User.full_name, User.owner_id).first()
            if not user:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            full_name = UserInternalData(*user)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=full_name)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_get_user_by_userid_or_username(field_of_user: int) -> ResponseModel:
    """(🟢 in production): Query get user by user_id. -> user_id, username, email, full_name, owner_id, is_active, is_admin"""
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(or_(User.user_id == field_of_user, User.owner_id == field_of_user, User.username == field_of_user)).with_entities(User.user_id, User.username, User.email, User.full_name, User.is_owner, User.owner_id, User.is_active, User.is_admin).first()
            if not user:
                user = session.query(SubUser).filter(or_(SubUser.user_id == field_of_user, SubUser.owner_id == field_of_user, SubUser.username == field_of_user)).with_entities(SubUser.user_id, SubUser.username, SubUser.email, SubUser.full_name, SubUser.is_owner, SubUser.owner_id, SubUser.is_active).first()
            
            if not user:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="Usuario no encontrado.", res=None)
            full_name = UserInternalData(*user)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Usuario encontrado.", res=full_name)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_owner_user_exists(username: str, email: str=None) -> ResponseModel:
    """(🟢 in production): Get owner-user by username.
    * Returns: ResponseModel.res -> UserInternalData"""
    try:
        with SessionLocal() as session:
            user_existence = session.query(exists().where(or_(User.username == username, User.email == email))).scalar()
            if user_existence is False:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="El usuario no existe.", res=False)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="El usuario ya existe.", res=True)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el usuario.", res=None)


async def query_get_sub_user(username: str, owner_id: str) -> ResponseModel:
    """(🟢 in production): Query the sub user for a given username and owner_id."""
    try:
        with SessionLocal() as session:
            user = session.query(SubUser).filter(and_(SubUser.owner_id == owner_id, SubUser.username == username)).options(
                defer(SubUser.password), defer(SubUser.owner_id)
            ).first()
            if not user:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="El sub-usuario no existe.", res=user)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Sub-usuario encontrado.", res=user)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener el sub-usuario.", res=None)


async def query_get_all_sub_users(owner_id: str) -> ResponseModel:
    """(🟢 in production): Query the sub-users for a given owner_id."""
    try:
        with SessionLocal() as session:
            user = session.query(SubUser).filter(SubUser.owner_id == owner_id).options(
                defer(SubUser.password), defer(SubUser.owner_id)
            ).all()
            if not user:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="No existen sub-usuarios.", res=user)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Sub-usuarios encontrados.", res=user)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener los sub-usuarios.", res=None)


#region: Town Halls
async def query_get_all_town_hall() -> ResponseModel:
    """(🟢 in production): Query all town halls."""
    try:
        with SessionLocal() as session:
            all_town_hall = session.query(TownHall).all()
            if not all_town_hall:
                return ResponseModel(status=status.HTTP_404_NOT_FOUND, error=True, message="No existen ayuntamientos.", res=all_town_hall)
            return ResponseModel(status=status.HTTP_200_OK, error=False, message="Ayuntamientos encontrados.", res=all_town_hall)
    except:
        return ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=True, message="Error al obtener los ayuntamientos.", res=None)

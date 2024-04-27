from app.db.connection import engine, Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, JSON


class User(Base):
    """[Modelo DB]: Users"""
    __tablename__ = 'users'
    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = Column("username", String(100), unique=True, nullable=True)
    password = Column("password", String(100), nullable=True)
    email = Column("email", String(100), unique=True, nullable=False)
    full_name = Column("full_name", String(100), nullable=True)
    is_owner = Column("is_owner", Boolean, nullable=False)
    owner_id = Column("owner_id", Integer, unique=True, nullable=False)
    created_at = Column("created_at", TIMESTAMP, nullable=True)
    updated_at = Column("updated_at", TIMESTAMP, nullable=True)
    is_active = Column("is_active", Boolean, nullable=True)
    phone = Column("phone", String(15), nullable=True)
    language = Column("language", String(15), nullable=True)
    id_card = Column("id_card", String(15), nullable=True)
    is_admin = Column("is_admin", Boolean, nullable=True)


class SubUser(Base):
    """[Modelo DB]: Sub Users"""
    __tablename__ = 'sub_users'
    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    owner_id = Column("owner_id", Integer, unique=True, nullable=False)
    username = Column("username", String(100), nullable=False)
    password = Column("password", String(100), nullable=True)
    email = Column("email", String(100), nullable=True)
    full_name = Column("full_name", String(100), nullable=True)
    is_owner = Column("is_owner", Boolean, nullable=False)
    created_at = Column("created_at", TIMESTAMP, nullable=True)
    updated_at = Column("updated_at", TIMESTAMP, nullable=True)
    is_active = Column("is_active", Boolean, nullable=True)
    #phone = Column("phone", String(15), nullable=True)
    #language = Column("language", String(15), nullable=True)
    #id_card = Column("id_card", String(15), nullable=True)
    #is_admin = Column("is_admin", Boolean, default=False, nullable=True)


class KeyUser(Base):
    """[Modelo DB]: Esta tabla se utiliza para almacenar las llaves de acceso de los usuarios.
    * user_id: int | owner_id: str | keyuser: str
    """
    __tablename__ = 'keys'
    key_id = Column("key_id", Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column("user_id", Integer, nullable=False)
    owner_id = Column("owner_id", Integer, nullable=True)
    keyuser = Column("keyuser", String(200), nullable=True)
    created_at = Column("created_at", TIMESTAMP, nullable=True)


class TownHall(Base):
    """[Modelo DB]: Esta tabla se utiliza para almacenar los datos de la ciudadanía."""
    __tablename__ = 'town_hall'
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column("title", String(100), nullable=True)
    description = Column("description", String(300), nullable=True)
    community = Column("community", String(100), nullable=False)
    location = Column("location", JSON, nullable=True)
    contacts = Column("contacts", JSON, nullable=True)
    email = Column("email", String(50), nullable=True)
    is_active = Column("is_active", Boolean, default=True, nullable=True)
    is_available = Column("is_available", Boolean, default=True, nullable=True)
    created_at = Column("created_at", TIMESTAMP, nullable=True)
    updated_at = Column("updated_at", TIMESTAMP, nullable=True)


"""
** Los usuarios comunes (la gente) va a tener acceso sin la creacion de una cuenta, solo se 
requerira que dicho usuario inicie session con Google/iCloud para reportar algun problema, 
y el uso de funciones similares.
"""


Base.metadata.create_all(engine)
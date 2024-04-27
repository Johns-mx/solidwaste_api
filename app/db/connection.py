import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = sqlalchemy.create_engine("mysql+pymysql://root:john_admin@localhost:3306/solidwastedb", 
    echo=False, pool_pre_ping=True,
    pool_timeout=20, pool_recycle=-1
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
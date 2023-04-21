import configparser
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

file_config = Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB_DEV', 'user')
host = config.get('DB_DEV', 'host')
db_name = config.get('DB_DEV', 'db_name')
password = config.get('DB_DEV', 'password')
port = config.get('DB_DEV', 'port')

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()

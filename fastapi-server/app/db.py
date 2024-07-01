from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

user_name=""
password=""
db_host="127.0.0.1"
db_name=""

DATABASE='mysql://'+user_name+':'+password+'@'+db_host+'/'+db_name+"?charset=utf8"

engine = create_engine(
    DATABASE,
    encoding='utf8',
    echo=True)

sesstion=scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    ))

Base = declarative_base()
Base.query = sesstion.query_property()

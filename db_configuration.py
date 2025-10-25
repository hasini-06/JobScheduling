from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
URI="sqlite:///./job.db"

engine=create_engine(URI,connect_args={"check_same_thread": False})

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

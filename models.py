# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    files = relationship("UserFile", back_populates="user")

class UserFile(Base):
    __tablename__ = 'user_files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="files")

DATABASE_URL = 'sqlite:///myapp.db'

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

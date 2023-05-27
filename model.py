# coding: utf-8
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import engine


class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=True)
    age = Column(Integer)


class User(BaseModel):
    id   : int
    name : str
    age  : int


def main():
    # Table 없으면 생성
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()
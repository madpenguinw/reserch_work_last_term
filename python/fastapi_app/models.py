from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "patronymic": self.patronymic,
            "age": self.age,
        }

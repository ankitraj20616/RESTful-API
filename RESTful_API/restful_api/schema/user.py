from dependency.database import Base
from sqlalchemy import Column, Integer, String


class user(Base):
    __tablename__ = "Employee"

    emp_id = Column(Integer, autoincrement= True, primary_key= True)
    full_name = Column(String(100))
    dept_id = Column(Integer)
    salary = Column(Integer)

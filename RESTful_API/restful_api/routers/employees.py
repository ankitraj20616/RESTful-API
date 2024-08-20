from fastapi import APIRouter, Depends, HTTPException, Path
from dependency.database import session_local
from typing import Annotated
from sqlalchemy.orm import Session
from schema.user import user
from pydantic import BaseModel, Field
from starlette import status

router = APIRouter()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class User_Reqst(BaseModel):
    full_name: str = Field(min_length= 1)
    dept_id: int = Field(gt= 0)
    salary: int = Field(gt= 0)



@router.get("/")
def read_all(db: db_dependency):
    return db.query(user).all()

@router.get("/{emp_id}")
def read_by_emp_id(db: db_dependency, emp_id: int):
    emp = db.query(user).filter(user.emp_id == emp_id).first()
    if emp is not None:
        return emp
    raise HTTPException(status_code= 404, detail= "Employee of provided id is not present in database.")

@router.get("/dept_id/")
def read_by_dept_id(db: db_dependency, dept_id: int):
    emp = db.query(user).filter(user.dept_id == dept_id).all()
    if len(emp) > 0:
        return emp
    raise HTTPException(status_code= 404, detail= "Department of provided id is not present in database.")

@router.post("/new_employee", status_code= status.HTTP_201_CREATED)
def create_new_employee(db: db_dependency, new_emp: User_Reqst):
    new_emp = user(**(new_emp.model_dump()))
    db.add(new_emp)
    db.commit()


@router.put("/update_employee/{emp_id}", status_code= status.HTTP_204_NO_CONTENT)
def update_employee(db: db_dependency, upated_emp: User_Reqst, emp_id: int= Path(gt = 0)):
    old_emp = db.query(user).filter(user.emp_id == emp_id).first()
    if old_emp is None:
        raise HTTPException(status_code= 404, detail= "Provided Employee id not present!")
    old_emp.full_name = upated_emp.full_name
    old_emp.dept_id = upated_emp.dept_id
    old_emp.salary = upated_emp.salary

    db.add(old_emp)
    db.commit()

@router.delete("/delete_emp/{emp_id}")
def delete_employee(db: db_dependency, emp_id: int = Path(gt = 0)):
    emp = db.query(user).filter(user.emp_id == emp_id).first()
    if emp is None:
        raise HTTPException(status_code= 404, detail= "Provided Employee id not present!")
    
    db.query(user).filter(user.emp_id == emp_id).delete()
    db.commit()

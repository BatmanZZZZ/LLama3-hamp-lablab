from pydantic import BaseModel
from typing import Dict, List, Union

class Task(BaseModel):
    name: str
    start_date: str
    duration: int

class Project(BaseModel):
    title: str
    project_start_date: str
    tasks: List[Task]

class RouteIdentification(BaseModel):
    route: str

class Pert_Task(BaseModel):
    Tid: str
    start: int
    duration: int
    end: int
    responsible: str
    pred: List[str]

class PertProject(BaseModel):
    Pert_Dict: Dict[str, Pert_Task]

class RouteIdentification(BaseModel):
    route: str
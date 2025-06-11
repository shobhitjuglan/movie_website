from enum import IntEnum
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()

# MODELS for the apis

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name : str = Field(..., min_length=3, max_length=512, description="todo task ka name")
    todo_description : str = Field(..., description="todo task ki description")
    priority: Priority

class Todo(TodoBase):
    todo_id: int = Field(..., description="id of the todo") 

class TodoCreate(TodoBase):
    pass   

class TodoUpdate(BaseModel):
    priority : Optional[Priority] = Field(None, description="Enter your priority")
    todo_name : Optional[str] = Field(None, min_length=3, max_length=512, description="todo task ka name")
    todo_description : Optional[str] = Field(None, description="todo task ki description")



# Simulated database
all_todos = [
    Todo(todo_id=1, todo_name='Sports', todo_description='Go to the gym', priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name='Dev Project', todo_description='Make a live paper trading website and deploy it', priority=Priority.HIGH),
    Todo(todo_id=3, todo_name='Date', todo_description='Call and have fun for 10 mins exact, focus', priority=Priority.LOW),
]



# SCHEMAS for the apis




# API ROUTES for the apis


# The below code is like how a newbie to fastapi would have written the code
# We use pydantic to make checks and also exceptions library to print custom errors

@api.get('/')
def index():
    return {"message":"Hello world"}


@api.get('/todos/{todo_id}', response_model=Todo)
def get(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    return HTTPException(status_code=404, detail='Todo not found')

@api.get('/todos', response_model=List[Todo])
def get(first_n: int = None):
    if(first_n):
        return all_todos[:first_n]
    else:
        return all_todos

@api.post('/todos', response_model=List[Todo])
# def post(todo_list: list[dict]):
def post(todo_list: List[TodoCreate]):
    index = max(todos.todo_id for todos in all_todos)+1
    for todo in todo_list:
        all_todos.append(Todo(todo_id=index, todo_name=todo.todo_name, todo_description=todo.todo_description,
                          priority=todo.priority))
        index = index + 1
    return all_todos

@api.put('/todos/{todo_id}', response_model=List[Todo])
def update_todos(todo_id: int, todo: TodoUpdate):
    for todos in all_todos:
        if todos.todo_id == todo_id:
            todos.todo_name = todo.todo_name
            todos.todo_description = todo.todo_description
            todos.priority = todo.priority
            return all_todos
    raise HTTPException(status_code=404, detail='Todo not found')

@api.delete('/todos/{todo_id}', response_model=List[Todo])
def delete_todo(todo_id: int):
    for index, todos in enumerate(all_todos):
        if todos.todo_id == todo_id:
            all_todos.pop(index)
            return all_todos
    raise HTTPException(status_code=404, detail='Todo not found')

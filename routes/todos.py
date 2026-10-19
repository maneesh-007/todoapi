from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.todo import Todo
from utilities import get_current_user
from schemas.todos import TodoCreate,TodoUpdate, TodoResponse



todorouter = APIRouter()

@todorouter.get("/todos")
def get_todos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).all()
    return todos

@todorouter.post("/add-todo", response_model=TodoResponse)
def add_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    print("Current User:", current_user)  # Debugging line
    #todo.user_id = current_user.id
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        user_id=current_user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@todorouter.put("/update-todo/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.completed = updated_todo.completed
    db.commit()
    db.refresh(todo)
    return todo 

@todorouter.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

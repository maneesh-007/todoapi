from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. Schema for Creating a Todo
class TodoCreate(BaseModel):
    title: str
    description: str

# 2. Schema for Updating a Todo (all fields optional for partial updates)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# 3. Schema for Returning Todo Data (Response Model)
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# 4. Schema for Delete / Generic Success Responses
class MessageResponse(BaseModel):
    message: str
    success: bool = True
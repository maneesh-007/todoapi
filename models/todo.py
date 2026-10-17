from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship,Mapped,mapped_column



class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    user_id: Mapped[int] = mapped_column(Integer,  ForeignKey("users.id"),index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", back_populates="todos")
    
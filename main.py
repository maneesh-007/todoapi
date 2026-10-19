from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import userrouter
from routes.todos import todorouter


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Todo API"}

app.include_router(userrouter)
app.include_router(todorouter)
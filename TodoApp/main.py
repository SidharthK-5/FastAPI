from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(router=auth.router, tags=["Authentication"])
app.include_router(router=admin.router, tags=["Admin"])
app.include_router(router=users.router, tags=["User"])
app.include_router(router=todos.router, tags=["Manage Todos"])

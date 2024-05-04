import sys
from starlette.responses import RedirectResponse
from starlette import status
from fastapi import Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from .auth import get_current_user, get_password_hash, verify_password
from database import SessionLocal, engine

sys.path.append("..")

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users", tags=["users"], responses={401: {"user": "Not Found"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/change-password", response_class=HTMLResponse)
async def change_password(request: Request):
    user = await get_current_user(request=request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "edit-user-password.html", {"request": request, "user": user}
    )


@router.post("/change-password", response_class=HTMLResponse)
async def changes_user_password(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    user = await get_current_user(request=request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(models.Users.username == username).first()
    msg = "Invalid username or password"

    if user_data is not None:
        if username == user_data.username and verify_password(
            password, user_data.hashed_password
        ):
            user_data.hashed_password = get_password_hash(password2)
            db.add(user_data)
            db.commit()
            msg = "Password updated"

    return templates.TemplateResponse(
        "edit-user-password.html", {"request": request, "user": user, "msg": msg}
    )

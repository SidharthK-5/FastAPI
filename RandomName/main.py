from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette import status
from sqlalchemy.orm import Session
import random
import models
from database import engine, SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


async def query_from_db(
    team: str = None, exception: str = None, db: Session = Depends(get_db)
) -> list:
    if team:
        # To select members from a specific team
        return (
            db.query(models.Members)
            .filter(models.Members.team == team)
            .filter(models.Members.hosted == False)  # noqa: E712
            .filter(models.Members.exception == "No")  # noqa: E712
            .all()
        )
    elif exception:
        # To select members with "Tentative" exception
        return (
            db.query(models.Members)
            .filter(models.Members.hosted == False)  # noqa: E712
            .filter(models.Members.exception == exception)
            .all()
        )
    else:
        # To select from all members
        return (
            db.query(models.Members)
            .filter(models.Members.hosted == False)  # noqa: E712
            .filter(models.Members.exception == "No")  # noqa: E712
            .all()
        )


async def update_hosting_status(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Members).filter(models.Members.id == member_id).first()
    member.hosted = True
    print(f"Member {member.name} has been selected for hosting.")
    db.add(member)
    db.commit()


async def reset_hosting_status(
    exception_type: str = None, db: Session = Depends(get_db)
):
    if not exception_type:
        members = db.query(models.Members).all()
    else:
        members = (
            db.query(models.Members)
            .filter(models.Members.exception == exception_type)
            .all()
        )
    for member in members:
        member.hosted = False
        db.add(member)
    db.commit()
    print("Selected members' hosting status has been reset.")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/view-all", response_class=HTMLResponse)
async def view_all(request: Request, db: Session = Depends(get_db)):
    members = db.query(models.Members).order_by(models.Members.name).all()
    return templates.TemplateResponse(
        "view_members.html", {"request": request, "members": members}
    )


@app.get("/random-dev-team-member")
async def random_dev_team_member(db: Session = Depends(get_db)):
    members = await query_from_db(team="DEV", db=db)
    if len(members) > 0:
        selected_member = random.choice(members)
        member_name = selected_member.name

        # Update hosting status of the selected member
        await update_hosting_status(member_id=selected_member.id, db=db)
        return member_name
    else:
        return "No available member to host."


@app.get("/random-qa-team-member")
async def random_qa_team_member(db: Session = Depends(get_db)):
    members = await query_from_db(team="QA", db=db)
    if len(members) > 0:
        selected_member = random.choice(members)
        member_name = selected_member.name

        # Update hosting status of the selected member
        await update_hosting_status(member_id=selected_member.id, db=db)
        return member_name
    else:
        return "No available member to host."


@app.get("/random-tentative-team-member")
async def random_tentative_team_member(db: Session = Depends(get_db)):
    members = await query_from_db(exception="Tentative", db=db)
    if len(members) == 0:
        print("No available member to host.")
        await reset_hosting_status(exception_type="Tentative", db=db)
        members = await query_from_db(exception="Tentative", db=db)

    selected_member = random.choice(members)
    member_name = selected_member.name

    # Update hosting status of the selected member
    await update_hosting_status(member_id=selected_member.id, db=db)
    return member_name


@app.get("/random-team-member")
async def random_team_member(db: Session = Depends(get_db)):
    members = await query_from_db(db=db)
    if len(members) == 0:
        print("No available member to host.")
        await reset_hosting_status(db=db)
        members = await query_from_db(db=db)

    selected_member = random.choice(members)
    member_name = selected_member.name

    # Update hosting status of the selected member
    await update_hosting_status(member_id=selected_member.id, db=db)
    return member_name


@app.get("/add-member", response_class=HTMLResponse)
async def add_member(request: Request):
    return templates.TemplateResponse("add_member.html", {"request": request})


@app.post("/add-member", response_class=HTMLResponse)
async def add_team_member(
    request: Request,
    name: str = Form(...),
    team: str = Form(...),
    hosted: str = Form(...),
    exception: str = Form(...),
    db: Session = Depends(get_db),
):
    new_member = models.Members()
    new_member.name = name
    new_member.team = team
    new_member.hosted = False if hosted == "No" else True
    new_member.exception = exception

    db.add(new_member)
    db.commit()

    return templates.TemplateResponse(
        "add_member.html", {"request": request, "msg": "Member added successfully!"}
    )


@app.get("/edit-member/{member_id}", response_class=HTMLResponse)
async def edit_member(request: Request, member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Members).filter(models.Members.id == member_id).first()
    return templates.TemplateResponse(
        "edit_member.html", {"request": request, "member": member}
    )


@app.post("/edit-member/{member_id}", response_class=HTMLResponse)
async def edit_member_commit(
    request: Request,
    member_id: int,
    name: str = Form(...),
    team: str = Form(...),
    hosted: str = Form(...),
    exception: str = Form(...),
    db: Session = Depends(get_db),
):
    member = db.query(models.Members).filter(models.Members.id == member_id).first()
    member.name = name
    member.team = team
    member.hosted = False if hosted == "No" else True
    member.exception = exception

    db.add(member)
    db.commit()

    return RedirectResponse(url="/view-all", status_code=status.HTTP_302_FOUND)

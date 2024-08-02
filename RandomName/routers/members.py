from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from sqlalchemy.orm import Session
import random
import models
from database import engine, SessionLocal

router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        members = (
            db.query(models.Members)
            .filter(models.Members.exception.in_(["Yes", "No"]))
            .all()
        )
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


@router.get("/view-all", response_class=HTMLResponse)
async def view_all(request: Request, db: Session = Depends(get_db)):
    members = db.query(models.Members).order_by(models.Members.name).all()
    return templates.TemplateResponse(
        "view_members.html", {"request": request, "members": members}
    )


@router.get("/random-dev-team-member")
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


@router.get("/random-qa-team-member")
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


@router.get("/random-tentative-team-member")
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


@router.get("/random-team-member")
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


@router.get("/add-member", response_class=HTMLResponse)
async def add_member(request: Request):
    return templates.TemplateResponse("add_member.html", {"request": request})


@router.post("/add-member", response_class=HTMLResponse)
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


@router.get("/edit-member/{member_id}", response_class=HTMLResponse)
async def edit_member(request: Request, member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Members).filter(models.Members.id == member_id).first()
    return templates.TemplateResponse(
        "edit_member.html", {"request": request, "member": member}
    )


@router.post("/edit-member/{member_id}", response_class=HTMLResponse)
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

    return RedirectResponse(url="/members/view-all", status_code=status.HTTP_302_FOUND)


@router.get("/count-dev-team-members")
async def count_dev_team_members(db: Session = Depends(get_db)):
    members = await query_from_db(team="DEV", db=db)
    return len(members)


@router.get("/count-qa-team-members")
async def count_qa_team_members(db: Session = Depends(get_db)):
    members = await query_from_db(team="QA", db=db)
    return len(members)


@router.get("/count-tentative-team-members")
async def count_tentative_team_members(db: Session = Depends(get_db)):
    members = await query_from_db(exception="Tentative", db=db)
    return len(members)


@router.get("/count-all-members")
async def count_all_members(db: Session = Depends(get_db)):
    members = await query_from_db(db=db)
    return len(members)

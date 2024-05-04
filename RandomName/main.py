from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import random
from team_members import DEV_TEAM, QA_TEAM, WHOLE_TEAM

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/random-dev-team-member", response_class=HTMLResponse)
async def random_dev_team_member():
    return random.choice(DEV_TEAM)


@app.get("/random-qa-team-member", response_class=HTMLResponse)
async def random_qa_team_member():
    return random.choice(QA_TEAM)


@app.get("/random-team-member", response_class=HTMLResponse)
async def random_team_member():
    return random.choice(WHOLE_TEAM)

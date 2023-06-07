#로그인 함수 구현
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from db import session
from model import CaseTable, Case, CaseVital, Vital, UserTable
# from model import

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {}
    context['request'] = request
    return templates.TemplateResponse("home.html", context)


@app.post("/login", response_class=RedirectResponse)
async def login(request: Request, form_data: dict = Form(...)):
    print(form_data)

    user = session.query(UserTable).filter_by(
        u_id=form_data["u_id"], u_pw=form_data["u_pw"]).first()
    
    if user:
        return RedirectResponse(url="/cases")
    else:
        return
        #return templates.TemplateResponse("home.html", {"request": request})
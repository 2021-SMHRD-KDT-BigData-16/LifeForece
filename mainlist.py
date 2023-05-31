from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import List
from starlette.middleware.cors import CORSMiddleware

from db import session
from model import CaseTable, Case, CaseVital, Vital

import json

templates = Jinja2Templates(directory="templates")

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
    return {"message": "/cases 에서 사용자관리"}


# ----------API 정의------------
@app.get("/cases", response_class=HTMLResponse)
async def read_cases(request: Request):
    
    context = {}

    cases = session.query(CaseTable).limit(10).all()

    context['request'] = request
    context['cases'] = cases

    return templates.TemplateResponse("user_list.html", context)


@app.get("/cases/{case_id}", response_class=HTMLResponse)
async def read_case(request: Request, case_id: int, page: int =1, rows_per_page: int=10):
    context = {}    
    case = session.query(CaseTable).filter(CaseTable.p_id == case_id).first()
    context['case'] = case
    vitals_query = session.query(CaseVital).filter(CaseVital.p_id == case_id)

    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    # Calculate the total number of rows
    total_rows = vitals_query.count()
    
    # Calculate the total number of pages
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page
    

    vitals = vitals_query.offset((page - 1) * rows_per_page).limit(rows_per_page).all()
    
    context['vitals']= vitals
    context['request'] = request
    context['page'] = page
    context['rows_per_page'] = rows_per_page
    context['total_pages'] = total_pages

    return templates.TemplateResponse("user_detail.html", context)


@app.post("/cases")
async def create_case(cases: Case):
    
    # data = await request.json()
    #caselist = list(cases)
    #caselist[0][1]
    #caselist[1][1]

    # 환자번호 입력하면 넣는 작업 필요
    # 점수가져와서 넣는 작업 필요
    u_id = "x"
    p_id = "1225"
    
    case = CaseTable()
    case.u_id = u_id
    case.p_id = p_id
    

    session.add(case)
    session.commit()

    return { 'result_msg': f'{p_id} Registered...' }


@app.put("/cases")
async def modify_cases(p_id: int = Form(...), p_cmt: str = Form(...)):
    #async def modify_cases(p_id: int = Form(...), p_cmt: str = Form(...)):
    #점수변화 확인하려면 # 풀어주기
    #현재는 cmt 만 수정할 수 있도록 해줬음

    #caselist = list(cases)   
    ##u_id = caselist[0][1]
    #p_id = caselist[1][1]
    ##p_score = caselist[2][1]
    ##p_SOFA = caselist[3][1]
    ##p_MEWS = caselist[4][1]
    #p_cmt = caselist[5][1]

    case = session.query(CaseTable).filter(CaseTable.p_id == p_id).first()
    #case.u_id = u_id
    #case.p_id = p_id
    #case.p_score = p_score
    #case.p_SOFA = p_SOFA
    #case.p_MEWS = p_MEWS
    case.p_cmt = p_cmt
    session.commit()

    return { 'result_msg': f"{p_id} updated..." }


@app.delete("/cases")
async def delete_cases(cases: Case):    

    caselist = list(cases)
    p_id = caselist[1][1]

    cases = session.query(CaseTable).filter(CaseTable.p_id == p_id).delete()
    session.commit()

    return {'result_msg': f"User deleted..."}
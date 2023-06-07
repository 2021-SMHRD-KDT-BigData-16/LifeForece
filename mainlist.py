from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from db import session
from fastapi import Body
from model import CaseTable, Case, CaseVital, Vital, UserTable, User
import pretreatment as pre
import pandas as pd
import prediction as pred
import sofa_mews
#from fastapi.responses import JSONResponse
# rom typing import List
#import json

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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
    return templates.TemplateResponse("login.html", context)

@app.post("/login")
async def login(request: Request, login_data: dict = Body(...)):
   
    u_id = login_data.get("u_id")
    u_pw = login_data.get("u_pw")
    print(u_id)
    #print(u_pw)    
    user = session.query(UserTable).filter_by(u_id=u_id, u_pw=u_pw).first()
    username=user.u_name
    print(user.u_name)    
    
    return {'user': f"{username}"}
   
# ------- 환자 검색하기 -------------------


@app.get("/search_case", response_class=HTMLResponse)
async def search_case_by_id(request: Request, p_id: int):
    context = {}
    case = session.query(CaseTable).filter_by(p_id=p_id).first()
    context['request'] = request
    context['case'] = case if case else {}
    print()
    session.close()
    return templates.TemplateResponse("user_search.html", context)

# ----------casetable에 있는 환자 점수 목록 가져오기------------

@app.get("/cases", response_class=HTMLResponse)
async def read_cases(request: Request,user: str = Query(...)):
    context = {}      
    cases = session.query(CaseTable).all()
    context['request'] = request
    context['cases'] = cases 
    context['user'] = user  
    session.close()

    return templates.TemplateResponse("user_list.html", context)


# ------환자 점수 목록에서 클릭시 환자의 casevital에 있는 값을 다른페이지에 가져오기----
@app.get("/cases/{case_id}", response_class=HTMLResponse)
async def read_case(request: Request, case_id: int, page: int = 1, rows_per_page: int = 10):
    context = {}
    # 환자 아이디와 LF 점수 를 담기 위해서 하나 선택해오기
    case = session.query(CaseTable).filter(CaseTable.p_id == case_id).first()
    context['case'] = case

    # 환자 한명의 바이탈 정보 담기
    vitals_query = session.query(CaseVital).filter(CaseVital.p_id == case_id)

    # 페이징처리하기
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    # Calculate the total number of rows
    total_rows = vitals_query.count()
    # Calculate the total number of pages
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page
    vitals = vitals_query.offset(
        (page - 1) * rows_per_page).limit(rows_per_page).all()

    context['vitals'] = vitals
    context['request'] = request
    context['page'] = page
    context['rows_per_page'] = rows_per_page
    context['total_pages'] = total_pages
    session.close()

    return templates.TemplateResponse("user_detail.html", context)


class MyData(BaseModel):
    id: int


@app.post("/cases1")
async def create_case(data: MyData):
    print(data.id)

    # 아이디로 DB 검색
    context = {}
    vitals = session.query(CaseVital).filter(CaseVital.p_id == data.id)
    context['vitals'] = vitals
    # Get the column names from the CaseVital table
    columns = CaseVital.__table__.columns.keys()

    # Convert query results to a DataFrame
    df = pd.DataFrame([{column: getattr(vital, column)
                      for column in columns} for vital in vitals])

    # 계산
    df = df.drop(['v_sequence'], axis=1)
    # print(df)
    # 전처리
    pre_df = pre.Pretreatment(df)

    # 모델 불러와서 예측
    prediction = pred.Prediction(pre_df)

    # print(prediction)
    df_ms =  sofa_mews.pre_treat(df)

    #sofa와 mews 점수 추가
    mews_max = sofa_mews.save_mews(df_ms)
    sofa_max = sofa_mews.save_sofa(df_ms)
    print(mews_max, sofa_max)

    # 계산 값을 DB에 저장
    new_case = CaseTable(u_id='a', p_id=data.id, p_score=prediction+40, p_SOFA=sofa_max, p_MEWS=mews_max)

    session.add(new_case)
    session.commit()
    print("확인")

    return {'result_msg': f"{data.id}"}

# -------- 환자에 대한 코멘트 수정하기----------


@app.put("/cases")
async def modify_cases(p_id: int = Form(...), p_cmt: str = Form(...)):

    case = session.query(CaseTable).filter(CaseTable.p_id == p_id).first()
    #case.u_id = u_id
    # case.p_id = p_id..
    print("수정")
    case.p_cmt = p_cmt
    session.commit()

    return {'result_msg': f"{p_id}"}

# -------- 환자 삭제하기 -------------------


@app.delete("/cases")
async def delete_cases(p_id: int):
    session.query(CaseTable).filter(CaseTable.p_id == p_id).delete()
    session.commit()
    print(p_id)

    return {'result_msg': f"{p_id}"}


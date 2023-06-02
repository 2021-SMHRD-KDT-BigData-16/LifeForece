from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import List
from starlette.middleware.cors import CORSMiddleware

from db import session
from model import CaseTable, Case, CaseVital, Vital
import pandas as pd
import json
from pydantic import BaseModel

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


# ----------casetable에 있는 환자 점수 목록 가져오기------------
@app.get("/cases", response_class=HTMLResponse)
async def read_cases(request: Request):
    
    context = {}
    cases = session.query(CaseTable).all()    
    
    context['request'] = request
    context['cases'] = cases    

    return templates.TemplateResponse("user_list.html", context)

# ------환자 점수 목록에서 클릭시 환자의 casevital에 있는 값을 다른페이지에 가져오기----
@app.get("/cases/{case_id}", response_class=HTMLResponse)
async def read_case(request: Request, case_id: float, page: int =1, rows_per_page: int=10):
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

# ------ 환자 아이디를 입력하면 그 환자의 casevital값을 가져와서 함수에 넣어야함---
# @app.get("/cases/{new_case}")   
# async def read_case(new_case: float):
    
#     return {"message":"Case values retrieved successively"}

# @app.post("/process")
# async def process_dataframe(request: Request):
#     dataframe = await request.form()
#     dataframe_value = dataframe["dataframe"]
    
#     # Convert the JSON dataframe value to a pandas DataFrame
#     import pandas as pd
#     df = pd.read_json(dataframe_value)

#     # Process the DataFrame as needed
#     # ...

#     return {"message": "DataFrame processed successfully"}


class MyData(BaseModel):
    id: str

@app.post("/cases1")
async def create_case(data: MyData):
    print(data.id)

    # 아이디로 DB 검색
    context = {}        
    vitals = session.query(CaseVital).filter(CaseVital.p_id == data.id)
    context['vitals']= vitals
    # Get the column names from the CaseVital table
    columns = CaseVital.__table__.columns.keys()

    # Convert query results to a DataFrame
    df = pd.DataFrame([{column: getattr(vital, column) for column in columns} for vital in vitals])
    
    print(df)
    # 계산
    
    df = df.drop(['v_sequence'], axis=1)
    
    # 전처리 
    import pretreatment as pre
    
    pre_df = pre.Pretreatment(df)
    print(pre_df)
    
    # 모델 불러와서 예측
    
    import prediction as pred
    
    prediction = pred.Prediction(pre_df)
    
    print(prediction)   

    # 계산 값을 DB에 저장

    # 원래 페이지로 이동
   


    # 점수가져와서 넣는 작업 필요
    # u_id = "a"
    # # p_id = "1225"    
    # case = CaseTable()
    # case.u_id = u_id
    # case.p_id = cases.p_id          

    # session.add(case)
    # session.commit()

    return {'result_msg': ' Registered...' }

#-------- 환자에 대한 코멘트 수정하기----------
@app.put("/cases")
async def modify_cases(p_id: float = Form(...), p_cmt: str = Form(...)):
    #async def modify_cases(p_id: int = Form(...), p_cmt: str = Form(...)):
    #점수변화 확인하려면 # 풀어주기
    #현재는 cmt 만 수정할 수 있도록 해줬음

    #caselist = list(cases)   
    #u_id = caselist[0][1]
    #p_id = caselist[1][1]...
   
    case = session.query(CaseTable).filter(CaseTable.p_id == p_id).first()
    #case.u_id = u_id
    #case.p_id = p_id..
  
    case.p_cmt = p_cmt
    session.commit()

    return { 'result_msg': f"{p_id} updated..." }


@app.delete("/cases")
async def delete_cases(p_id: float):   
    print(p_id)
    session.query(CaseTable).filter(CaseTable.p_id == p_id).delete()
    session.commit()

    return {'result_msg': f"Case deleted..."}
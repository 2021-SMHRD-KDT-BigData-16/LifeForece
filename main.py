from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware

from db import session
from model import CaseTable, Case

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------API 정의------------
@app.get("/cases")
def read_cases():
    cases = session.query(CaseTable).all()
    return cases

@app.get("/cases/{case_id}")
def read_case(case_id: int):
    case = session.query(CaseTable).filter(CaseTable.id == case_id).first()
    return case

@app.post("/case")
# /user?name="이름"&age=10
async def create_case(u_id: str, p_id: int):

    case = CaseTable()
    case.u_id = u_id
    case.p_id = p_id

    session.add(case)
    session.commit()

    return f"{p_id} patient is created"

@app.put("/cases")
# users=[{"id": 1, "name": "이름1", "age": 16},{"id": 2, "name": "이름2", "age": 20}]
async def update_cases(cases: List[Case]):

    for i in cases:
        case = session.query(CaseTable).filter(CaseTable.id == i.id).first()
        case.u_id = i.u_id
        case.p_id = i.p_id
        session.commit()

    return f"{case[0].name} patient is updated"


@app.delete("/case")
async def delete_cases(caseid: int):

    case = session.query(CaseTable).filter(CaseTable.id == caseid).delete()
    session.commit()

    return f"pateint is deleted"
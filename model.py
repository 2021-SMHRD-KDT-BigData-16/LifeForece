# coding: utf-8
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from db import Base
from db import engine


class CaseTable(Base):
    __tablename__ = 'caseinfo'
    u_id = Column(String(45), primary_key=True)
    p_id = Column(Integer, primary_key=True)
    p_score = Column(Integer, nullable=True)
    p_SOFA = Column(Integer, nullable=True)
    p_MEWS = Column(Integer, nullable=True)
    p_cmt = Column(String(45), nullable=True)
    

class Case(BaseModel):
    u_id   : str
    p_id : int
    p_score  : int
    p_SOFA : int
    p_MEWS : int
    p_cmt :  str
    
#p_id = Column(Float,ForeignKey('caseinfo.p_id', name="fk_casevital_caseinfo_u_id", ondelete='CASCADE'))

class CaseVital(Base):
    __tablename__ = 'casevital'
    v_sequence = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer,nullable=False)
    rec_time = Column(String(45), nullable=True)
    age = Column(Integer, nullable=True)    
    ICUtype = Column(Float, nullable=True)
    ALP = Column(Float, nullable=True)
    ALT = Column(Float, nullable=True)
    AST = Column(Float, nullable=True)
    Albumin = Column(Float, nullable=True)
    BUN = Column(Float, nullable=True)
    Bilirubin = Column(Float, nullable=True)
    Cholesterol = Column(Float, nullable=True)
    Creatinine = Column(Float, nullable=True)
    FiO2 = Column(Float, nullable=True)
    GCS = Column(Float, nullable=True)
    Glucose = Column(Float, nullable=True)
    HCO3 = Column(Float, nullable=True)
    HCT = Column(Float, nullable=True)
    HR = Column(Float, nullable=True)
    K = Column(Float, nullable=True)
    Lactate = Column(Float, nullable=True)
    Mg = Column(Float, nullable=True)
    Na = Column(Float, nullable=True)
    PaCO2 = Column(Float, nullable=True)
    PaO2 = Column(Float, nullable=True)
    Platelets = Column(Float, nullable=True)
    RR = Column(Float, nullable=True)
    SPO2 = Column(Float, nullable=True)
    BT = Column(Float, nullable=True)
    TroponinI = Column(Float, nullable=True)
    TroponinT = Column(Float, nullable=True)
    Urine = Column(Float, nullable=True)
    WBC = Column(Float, nullable=True)
    pH = Column(Float, nullable=True)
    MechVent = Column(Float, nullable=True)
    SBP = Column(Float, nullable=True)
    DBP = Column(Float, nullable=True)
    MBP = Column(Float, nullable=True)
    male = Column(Float, nullable=True)
    female = Column(Float, nullable=True)    

    

class Vital(BaseModel):
    v_sequence: int
    p_id: int
    rec_time: str
    age: int    
    ICUtype: float
    ALP: float
    ALT: float
    AST: float
    Albumin: float
    BUN: float
    Bilirubin: float
    Cholesterol: float
    Creatinine: float
    FiO2: float
    GCS: float
    Glucose: float
    HCO3: float
    HCT: float
    HR: float
    K: float
    Lactate: float
    Mg: float
    Na: float
    PaCO2: float
    PaO2: float
    Platelets: float
    RR: float
    SPO2: float
    BT: float
    TroponinI: float
    TroponinT: float
    Urine: float
    WBC: float
    pH: float
    MechVent: float
    SBP: float
    DBP: float
    MBP: float
    male: float
    female: float  

#class UserTable(Base):
#    __tablename__ = 'user'
#    id = Column(Integer, primary_key=True, autoincrement=True)
#    name = Column(String(45), nullable=True)
#    age = Column(Integer)


#class User(BaseModel):
#    id   : int
#    name : str
#    age  : int


def main():
    # Table 없으면 생성
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()
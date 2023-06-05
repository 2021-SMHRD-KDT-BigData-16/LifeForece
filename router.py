from fastapi import APIRouter
from sqlalchemy.orm import Session
from model import CaseTable, Case, CaseVital, Vital
from db import session

router= APIRouter()
from fastapi import FastAPI
from pydantic import BaseModel
from gemini_utils import get_home_plan, get_party_plan, get_jewelry_plan
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="PocketSmart - Vetri Thiran Thittam")

class HomeRequest(BaseModel):
    budget: str
    style: str

class PartyRequest(BaseModel):
    event_type: str
    budget: str
    guests: int

class JewelryRequest(BaseModel):
    outfit: str
    budget: str

@app.get("/")
def home():
    return {"message": "PocketSmart AI is Running!"}

@app.post("/plan-home")
def plan_home(req: HomeRequest):
    result = get_home_plan(req.budget, req.style)
    return {"plan": result}

@app.post("/plan-party")
def plan_party(req: PartyRequest):
    result = get_party_plan(req.event_type, req.budget, req.guests)
    return {"plan": result}

@app.post("/plan-jewelry")
def plan_jewelry(req: JewelryRequest):
    result = get_jewelry_plan(req.outfit, req.budget)
    return {"plan": result}

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "PocketSmart AI Running"}

@app.post("/budget/")
def budget(amount: int):
    return {"budget": amount, "saving": amount*0.2, "expense": amount*0.8}

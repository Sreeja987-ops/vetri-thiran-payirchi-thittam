# main.py - PocketSmart AI Full Working App - FIXED
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import os
from dotenv import load_dotenv
from datetime import datetime

from models import HomeBudgetInput, PartyBudgetInput, JewelryBudgetInput
from gemini_utils import get_home_recommendations, get_party_recommendations, get_jewelry_recommendations
from auth import create_user, authenticate_user, create_access_token, decode_token, users_db, active_sessions, user_history, save_to_history

load_dotenv()
app = FastAPI(title="PocketSmart AI")

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token: return None
    username = decode_token(token)
    if username and username in users_db: return users_db[username]
    return None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_current_user(request)
    html = f"""<html><head><title>PocketSmart AI</title>
    <style>body{{font-family:Arial;background:#f5f5f5;text-align:center;padding:50px}}
  .card{{background:white;padding:30px;border-radius:15px;max-width:600px;margin:auto;box-shadow:0 5px 15px rgba(0,0,0,0.1)}}
    a{{padding:10px 20px;background:#6c5ce7;color:white;text-decoration:none;border-radius:8px;margin:5px;display:inline-block}}</style></head><body>
    <div class='card'><h1>🛍️ PocketSmart AI</h1><p>Your Smart Budget Assistant</p>
    <br><a href='/register'>Register</a> <a href='/login'>Login</a> <a href='/dashboard'>Dashboard</a><br><br><p>✅ Server Running!</p></div></body></html>"""
    return HTMLResponse(html)

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    html = """<html><head><title>Register</title>
    <style>body{font-family:Arial;background:#f5f5f5;padding:50px}
  .card{background:white;padding:30px;border-radius:15px;max-width:400px;margin:auto}
    input{width:100%;padding:10px;margin:8px 0;border:1px solid #ddd;border-radius:8px}
    button{width:100%;padding:12px;background:#6c5ce7;color:white;border:none;border-radius:8px;cursor:pointer}</style></head><body>
    <div class='card'><h2>Register</h2><form method='post'>
    <input name='username' placeholder='Username' required>
    <input name='email' placeholder='Email' required>
    <input type='password' name='password' placeholder='Password' required>
    <button type='submit'>Create Account</button></form><br><a href='/login'>Login</a></div></body></html>"""
    return HTMLResponse(html)

@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    user = create_user(username, email, password)
    if not user: return HTMLResponse("<h3>Username exists! <a href='/register'>Try again</a></h3>", status_code=400)
    return RedirectResponse("/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    html = """<html><head><title>Login</title>
    <style>body{font-family:Arial;background:#f5f5f5;padding:50px}
  .card{background:white;padding:30px;border-radius:15px;max-width:400px;margin:auto}
    input{width:100%;padding:10px;margin:8px 0;border:1px solid #ddd;border-radius:8px}
    button{width:100%;padding:12px;background:#00b894;color:white;border:none;border-radius:8px;cursor:pointer}</style></head><body>
    <div class='card'><h2>Login</h2><form method='post'>
    <input name='username' placeholder='Username' required>
    <input type='password' name='password' placeholder='Password' required>
    <button type='submit'>Login</button></form><br><a href='/register'>Register</a></div></body></html>"""
    return HTMLResponse(html)

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user: return HTMLResponse("<h3>Invalid login! <a href='/login'>Try again</a></h3>", status_code=401)
    token = create_access_token({"sub": username})
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    active_sessions[username] = {"login_time": datetime.utcnow().isoformat()}
    return response

@app.get("/logout")
async def logout():
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("access_token")
    return resp

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user: return RedirectResponse("/login", status_code=302)
    history = user_history.get(user["username"], [])[-5:][::-1]
    html = f"""<html><head><title>Dashboard</title>
    <style>body{{font-family:Arial;background:#f5f5f5;padding:20px}}
  .card{{background:white;padding:20px;border-radius:15px;max-width:800px;margin:20px auto}}
    a{{padding:10px 15px;background:#6c5ce7;color:white;text-decoration:none;border-radius:8px;margin:5px;display:inline-block}}</style></head><body>
    <div class='card'><h2>Welcome {user['username']}! 👋</h2><p>Email: {user['email']}</p>
    <a href='/home-planner'>🏠 Home Planner</a><a href='/party-planner'>🎉 Party Planner</a><a href='/jewelry-planner'>💍 Jewelry Planner</a>
    <a href='/history'>📜 History</a><a href='/logout' style='background:#d63031'>Logout</a></div>
    <div class='card'><h3>Recent History - {len(history)} plans</h3></div></body></html>"""
    return HTMLResponse(html)

@app.get("/home-planner", response_class=HTMLResponse)
async def home_planner_page(request: Request):
    user = get_current_user(request)
    if not user: return RedirectResponse("/login", status_code=302)
    html = """<html><head><title>Home Planner</title>
    <style>body{font-family:Arial;background:#f5f5f5;padding:20px}
  .card{background:white;padding:25px;border-radius:15px;max-width:600px;margin:auto}
    input,select{width:100%;padding:10px;margin:6px 0;border:1px solid #ddd;border-radius:8px}
    button{width:100%;padding:12px;background:#6c5ce7;color:white;border:none;border-radius:8px;cursor:pointer;margin-top:10px}
    #result{margin-top:20px;padding:15px;background:#f1f2f6;border-radius:10px;white-space:pre-wrap}</style></head><body>
    <div class='card'><h2>🏠 Home Interior Planner</h2>
    <input id='budget' type='number' placeholder='Total Budget' value='50000'>
    <input id='lights' type='number' placeholder='Num Lights' value='4'>
    <input id='fans' type='number' placeholder='Num Fans' value='3'>
    <input id='furniture' type='number' placeholder='Furniture sets' value='1'>
    <input id='dining' type='number' placeholder='Dining Tables' value='1'>
    <input id='extra' placeholder='Extra needs'><button onclick='generate()'>Generate Recommendations</button>
    <div id='result'>Result will appear here...</div><br><a href='/dashboard'>Back</a></div>
    <script>async function generate(){const data={total_budget:parseFloat(document.getElementById('budget').value),num_lights:parseInt(document.getElementById('lights').value),num_fans:parseInt(document.getElementById('fans').value),num_furniture:parseInt(document.getElementById('furniture').value),num_dining_tables:parseInt(document.getElementById('dining').value),has_living_room:true,has_kitchen:true,has_bedroom:true,additional_requirements:document.getElementById('extra').value};document.getElementById('result').innerText='⏳ Generating...';const res=await fetch('/generate-home',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const json=await res.json();document.getElementById('result').innerHTML='<h3>Recommendations:</h3><pre>'+JSON.stringify(json,null,2)+'</pre>';}</script></body></html>"""
    return HTMLResponse(html)

@app.post("/generate-home")
async def generate_home(request: Request):
    user = get_current_user(request)
    if not user: return JSONResponse({"error":"Login first"},status_code=401)
    data = await request.json()
    budget_input = HomeBudgetInput(**data)
    result = get_home_recommendations(budget_input)
    save_to_history(user["username"],"home",data,result)
    return JSONResponse(result)

@app.get("/party-planner", response_class=HTMLResponse)
async def party_planner_page(request: Request):
    user = get_current_user(request)
    if not user: return RedirectResponse("/login", status_code=302)
    html = """<html><head><title>Party Planner</title><style>body{font-family:Arial;background:#f5f5f5;padding:20px}
  .card{background:white;padding:25px;border-radius:15px;max-width:600px;margin:auto}
    input,select{width:100%;padding:10px;margin:6px 0;border:1px solid #ddd;border-radius:8px}
    button{width:100%;padding:12px;background:#e17055;color:white;border:none;border-radius:8px;cursor:pointer;margin-top:10px}
    #result{margin-top:20px;padding:15px;background:#f1f2f6;border-radius:10px}</style></head><body>
    <div class='card'><h2>🎉 Party Planner</h2><input id='budget' type='number' value='30000'><input id='guests' type='number' value='20'>
    <select id='event'><option value='birthday'>Birthday</option><option value='wedding'>Wedding</option></select>
    <select id='venue'><option value='home'>Home</option><option value='banquet'>Banquet Hall</option></select>
    <select id='food'><option value='veg'>Veg</option><option value='non-veg'>Non-Veg</option><option value='both'>Both</option></select>
    <button onclick='generate()'>Generate Party Plan</button><div id='result'>Result here...</div><br><a href='/dashboard'>Back</a></div>
    <script>async function generate(){const data={total_budget:parseFloat(document.getElementById('budget').value),guest_count:parseInt(document.getElementById('guests').value),event_type:document.getElementById('event').value,venue_type:document.getElementById('venue').value,food_preference:document.getElementById('food').value,decoration_theme:'simple'};document.getElementById('result').innerText='⏳ Generating...';const res=await fetch('/generate-party',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const json=await res.json();document.getElementById('result').innerHTML='<pre>'+JSON.stringify(json,null,2)+'</pre>';}</script></body></html>"""
    return HTMLResponse(html)

@app.post("/generate-party")
async def generate_party(request: Request):
    user = get_current_user(request)
    if not user: return JSONResponse({"error":"Login first"},status_code=401)
    data = await request.json()
    party_input = PartyBudgetInput(**data)
    result = get_party_recommendations(party_input)
    save_to_history(user["username"],"party",data,result)
    return JSONResponse(result)

@app.get("/jewelry-planner", response_class=HTMLResponse)
async def jewelry_planner_page(request: Request):
    user = get_current_user(request)
    if not user: return RedirectResponse("/login", status_code=302)
    html = """<html><head><title>Jewelry Planner</title><style>body{font-family:Arial;background:#f5f5f5;padding:20px}
  .card{background:white;padding:25px;border-radius:15px;max-width:600px;margin:auto}
    input,select{width:100%;padding:10px;margin:6px 0;border:1px solid #ddd;border-radius:8px}
    button{width:100%;padding:12px;background:#fdcb6e;color:#333;border:none;border-radius:8px;cursor:pointer;margin-top:10px;font-weight:bold}
    #result{margin-top:20px;padding:15px;background:#f1f2f6;border-radius:10px}</style></head><body>
    <div class='card'><h2>💍 Jewelry Planner</h2><input id='budget' type='number' value='20000'>
    <select id='occasion'><option value='wedding'>Wedding</option><option value='festival'>Festival</option></select>
    <select id='style'><option value='traditional'>Traditional</option><option value='modern'>Modern</option></select>
    <select id='metal'><option value='gold'>Gold</option><option value='silver'>Silver</option></select>
    <input id='extra' placeholder='Extra notes'><button onclick='generate()'>Generate Jewelry Suggestions</button>
    <div id='result'>Result here...</div><br><a href='/dashboard'>Back</a></div>
    <script>async function generate(){const data={total_budget:parseFloat(document.getElementById('budget').value),occasion:document.getElementById('occasion').value,style_preference:document.getElementById('style').value,metal_preference:document.getElementById('metal').value,additional_requirements:document.getElementById('extra').value};document.getElementById('result').innerText='⏳ Generating...';const res=await fetch('/generate-jewelry',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const json=await res.json();document.getElementById('result').innerHTML='<pre>'+JSON.stringify(json,null,2)+'</pre>';}</script></body></html>"""
    return HTMLResponse(html)

@app.post("/generate-jewelry")
async def generate_jewelry(request: Request):
    user = get_current_user(request)
    if not user: return JSONResponse({"error":"Login first"},status_code=401)
    data = await request.json()
    jewelry_input = JewelryBudgetInput(**data)
    result = get_jewelry_recommendations(jewelry_input)
    save_to_history(user["username"],"jewelry",data,result)
    return JSONResponse(result)

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    user = get_current_user(request)
    if not user: return RedirectResponse("/login", status_code=302)
    hist = user_history.get(user["username"], [])[::-1]
    html = f"<html><body style='font-family:Arial;padding:20px'><h2>📜 History for {user['username']}</h2><p>Total: {len(hist)}</p><pre>{str(hist[:2])[:2000]}</pre><br><a href='/dashboard'>Back</a></body></html>"
    return HTMLResponse(html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
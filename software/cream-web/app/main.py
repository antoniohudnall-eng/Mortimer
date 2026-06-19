from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import sqlite3
import json
import hashlib
import secrets
import uvicorn
from pathlib import Path

app = FastAPI(title="CREAM - Real Estate Management", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="/root/.openclaw/workspace/cream-web/static"), name="static")
templates = Jinja2Templates(directory="/root/.openclaw/workspace/cream-web/templates")

# Database setup
DB_PATH = "/root/.openclaw/workspace/cream-web/cream.db"

def init_db():
    """Initialize database with auth and CREAM tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table with auth
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            company TEXT,
            license_number TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Sessions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Leads table
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            source TEXT,
            status TEXT DEFAULT 'new',
            temperature TEXT DEFAULT 'cold',
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            notes TEXT,
            ai_score INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Appointments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lead_id INTEGER,
            title TEXT,
            datetime TEXT,
            location TEXT,
            status TEXT DEFAULT 'scheduled',
            outcome TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    ''')
    
    # Transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lead_id INTEGER,
            address TEXT,
            sale_price REAL,
            commission_rate REAL,
            commission_amount REAL,
            expenses REAL,
            net_profit REAL,
            status TEXT DEFAULT 'prospect',
            closing_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    ''')
    
    # Farming campaigns table
    c.execute('''
        CREATE TABLE IF NOT EXISTS farming_campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            zip_code TEXT,
            target_count INTEGER,
            sent_count INTEGER DEFAULT 0,
            response_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Demo user (for testing)
    demo_hash = hashlib.sha256("demo123".encode()).hexdigest()
    c.execute('''
        INSERT OR IGNORE INTO users (id, email, password_hash, name, company)
        VALUES (1, 'demo@cream.app', ?, 'Demo Agent', 'Demo Realty')
    ''', (demo_hash,))
    
    # Demo data
    c.execute('''
        INSERT OR IGNORE INTO leads (id, user_id, name, email, phone, source, status, temperature, city, ai_score)
        VALUES 
        (1, 1, 'Sarah Johnson', 'sarah@email.com', '555-0101', 'Referral', 'hot', 'hot', 'Pasadena', 85),
        (2, 1, 'Mike Chen', 'mike@email.com', '555-0102', 'Website', 'warm', 'warm', 'Los Angeles', 72),
        (3, 1, 'Lisa Park', 'lisa@email.com', '555-0103', 'Open House', 'cold', 'cold', 'Santa Monica', 45)
    ''')
    
    conn.commit()
    conn.close()

# Auth Models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    company: Optional[str] = None

# Auth functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_session(user_id: int) -> str:
    session_id = secrets.token_urlsafe(32)
    expires = (datetime.now() + timedelta(days=7)).isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO sessions (id, user_id, expires_at)
        VALUES (?, ?, ?)
    ''', (session_id, user_id, expires))
    conn.commit()
    conn.close()
    
    return session_id

def verify_session(session_id: str) -> Optional[int]:
    if not session_id:
        return None
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT user_id FROM sessions 
        WHERE id = ? AND expires_at > ?
    ''', (session_id, datetime.now().isoformat()))
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else None

def get_current_user(request: Request) -> Optional[dict]:
    session_id = request.cookies.get("session_id")
    user_id = verify_session(session_id)
    
    if not user_id:
        return None
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    
    return dict(row) if row else None

# Routes
@app.on_event("startup")
async def startup():
    init_db()
    print("CREAM database initialized")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main app with auth overlay"""
    user = get_current_user(request)
    if user:
        return templates.TemplateResponse("app.html", {"request": request, "user": user})
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    """Main CREAM app (requires auth)"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("app.html", {"request": request, "user": user})

# Auth API
@app.post("/api/auth/login")
async def login(request: Request, login_data: LoginRequest):
    """Login endpoint"""
    password_hash = hash_password(login_data.password)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, name, email, company FROM users 
        WHERE email = ? AND password_hash = ? AND is_active = 1
    ''', (login_data.email, password_hash))
    user = c.fetchone()
    
    if user:
        # Update last login
        c.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                 (datetime.now().isoformat(), user[0]))
        conn.commit()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_id = create_session(user[0])
    
    response = JSONResponse({
        "success": True,
        "user": {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "company": user[3]
        }
    })
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=604800)
    return response

@app.post("/api/auth/register")
async def register(register_data: RegisterRequest):
    """Register new user"""
    password_hash = hash_password(register_data.password)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO users (email, password_hash, name, company)
            VALUES (?, ?, ?, ?)
        ''', (register_data.email, password_hash, register_data.name, register_data.company))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        session_id = create_session(user_id)
        
        response = JSONResponse({
            "success": True,
            "user": {
                "id": user_id,
                "name": register_data.name,
                "email": register_data.email
            }
        })
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=604800)
        return response
        
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")

@app.post("/api/auth/logout")
async def logout(request: Request):
    """Logout endpoint"""
    session_id = request.cookies.get("session_id")
    
    if session_id:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
        conn.commit()
        conn.close()
    
    response = JSONResponse({"success": True})
    response.delete_cookie(key="session_id")
    return response

# Dashboard API
@app.get("/api/dashboard")
async def dashboard(request: Request):
    """Get dashboard stats"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count stats
    c.execute('SELECT COUNT(*) FROM leads WHERE user_id = ?', (user['id'],))
    lead_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM appointments WHERE user_id = ? AND status = ?', (user['id'], 'scheduled'))
    appointment_count = c.fetchone()[0]
    
    c.execute('SELECT SUM(net_profit) FROM transactions WHERE user_id = ? AND status = ?', 
              (user['id'], 'closed'))
    revenue = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM transactions WHERE user_id = ? AND status = ?', 
              (user['id'], 'closed'))
    deals_closed = c.fetchone()[0]
    
    conn.close()
    
    conversion_rate = round((deals_closed / lead_count * 100) if lead_count > 0 else 0, 1)
    
    return {
        "leads": lead_count,
        "appointments": appointment_count,
        "revenue": revenue,
        "deals_closed": deals_closed,
        "conversion_rate": conversion_rate,
        "tasks": [
            "Follow up with 3 leads",
            "Send farming letter to Modoc County"
        ]
    }

# Leads API
@app.get("/api/leads")
async def get_leads(request: Request, status: Optional[str] = None):
    """Get leads for user"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if status:
        c.execute('SELECT * FROM leads WHERE user_id = ? AND status = ? ORDER BY created_at DESC', 
                  (user['id'], status))
    else:
        c.execute('SELECT * FROM leads WHERE user_id = ? ORDER BY created_at DESC', (user['id'],))
    
    leads = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {"leads": leads}

@app.post("/api/leads")
async def create_lead(request: Request, lead_data: dict):
    """Create new lead"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO leads (user_id, name, email, phone, source, status, temperature, city, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user['id'], lead_data.get('name'), lead_data.get('email'), lead_data.get('phone'),
          lead_data.get('source', 'Unknown'), lead_data.get('status', 'new'),
          lead_data.get('temperature', 'cold'), lead_data.get('city'), lead_data.get('notes')))
    conn.commit()
    lead_id = c.lastrowid
    conn.close()
    
    return {"success": True, "id": lead_id}

# Health check
@app.get("/api/health")
async def health():
    return {"status": "healthy", "version": "2.0.0", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8084)

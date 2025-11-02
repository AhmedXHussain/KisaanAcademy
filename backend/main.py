from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import sqlite3
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import os

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads variables from .env file
    print("✓ Loaded environment variables from .env file")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually")

# App will be created after lifespan definition

# Database initialization
DATABASE = "kisaan_academy.db"

def migrate_database(cursor):
    """Add missing columns to existing tables if they don't exist."""
    try:
        # Check if wiki_url column exists in wiki_articles
        cursor.execute("PRAGMA table_info(wiki_articles)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'wiki_url' not in columns:
            cursor.execute('ALTER TABLE wiki_articles ADD COLUMN wiki_url TEXT')
            print("✓ Added wiki_url column to wiki_articles table")
    except Exception as e:
        print(f"Migration warning: {e}")

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            region TEXT,
            language TEXT DEFAULT 'ur',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_ur TEXT NOT NULL,
            title_en TEXT NOT NULL,
            description_ur TEXT,
            description_en TEXT,
            category TEXT,
            video_url TEXT,
            content_ur TEXT,
            content_en TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(title_ur, title_en)
        )
    ''')
    
    # Market prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL,
            region TEXT NOT NULL,
            price_per_kg REAL NOT NULL,
            mandi_name TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Weather alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT,
            message_ur TEXT,
            message_en TEXT,
            valid_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Pest alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pest_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            pest_name_ur TEXT,
            pest_name_en TEXT,
            crop_affected TEXT,
            severity TEXT,
            prevention_ur TEXT,
            prevention_en TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Wiki articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wiki_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_ur TEXT NOT NULL,
            title_en TEXT NOT NULL,
            content_ur TEXT,
            content_en TEXT,
            category TEXT,
            tags TEXT,
            wiki_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(title_ur, title_en)
        )
    ''')
    
    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            language TEXT DEFAULT 'ur',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Migrate existing tables
    migrate_database(cursor)
    conn.commit()
    
    # Insert sample data
    insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    # Sample courses with YouTube video links
    courses = [
        ("ڈرپ اریگیشن کا استعمال", "Drip Irrigation Usage", 
         "ڈرپ اریگیشن کے فوائد اور استعمال کا طریقہ", 
         "Benefits and usage of drip irrigation",
         "sustainable_practices", "https://youtu.be/Xej22GsLLQA?si=PHj6dl6ADtEGCCw1",
         "ڈرپ اریگیشن پانی کے بہتر استعمال کا ایک موثر طریقہ ہے جو پانی کی بچت کرتا ہے اور فصلوں کی بہتر افزائش میں مدد کرتا ہے۔", 
         "Drip irrigation is an effective method for better water usage that saves water and helps in better crop growth."),
        ("کمپوسٹ بنانے کا طریقہ", "How to Make Compost",
         "کھاد بنانے کا آسان طریقہ", 
         "Easy method to make fertilizer",
         "waste_management", "https://youtu.be/_K25WjjCBuw?si=ofVETNZjDqghuH80",
         "کمپوسٹ بنانے کے لیے پودوں کی باقیات، کچرے اور نامیاتی مواد کو مناسب طریقے سے استعمال کریں۔",
         "Use crop residues, waste, and organic materials properly to make compost."),
        ("مٹی کی جانچ", "Soil Testing",
         "مٹی کی صحت کیسے چیک کریں",
         "How to check soil health",
         "sustainable_practices", "https://youtu.be/L6EtmGMJflI?si=7V3Y5w8ItkBzdUGw",
         "مٹی کی جانچ فصل کی بہتری کے لیے ضروری ہے تاکہ آپ صحیح کھاد اور علاج استعمال کر سکیں۔",
         "Soil testing is essential for crop improvement so you can use the right fertilizers and treatments."),
        ("گندم کی کاشت", "Wheat Cultivation",
         "گندم کی کاشت کا مکمل طریقہ کار",
         "Complete guide to wheat cultivation",
         "crop_production", "https://youtu.be/xVO9bjuhB58?si=Cc8nqvcAuIFj5m9M",
         "گندم پاکستان کی اہم ترین فصل ہے۔ اس کی کاشت کے لیے زمین کی تیاری، بیج کی اچھی قسم کا انتخاب، اور وقت پر کاشت بہت ضروری ہے۔",
         "Wheat is Pakistan's most important crop. Land preparation, selecting good seed varieties, and timely sowing are essential."),
        ("چاول کی کاشت", "Rice Cultivation",
         "چاول کی کاشت کے بہترین طریقے",
         "Best methods for rice cultivation",
         "crop_production", "https://youtu.be/FW_bw9jdrlQ?si=zIlptf1nqHRvqAAW",
         "چاول کی کاشت کے لیے پانی کا مناسب انتظام، زمین کی تیاری، اور بیج کا انتخاب بہت اہم ہے۔",
         "Proper water management, land preparation, and seed selection are very important for rice cultivation."),
        ("کپاس کی کاشت", "Cotton Cultivation",
         "کپاس کی کامیاب کاشت کے رہنما اصول",
         "Guiding principles for successful cotton cultivation",
         "crop_production", "https://youtu.be/eN-TqqBQOAk?si=klQi7MA3dkPoEBLx",
         "کپاس کی کاشت کے لیے موسم، زمین کی قسم، اور کیڑوں کا انتظام بہت ضروری ہے۔",
         "Weather, soil type, and pest management are essential for cotton cultivation."),
        ("کیمیائی کھاد کا استعمال", "Chemical Fertilizer Usage",
         "کیمیائی کھادوں کا صحیح استعمال",
         "Proper use of chemical fertilizers",
         "fertilizer_management", "https://youtu.be/y9b2p69CxCk?si=FIItGgzeOtBpMhpW",
         "کیمیائی کھادوں کا صحیح استعمال فصلوں کی پیداوار بڑھاتا ہے لیکن زیادہ استعمال نقصان دہ ہو سکتا ہے۔",
         "Proper use of chemical fertilizers increases crop yield but excessive use can be harmful."),
        ("نامیاتی کھاد", "Organic Fertilizer",
         "نامیاتی کھاد بنانے اور استعمال کرنے کا طریقہ",
         "How to make and use organic fertilizer",
         "fertilizer_management", "https://youtu.be/lofNYAtHYu4?si=Sv78H9e6jyo8VAy1",
         "نامیاتی کھاد ماحول دوست ہے اور مٹی کی صحت کو بہتر بناتی ہے۔",
         "Organic fertilizer is environmentally friendly and improves soil health."),
        ("کیڑے مار ادویات", "Pesticide Usage",
         "کیڑے مار ادویات کا محفوظ استعمال",
         "Safe use of pesticides",
         "pest_management", "https://youtu.be/lJEeGMMcYCI?si=xPnsjDkChLn9GoF6",
         "کیڑے مار ادویات کا محفوظ اور مناسب استعمال فصلوں کو کیڑوں سے بچاتا ہے۔",
         "Safe and proper use of pesticides protects crops from pests."),
        ("پانی کی بچت", "Water Conservation",
         "کھیتی باڑی میں پانی کیسے بچایا جائے",
         "How to save water in farming",
         "resource_management", "https://youtu.be/-evivoRwUZw?si=JBMXsQWJchfMP3Al",
         "پانی کی بچت کے مختلف طریقے جیسے بارش کے پانی کا ذخیرہ، ڈرپ اریگیشن، اور مناسب اریگیشن وقت۔",
         "Various water conservation methods like rainwater harvesting, drip irrigation, and proper irrigation timing."),
        ("فصل کی کٹائی", "Harvesting",
         "فصل کی کٹائی کا صحیح وقت اور طریقہ",
         "Right time and method for harvesting",
         "crop_production", "https://youtu.be/kWd_QnyO3eI?si=3S0fNULnIuWI9ltL",
         "فصل کی کٹائی کا صحیح وقت پیداوار کی کیفیت اور مقدار کو متاثر کرتا ہے۔",
         "The right time for harvesting affects the quality and quantity of yield."),
        ("بیج کی اچھی اقسام", "Quality Seed Varieties",
         "بہتر پیداوار کے لیے بیج کی اقسام کا انتخاب",
         "Selecting seed varieties for better yield",
         "crop_production", "https://youtu.be/Oir1J_CfU9Q?si=tcbiBFgsfyF79H5Y",
         "بیج کی اچھی اقسام کا انتخاب کامیاب فصل کی بنیاد ہے۔",
         "Selecting quality seed varieties is the foundation of a successful crop."),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO courses (title_ur, title_en, description_ur, description_en, category, video_url, content_ur, content_en)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', courses)
    
    # Sample market prices
    prices = [
        ("گندم", "Punjab", 4500.0, "Lahore Mandi"),
        ("چاول", "Punjab", 5500.0, "Lahore Mandi"),
        ("کپاس", "Sindh", 8000.0, "Karachi Mandi"),
        ("گندم", "Sindh", 4600.0, "Hyderabad Mandi"),
        ("چاول", "KPK", 5400.0, "Peshawar Mandi"),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO market_prices (crop_name, region, price_per_kg, mandi_name)
        VALUES (?, ?, ?, ?)
    ''', prices)
    
    # Sample wiki articles with Wikipedia links
    wiki_articles = [
        ("کھیتی باڑی کے فضلے کا انتظام", "Agricultural Waste Management",
         "کھیتی باڑی کے فضلے کو کیسے استعمال کیا جائے۔ فصلوں کی باقیات، جانوروں کا گوبر، اور دیگر نامیاتی مواد کو کمپوسٹ اور بائیوچار میں تبدیل کیا جا سکتا ہے۔",
         "How to utilize agricultural waste. Crop residues, animal manure, and other organic materials can be converted into compost and biochar.",
         "waste_management", "کمپوسٹ, بائیوچار, کھاد", "https://en.wikipedia.org/wiki/Agricultural_waste"),
        ("پانی کی بچت", "Water Conservation",
         "پانی کے موثر استعمال کے طریقے۔ بارش کے پانی کا ذخیرہ، ڈرپ اریگیشن، اور موسمی اریگیشن سے پانی کی بچت ہو سکتی ہے۔",
         "Methods for efficient water usage. Rainwater harvesting, drip irrigation, and seasonal irrigation can save water.",
         "resource_management", "پانی, بچت, اریگیشن", "https://en.wikipedia.org/wiki/Water_conservation"),
        ("مٹی کی صحت", "Soil Health",
         "مٹی کی صحت کو برقرار رکھنے کے طریقے۔ نامیاتی کھاد، کروپ روٹیشن، اور مناسب زمین کی تیاری مٹی کی صحت کو بہتر بناتی ہے۔",
         "Methods to maintain soil health. Organic fertilizers, crop rotation, and proper land preparation improve soil health.",
         "sustainable_practices", "مٹی, صحت, نامیاتی", "https://en.wikipedia.org/wiki/Soil_health"),
        ("کھیتی باڑی میں ماحولیاتی تبدیلی", "Climate Change in Agriculture",
         "ماحولیاتی تبدیلی کا کھیتی باڑی پر اثر اور اس سے نمٹنے کے طریقے۔",
         "Impact of climate change on agriculture and methods to deal with it.",
         "sustainable_practices", "موسم, تبدیلی, ماحول", "https://en.wikipedia.org/wiki/Climate_change_and_agriculture"),
        ("آرگینک کھیتی باڑی", "Organic Farming",
         "آرگینک کھیتی باڑی کے اصول اور طریقے۔ کیمیائی کھادوں اور کیڑے مار ادویات کے بغیر قدرتی طریقوں سے کھیتی باڑی۔",
         "Principles and methods of organic farming. Farming using natural methods without chemical fertilizers and pesticides.",
         "sustainable_practices", "نامیاتی, قدرتی, ماحول دوست", "https://en.wikipedia.org/wiki/Organic_farming"),
        ("بائیو ڈائیورسٹی", "Biodiversity",
         "کھیتی باڑی میں حیاتیاتی تنوع کی اہمیت۔ مختلف فصلوں اور جانوروں کی اقسام کا برقرار رکھنا۔",
         "Importance of biodiversity in agriculture. Maintaining different varieties of crops and animals.",
         "sustainable_practices", "تنوع, حیاتیات, فصل", "https://en.wikipedia.org/wiki/Agricultural_biodiversity"),
        ("ڈرپ اریگیشن", "Drip Irrigation",
         "ڈرپ اریگیشن نظام کی تفصیلات۔ پانی کی بچت اور موثر اریگیشن کا بہترین طریقہ۔",
         "Details of drip irrigation system. The best method for water saving and efficient irrigation.",
         "resource_management", "اریگیشن, پانی, بچت", "https://en.wikipedia.org/wiki/Drip_irrigation"),
        ("کمپوسٹ", "Compost",
         "کمپوسٹ بنانے کا طریقہ اور اس کے فوائد۔ نامیاتی کچرے کو مفید کھاد میں تبدیل کرنا۔",
         "Method of making compost and its benefits. Converting organic waste into useful fertilizer.",
         "waste_management", "کمپوسٹ, کھاد, نامیاتی", "https://en.wikipedia.org/wiki/Compost"),
        ("کروپ روٹیشن", "Crop Rotation",
         "کروپ روٹیشن کی اہمیت اور طریقہ کار۔ مختلف فصلوں کی باری باری کاشت سے مٹی کی صحت بہتر ہوتی ہے۔",
         "Importance and methodology of crop rotation. Alternating different crops improves soil health.",
         "sustainable_practices", "فصل, باری, صحت", "https://en.wikipedia.org/wiki/Crop_rotation"),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO wiki_articles (title_ur, title_en, content_ur, content_en, category, tags, wiki_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', wiki_articles)
    
    # Sample weather alerts
    weather_alerts = [
        ("Punjab", "heatwave", "high", "اگلے 3 دنوں میں گرمی کی لہر متوقع ہے", "Heatwave expected in next 3 days", None),
        ("Sindh", "heavy_rain", "medium", "بارش کی پیش گوئی", "Rain forecast", None)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO weather_alerts (region, alert_type, severity, message_ur, message_en, valid_until)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', weather_alerts)
    
    # Pest alerts are populated from database migration/update scripts
    # Comprehensive pest data is added separately to avoid duplicates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Kisaan Academy API",
    description="API for Kisaan Academy - Agricultural Learning Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    region: Optional[str] = None
    language: str = "ur"

class ChatMessage(BaseModel):
    user_id: Optional[int] = None
    question: str
    language: str = "ur"

class MarketPriceFilter(BaseModel):
    crop_name: Optional[str] = None
    region: Optional[str] = None

# API Routes

@app.get("/")
async def root():
    return {"message": "Kisaan Academy API", "status": "running"}

# User endpoints
@app.post("/api/users")
async def create_user(user: UserCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, email, phone, region, language)
        VALUES (?, ?, ?, ?, ?)
    ''', (user.name, user.email, user.phone, user.region, user.language))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": user_id, "message": "User created successfully"}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    raise HTTPException(status_code=404, detail="User not found")

# Course endpoints
@app.get("/api/courses")
async def get_courses(language: str = "ur"):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses ORDER BY created_at DESC')
    courses = cursor.fetchall()
    conn.close()
    
    # Remove duplicates by title_en to ensure unique courses
    seen_titles = set()
    result = []
    for course in courses:
        title_key = course["title_en"]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            result.append({
                "id": course["id"],
                "title": course[f"title_{language}"] if language in ["ur", "en"] else course["title_ur"],
                "description": course[f"description_{language}"] if language in ["ur", "en"] else course["description_ur"],
                "category": course["category"],
                "video_url": course["video_url"],
                "content": course[f"content_{language}"] if language in ["ur", "en"] else course["content_ur"],
                "created_at": course["created_at"]
            })
    return result

@app.get("/api/courses/{course_id}")
async def get_course(course_id: int, language: str = "ur"):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()
    conn.close()
    
    if course:
        return {
            "id": course["id"],
            "title": course[f"title_{language}"] if language in ["ur", "en"] else course["title_ur"],
            "description": course[f"description_{language}"] if language in ["ur", "en"] else course["description_ur"],
            "category": course["category"],
            "video_url": course["video_url"],
            "content": course[f"content_{language}"] if language in ["ur", "en"] else course["content_ur"],
            "created_at": course["created_at"]
        }
    raise HTTPException(status_code=404, detail="Course not found")

# Market price endpoints
@app.get("/api/market-prices")
async def get_market_prices(crop_name: Optional[str] = None, region: Optional[str] = None, update: bool = False):
    """
    Get market prices from database.
    If update=true, fetches latest data from RapidAPI first.
    """
    # Optionally fetch from RapidAPI if requested
    if update:
        try:
            from market_integration import fetch_market_prices_from_api
            prices = fetch_market_prices_from_api()
            print(f"✓ Updated market prices from RapidAPI: {len(prices)} commodities")
        except ImportError:
            pass  # market_integration not available
        except Exception as e:
            print(f"Error updating market prices from API: {e}")
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = 'SELECT * FROM market_prices WHERE 1=1'
    params = []
    
    if crop_name:
        query += ' AND crop_name LIKE ?'
        params.append(f"%{crop_name}%")
    if region:
        query += ' AND region = ?'
        params.append(region)
    
    query += ' ORDER BY recorded_at DESC LIMIT 100'
    
    cursor.execute(query, params)
    prices = cursor.fetchall()
    conn.close()
    
    return [dict(price) for price in prices]

@app.post("/api/market-prices/update")
async def update_market_prices():
    """
    Manually trigger update of market prices from RapidAPI
    """
    try:
        from market_integration import fetch_market_prices_from_api
        commodities = fetch_market_prices_from_api()
        return {
            "status": "success",
            "message": f"Updated {len(commodities)} commodity prices",
            "count": len(commodities)
        }
    except ImportError:
        raise HTTPException(status_code=500, detail="Market integration module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating prices: {str(e)}")

@app.get("/api/market-prices/forecast/{crop_name}")
async def get_price_forecast(crop_name: str, region: Optional[str] = None):
    # Simple forecasting - in production, use Prophet or ARIMA
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = 'SELECT price_per_kg, recorded_at FROM market_prices WHERE crop_name = ?'
    params = [crop_name]
    
    if region:
        query += ' AND region = ?'
        params.append(region)
    
    query += ' ORDER BY recorded_at DESC LIMIT 30'
    
    cursor.execute(query, params)
    prices = cursor.fetchall()
    conn.close()
    
    if not prices:
        return {"forecast": "Insufficient data", "trend": "neutral"}
    
    # Simple trend calculation
    recent_avg = sum(p["price_per_kg"] for p in prices[:10]) / min(10, len(prices))
    older_avg = sum(p["price_per_kg"] for p in prices[10:20]) / max(1, len(prices) - 10)
    
    trend = "increasing" if recent_avg > older_avg else "decreasing" if recent_avg < older_avg else "stable"
    
    return {
        "crop_name": crop_name,
        "region": region or "All",
        "current_price": prices[0]["price_per_kg"],
        "forecast": recent_avg * 1.05 if trend == "increasing" else recent_avg * 0.95,
        "trend": trend,
        "confidence": "medium"
    }

# Weather alerts endpoints
@app.get("/api/weather-alerts")
async def get_weather_alerts(region: Optional[str] = None, language: str = "ur", update: bool = False):
    """
    Get weather alerts from database.
    If update=true, fetches latest data from Weather API first.
    Automatically fetches from API if no valid alerts exist in database.
    """
    # Check if we have valid alerts in database
    conn_check = sqlite3.connect(DATABASE)
    cursor_check = conn_check.cursor()
    cursor_check.execute('SELECT COUNT(*) FROM weather_alerts WHERE valid_until IS NULL OR valid_until > datetime("now")')
    count = cursor_check.fetchone()[0]
    conn_check.close()
    
    # Fetch from API if update requested or no valid alerts in database
    if update or count == 0:
        try:
            from weather_integration import fetch_weather_alerts_from_api, update_weather_alerts_in_db
            alerts = fetch_weather_alerts_from_api(region)
            if alerts:
                update_weather_alerts_in_db(alerts)
                print(f"✓ Updated {len(alerts)} weather alerts from API")
        except ImportError:
            pass  # weather_integration not available
        except Exception as e:
            print(f"Error updating weather alerts from API: {e}")
    
    # Get from database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Return all alerts, not just valid ones, to ensure we have data to show
    query = 'SELECT * FROM weather_alerts WHERE 1=1'
    params = []
    
    if region:
        query += ' AND region = ?'
        params.append(region)
    
    query += ' ORDER BY created_at DESC LIMIT 20'
    
    cursor.execute(query, params)
    alerts = cursor.fetchall()
    conn.close()
    
    result = []
    for alert in alerts:
        # Get message in requested language, fallback to Urdu
        message_key = f"message_{language}" if language in ["ur", "en"] else "message_ur"
        message = alert[message_key] if message_key in alert.keys() else (alert["message_ur"] if "message_ur" in alert.keys() else "No message available")
        
        result.append({
            "id": alert["id"],
            "region": alert["region"],
            "alert_type": alert["alert_type"],
            "severity": alert["severity"] if "severity" in alert.keys() else "medium",
            "message": message,
            "created_at": alert["created_at"]
        })
    
    # If no results and we didn't fetch from API, try one more time
    if not result:
        try:
            from weather_integration import fetch_weather_alerts_from_api, update_weather_alerts_in_db
            alerts = fetch_weather_alerts_from_api(region)
            if alerts:
                update_weather_alerts_in_db(alerts)
                # Re-query after update
                conn = sqlite3.connect(DATABASE)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                alerts = cursor.fetchall()
                conn.close()
                result = []
                for alert in alerts:
                    message_key = f"message_{language}" if language in ["ur", "en"] else "message_ur"
                    message = alert[message_key] if message_key in alert.keys() else (alert["message_ur"] if "message_ur" in alert.keys() else "No message available")
                    result.append({
                        "id": alert["id"],
                        "region": alert["region"],
                        "alert_type": alert["alert_type"],
                        "severity": alert["severity"] if "severity" in alert.keys() else "medium",
                        "message": message,
                        "created_at": alert["created_at"]
                    })
        except Exception as e:
            print(f"Error fetching weather alerts: {e}")
    
    return result

# Endpoint to manually update weather alerts from API
@app.post("/api/weather-alerts/update")
async def update_weather_alerts_from_api(region: Optional[str] = None):
    """
    Manually trigger update of weather alerts from Weather API.
    """
    try:
        from weather_integration import fetch_weather_alerts_from_api, update_weather_alerts_in_db
        alerts = fetch_weather_alerts_from_api(region)
        if alerts:
            update_weather_alerts_in_db(alerts)
            return {"status": "success", "message": f"Updated {len(alerts)} weather alerts", "count": len(alerts)}
        else:
            return {"status": "success", "message": "No new alerts found", "count": 0}
    except ImportError:
        return {"status": "error", "message": "weather_integration module not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Pest alerts endpoints
@app.get("/api/pest-alerts")
async def get_pest_alerts(region: Optional[str] = None, language: str = "ur", pest_name: Optional[str] = None):
    """
    Get pest alerts from database with comprehensive information.
    No API dependency - all data is stored locally.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = 'SELECT * FROM pest_alerts WHERE 1=1'
    params = []
    
    if region:
        query += ' AND region = ?'
        params.append(region)
    
    if pest_name:
        query += ' AND (pest_name_ur LIKE ? OR pest_name_en LIKE ?)'
        params.extend([f"%{pest_name}%", f"%{pest_name}%"])
    
    query += ' ORDER BY created_at DESC LIMIT 20'
    
    cursor.execute(query, params)
    alerts = cursor.fetchall()
    conn.close()
    
    result = []
    for alert in alerts:
        pest_name_key = f"pest_name_{language}" if language in ["ur", "en"] else "pest_name_ur"
        prevention_key = f"prevention_{language}" if language in ["ur", "en"] else "prevention_ur"
        symptoms_key = f"symptoms_{language}" if language in ["ur", "en"] else "symptoms_ur"
        treatment_key = f"treatment_{language}" if language in ["ur", "en"] else "treatment_ur"
        
        result.append({
            "id": alert["id"],
            "region": alert["region"],
            "pest_name": alert[pest_name_key] if pest_name_key in alert.keys() else alert["pest_name_ur"],
            "pest_name_ur": alert["pest_name_ur"] if "pest_name_ur" in alert.keys() else "",
            "pest_name_en": alert["pest_name_en"] if "pest_name_en" in alert.keys() else "",
            "crop_affected": alert["crop_affected"],
            "severity": alert["severity"],
            "prevention": alert[prevention_key] if prevention_key in alert.keys() else alert["prevention_ur"],
            "symptoms": alert[symptoms_key] if symptoms_key in alert.keys() else (alert["symptoms_ur"] if "symptoms_ur" in alert.keys() else ""),
            "treatment": alert[treatment_key] if treatment_key in alert.keys() else (alert["treatment_ur"] if "treatment_ur" in alert.keys() else ""),
            "created_at": alert["created_at"]
        })
    return result

@app.get("/api/pest-alerts/{pest_id}")
async def get_pest_detail(pest_id: int, language: str = "ur"):
    """
    Get detailed information about a specific pest
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pest_alerts WHERE id = ?', (pest_id,))
    alert = cursor.fetchone()
    conn.close()
    
    if alert:
        return {
            "id": alert["id"],
            "region": alert["region"],
            "pest_name": alert[f"pest_name_{language}"] if language in ["ur", "en"] else alert["pest_name_ur"],
            "pest_name_ur": alert.get("pest_name_ur", ""),
            "pest_name_en": alert.get("pest_name_en", ""),
            "crop_affected": alert["crop_affected"],
            "severity": alert["severity"],
            "prevention": alert[f"prevention_{language}"] if language in ["ur", "en"] else alert["prevention_ur"],
            "symptoms": alert.get(f"symptoms_{language}", alert.get("symptoms_ur", "")) if language in ["ur", "en"] else alert.get("symptoms_ur", ""),
            "treatment": alert.get(f"treatment_{language}", alert.get("treatment_ur", "")) if language in ["ur", "en"] else alert.get("treatment_ur", ""),
            "created_at": alert["created_at"]
        }
    raise HTTPException(status_code=404, detail="Pest alert not found")

# Wiki endpoints
@app.get("/api/wiki")
async def get_wiki_articles(category: Optional[str] = None, language: str = "ur"):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = 'SELECT * FROM wiki_articles WHERE 1=1'
    params = []
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    articles = cursor.fetchall()
    conn.close()
    
    # Remove duplicates by title_en to ensure unique articles
    seen_titles = set()
    result = []
    for article in articles:
        title_key = article["title_en"]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            result.append({
                "id": article["id"],
                "title": article[f"title_{language}"] if language in ["ur", "en"] else article["title_ur"],
                "content": article[f"content_{language}"] if language in ["ur", "en"] else article["content_ur"],
                "category": article["category"],
                "tags": article["tags"],
                "wiki_url": article["wiki_url"] if article["wiki_url"] else "",
                "created_at": article["created_at"]
            })
    return result

@app.get("/api/wiki/{article_id}")
async def get_wiki_article(article_id: int, language: str = "ur"):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wiki_articles WHERE id = ?', (article_id,))
    article = cursor.fetchone()
    conn.close()
    
    if article:
        return {
            "id": article["id"],
            "title": article[f"title_{language}"] if language in ["ur", "en"] else article["title_ur"],
            "content": article[f"content_{language}"] if language in ["ur", "en"] else article["content_ur"],
            "category": article["category"],
            "tags": article["tags"],
            "wiki_url": article["wiki_url"] if article["wiki_url"] else "",
            "created_at": article["created_at"]
        }
    raise HTTPException(status_code=404, detail="Article not found")

# Chat endpoint (with Gemini API integration support)
@app.post("/api/chat")
async def chat(message: ChatMessage):
    question = message.question.lower()
    
    # Try to use Gemini API if available
    try:
        from gemini_integration import get_agri_response
        response = get_agri_response(message.question, message.language)
    except ImportError:
        # Fallback to keyword-based responses
        response = "میں آپ کی مدد کرنے کے لیے یہاں ہوں۔ براہ کرم اپنا سوال مزید تفصیل سے پوچھیں۔"
        
        if message.language == "ur":
            if "price" in question or "قیمت" in question:
                response = "قیمتوں کے لیے، براہ کرم مارکیٹ انٹیلی جنس ہب چیک کریں۔"
            elif "disease" in question or "بیماری" in question or "روگ" in question:
                response = "فصلوں کی بیماریوں کے لیے، آپ کا مقامی زرعی ماہر سے مشورہ لینا بہتر ہوگا۔"
            elif "compost" in question or "کمپوسٹ" in question:
                response = "کمپوسٹ بنانے کے لیے، براہ کرم Sustainable Practices Wiki میں دیکھیں۔"
            elif "water" in question or "پانی" in question:
                response = "پانی کی بچت کے طریقوں کے لیے، ہمارے وسائل کیلکولیٹرز دیکھیں۔"
        else:
            if "price" in question:
                response = "Please check the Market Intelligence Hub for prices."
            elif "disease" in question:
                response = "For crop diseases, it's better to consult your local agricultural expert."
            elif "compost" in question:
                response = "For making compost, please check the Sustainable Practices Wiki."
            elif "water" in question:
                response = "For water conservation methods, see our resource calculators."
    
    # Save chat history
    if message.user_id:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chat_history (user_id, question, answer, language)
            VALUES (?, ?, ?, ?)
        ''', (message.user_id, message.question, response, message.language))
        conn.commit()
        conn.close()
    
    return {"answer": response, "language": message.language}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


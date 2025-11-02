"""
Example Gemini API Integration for Kisaan Academy
To use this, you'll need to:
1. Install: pip install google-generativeai
2. Get API key from: https://makersuite.google.com/app/apikey
3. Set environment variable: export GEMINI_API_KEY=your_key_here
"""

import os
import google.generativeai as genai
from typing import Optional, Tuple

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    import os
    # Load from current directory (where .env file is located)
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path, override=True)
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables

# Configure Gemini API
# Get your API key from: https://makersuite.google.com/app/apikey
# Option 1: Create backend/.env file with: GEMINI_API_KEY=your_key_here
# Option 2: Set environment variable: $env:GEMINI_API_KEY="your_key_here" (PowerShell)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Debug: Check if API key is loaded
if GEMINI_API_KEY:
    if GEMINI_API_KEY == "your_gemini_api_key_here":
        print("⚠ Warning: .env file has placeholder. Please replace 'your_gemini_api_key_here' with your actual API key!")
        GEMINI_API_KEY = None  # Treat placeholder as not set
    else:
        print(f"✓ Found API key (length: {len(GEMINI_API_KEY)})")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use the latest available model - try gemini-2.5-flash (fast and free tier friendly)
        model = None
        model_names = [
            'models/gemini-2.5-flash',  # Latest flash model
            'models/gemini-2.5-flash-lite-preview-06-17',  # Alternative
            'models/gemini-2.5-pro-preview-05-06',  # Pro version if flash fails
        ]
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✓ Gemini API configured with {model_name}")
                break
            except Exception as e:
                continue
        
        if not model:
            print("✗ Could not configure any Gemini model. Listing available models...")
            try:
                available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                print(f"Available models: {available[:3]}")
                if available:
                    model = genai.GenerativeModel(available[0])
                    print(f"✓ Using first available model: {available[0]}")
            except Exception as e:
                print(f"✗ Error configuring Gemini API: {e}")
                model = None
    except Exception as e:
        print(f"✗ Error configuring Gemini API: {e}")
        model = None
else:
    model = None
    print("⚠ Warning: GEMINI_API_KEY not set. Using fallback responses.")
    print("   Set it with: $env:GEMINI_API_KEY='your_key_here' (Windows PowerShell)")
    print("   Or: export GEMINI_API_KEY='your_key_here' (Linux/Mac)")


def detect_price_query(question: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if question is about prices/market and extract crop name if mentioned.
    
    Returns:
        (is_price_query: bool, crop_name: Optional[str])
    """
    question_lower = question.lower()
    
    # Price-related keywords
    price_keywords = [
        "price", "قیمت", "قیمتوں",
        "market", "مارکیٹ", "بازار",
        "rate", "ریٹ", "فیس",
        "cost", "لاگت",
        "expensive", "مہنگا", "cheap", "سستا",
        "wheat price", "گندم کی قیمت",
        "rice price", "چاول کی قیمت",
        "cotton price", "کپاس کی قیمت",
        "sugar price", "چینی کی قیمت",
    ]
    
    is_price = any(keyword in question_lower for keyword in price_keywords)
    
    if not is_price:
        return False, None
    
    # Try to extract crop name
    crops = {
        "wheat": ["wheat", "گندم"],
        "rice": ["rice", "چاول"],
        "cotton": ["cotton", "کپاس"],
        "sugar": ["sugar", "چینی", "sweet"],
        "corn": ["corn", "مکئی", "maize"],
    }
    
    for crop, keywords in crops.items():
        if any(keyword in question_lower for keyword in keywords):
            return True, crop
    
    return True, None  # Price query but no specific crop


def detect_pest_query(question: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if question is about pests and extract pest name if mentioned.
    
    Returns:
        (is_pest_query: bool, pest_name: Optional[str])
    """
    question_lower = question.lower()
    
    # Pest-related keywords
    pest_keywords = [
        "pest", "کیڑا", "کیڑے", "کیڑوں",
        "insect", "حشرات",
        "disease", "بیماری",
        "aphid", "اپھیڈ",
        "borer", "بورر",
        "whitefly", "سفید مکھی",
        "thrips", "تھرپس",
        "jassid", "جیڈ",
        "caterpillar", "کیٹر پلر",
        "infestation", "انفیکشن",
        "control", "کنٹرول",
        "prevention", "بچاؤ", "روک تھام",
        "treatment", "علاج",
        "symptoms", "علامات", "نشانات",
    ]
    
    is_pest = any(keyword in question_lower for keyword in pest_keywords)
    
    if not is_pest:
        return False, None
    
    # Try to extract pest name
    pests = {
        "aphid": ["aphid", "اپھیڈ"],
        "whitefly": ["whitefly", "سفید مکھی", "white fly"],
        "borer": ["borer", "بورر", "stem borer", "ڈھڈا بورر"],
        "thrips": ["thrips", "تھرپس"],
        "jassid": ["jassid", "جیڈ"],
        "armyworm": ["armyworm", "فال آرمی ورم"],
        "leafhopper": ["leafhopper", "لیف ہوپر"],
    }
    
    for pest, keywords in pests.items():
        if any(keyword in question_lower for keyword in keywords):
            return True, pest
    
    # Check for crop-specific pest queries
    crops = ["wheat", "rice", "cotton", "corn", "گندم", "چاول", "کپاس", "مکئی"]
    if any(crop in question_lower for crop in crops) and is_pest:
        return True, None
    
    return True, None  # Pest query but no specific pest name


def detect_weather_query(question: str) -> Tuple[bool, Optional[str]]:
    """
    Detect if question is about weather and extract city name if mentioned.
    
    Returns:
        (is_weather_query: bool, city_name: Optional[str])
    """
    question_lower = question.lower()
    
    # Weather-related keywords
    weather_keywords = [
        "weather", "موسم", "آب و ہوا",
        "temperature", "درجہ حرارت", "ٹمپریچر", "گرمی", "سردی",
        "rain", "بارش", "طوفان", "storm",
        "humidity", "نمی", "humidity",
        "wind", "ہوا", "wind speed",
        "forecast", "پیشن گوئی", "پیش گوئی",
        "hot", "گرم", "cold", "سرد",
        "sunny", "دھوپ", "cloudy", "ابر آلود",
    ]
    
    is_weather = any(keyword in question_lower for keyword in weather_keywords)
    
    # Extract city name
    cities = [
        "multan", "ملتان",
        "lahore", "لاہور",
        "karachi", "کراچی",
        "islamabad", "اسلام آباد",
        "peshawar", "پشاور",
        "quetta", "کوئٹہ",
        "faisalabad", "فیصل آباد",
        "rawalpindi", "راولپنڈی",
        "gujranwala", "گوجرانوالہ",
        "sialkot", "سیالکوٹ",
        "punjab", "پنجاب",
        "sindh", "سندھ",
        "kpk", "خیبر پختونخوا",
        "balochistan", "بلوچستان",
    ]
    
    city = None
    for c in cities:
        if c in question_lower:
            # Extract the word that contains the city name
            words = question_lower.split()
            for word in words:
                if c in word:
                    city = c
                    break
            if city:
                break
    
    return is_weather, city


def get_agri_response(question: str, language: str = "ur") -> str:
    """
    Get AI response from Gemini API for farming-related questions.
    Now includes weather data integration for weather queries.
    
    Args:
        question: User's question
        language: Language preference ('ur' or 'en')
    
    Returns:
        AI-generated response
    """
    if not model:
        # Fallback response if Gemini is not configured
        return get_fallback_response(question, language)
    
    try:
        # Check if this is a weather query
        is_weather, city = detect_weather_query(question)
        weather_info = ""
        
        if is_weather:
            try:
                from weather_integration import get_current_weather
                
                # If city is mentioned, get weather for that city
                # Otherwise, try to extract city from question or default to Lahore
                query_city = city if city else "Lahore"
                
                weather_data = get_current_weather(query_city)
                
                if weather_data:
                    # Format weather data for Gemini
                    if language == "ur":
                        weather_info = f"""
[موجودہ موسمی معلومات - {weather_data['city']}]
درجہ حرارت: {weather_data['temperature_c']}°C (محسوس: {weather_data['feels_like_c']}°C)
حالت: {weather_data['condition']}
نمی: {weather_data['humidity']}%
ہوا: {weather_data['wind_kph']} کلومیٹر/گھنٹہ ({weather_data['wind_dir']})
دباؤ: {weather_data['pressure_mb']} mb
بارش: {weather_data['precip_mm']} mm
"""
                        if "today" in weather_data:
                            weather_info += f"آج: {weather_data['today']['min_temp_c']}°C - {weather_data['today']['max_temp_c']}°C, {weather_data['today']['condition']}\n"
                        if "tomorrow" in weather_data:
                            weather_info += f"کل: {weather_data['tomorrow']['min_temp_c']}°C - {weather_data['tomorrow']['max_temp_c']}°C, {weather_data['tomorrow']['condition']}\n"
                    else:
                        weather_info = f"""
[Current Weather Information - {weather_data['city']}]
Temperature: {weather_data['temperature_c']}°C (Feels like: {weather_data['feels_like_c']}°C)
Condition: {weather_data['condition']}
Humidity: {weather_data['humidity']}%
Wind: {weather_data['wind_kph']} km/h ({weather_data['wind_dir']})
Pressure: {weather_data['pressure_mb']} mb
Precipitation: {weather_data['precip_mm']} mm
"""
                        if "today" in weather_data:
                            weather_info += f"Today: {weather_data['today']['min_temp_c']}°C - {weather_data['today']['max_temp_c']}°C, {weather_data['today']['condition']}\n"
                        if "tomorrow" in weather_data:
                            weather_info += f"Tomorrow: {weather_data['tomorrow']['min_temp_c']}°C - {weather_data['tomorrow']['max_temp_c']}°C, {weather_data['tomorrow']['condition']}\n"
                    
                    print(f"✓ Fetched weather data for {weather_data['city']}")
                else:
                    weather_info = "\n[Weather data not available at the moment.]\n" if language == "en" else "\n[موسمی معلومات فی الوقت دستیاب نہیں۔]\n"
            except ImportError:
                weather_info = ""
            except Exception as e:
                print(f"Error fetching weather: {e}")
                weather_info = ""
        
        # Check if this is a pest query
        question_lower = question.lower()
        is_pest, pest_name = detect_pest_query(question)
        pest_info = ""
        
        if is_pest:
            try:
                import sqlite3
                conn = sqlite3.connect("kisaan_academy.db")
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if pest_name:
                    # Search by pest name
                    cursor.execute('''
                        SELECT * FROM pest_alerts 
                        WHERE pest_name_en LIKE ? OR pest_name_ur LIKE ?
                        ORDER BY created_at DESC 
                        LIMIT 1
                    ''', (f"%{pest_name}%", f"%{pest_name}%"))
                else:
                    # Search by crop mentioned in question
                    crop_keywords = {
                        "wheat": ["wheat", "گندم"],
                        "rice": ["rice", "چاول"],
                        "cotton": ["cotton", "کپاس"],
                        "corn": ["corn", "مکئی", "maize"],
                        "vegetable": ["vegetable", "سبزی"],
                    }
                    
                    found_crop = None
                    for crop, keywords in crop_keywords.items():
                        if any(keyword in question_lower for keyword in keywords):
                            found_crop = crop
                            break
                    
                    if found_crop:
                        crop_ur = {"wheat": "گندم", "rice": "چاول", "cotton": "کپاس", "corn": "مکئی", "vegetable": "سبزی"}.get(found_crop, "")
                        cursor.execute('''
                            SELECT * FROM pest_alerts 
                            WHERE crop_affected LIKE ?
                            ORDER BY created_at DESC 
                            LIMIT 3
                        ''', (f"%{crop_ur}%",))
                    else:
                        # Get general pest information
                        cursor.execute('''
                            SELECT * FROM pest_alerts 
                            ORDER BY created_at DESC 
                            LIMIT 3
                        ''')
                
                pests = cursor.fetchall()
                conn.close()
                
                if pests:
                    if language == "ur":
                        pest_info = "\n[کیڑوں کی تفصیلات]\n\n"
                        for pest in pests:
                            pest_info += f"**{pest['pest_name_ur']}** ({pest['crop_affected']})\n"
                            pest_info += f"خطہ: {pest['region']}\n"
                            pest_info += f"شدت: {pest['severity']}\n"
                            if pest.get('symptoms_ur'):
                                pest_info += f"علامات: {pest['symptoms_ur']}\n"
                            if pest.get('prevention_ur'):
                                pest_info += f"بچاؤ: {pest['prevention_ur']}\n"
                            if pest.get('treatment_ur'):
                                pest_info += f"علاج: {pest['treatment_ur']}\n"
                            pest_info += "\n"
                    else:
                        pest_info = "\n[Pest Information]\n\n"
                        for pest in pests:
                            pest_info += f"**{pest['pest_name_en']}** ({pest['crop_affected']})\n"
                            pest_info += f"Region: {pest['region']}\n"
                            pest_info += f"Severity: {pest['severity']}\n"
                            if pest.get('symptoms_en'):
                                pest_info += f"Symptoms: {pest['symptoms_en']}\n"
                            if pest.get('prevention_en'):
                                pest_info += f"Prevention: {pest['prevention_en']}\n"
                            if pest.get('treatment_en'):
                                pest_info += f"Treatment: {pest['treatment_en']}\n"
                            pest_info += "\n"
            except Exception as e:
                print(f"Error fetching pest information: {e}")
                pest_info = ""
        
        # Check if this is a price/market query
        is_price, crop_name = detect_price_query(question)
        price_info = ""
        
        if is_price:
            try:
                from market_integration import get_current_market_price, format_price_for_chat
                
                if crop_name:
                    price_data = get_current_market_price(crop_name)
                    if price_data:
                        price_info = format_price_for_chat(price_data, language)
                    else:
                        # Try to get from database as fallback
                        try:
                            import sqlite3
                            conn = sqlite3.connect("kisaan_academy.db")
                            conn.row_factory = sqlite3.Row
                            cursor = conn.cursor()
                            
                            crop_name_ur = {"wheat": "گندم", "rice": "چاول", "cotton": "کپاس", "sugar": "چینی"}.get(crop_name, crop_name)
                            cursor.execute('''
                                SELECT crop_name, price_per_kg, region, recorded_at 
                                FROM market_prices 
                                WHERE crop_name LIKE ? 
                                ORDER BY recorded_at DESC 
                                LIMIT 1
                            ''', (f"%{crop_name_ur}%",))
                            
                            row = cursor.fetchone()
                            conn.close()
                            
                            if row:
                                price_value = f"{row['price_per_kg']:.2f}"
                                if language == "ur":
                                    price_info = f"{row['crop_name']} کی موجودہ قیمت: {price_value} روپے فی کلوگرام (PKR/kg) - {row['region']}"
                                else:
                                    price_info = f"Current price of {row['crop_name']}: {price_value} PKR per kg - {row['region']}"
                        except Exception as db_error:
                            print(f"Error fetching from database: {db_error}")
                            price_info = ""
                else:
                    # General price query - get latest prices from database
                    try:
                        import sqlite3
                        conn = sqlite3.connect("kisaan_academy.db")
                        conn.row_factory = sqlite3.Row
                        cursor = conn.cursor()
                        
                        cursor.execute('''
                            SELECT crop_name, price_per_kg, region, recorded_at 
                            FROM market_prices 
                            ORDER BY recorded_at DESC 
                            LIMIT 5
                        ''')
                        
                        rows = cursor.fetchall()
                        conn.close()
                        
                        if rows:
                            if language == "ur":
                                price_info = "\n[موجودہ مارکیٹ قیمتیں - PKR/kg]\n"
                                for row in rows:
                                    price_value = f"{row['price_per_kg']:.2f}"
                                    price_info += f"{row['crop_name']}: {price_value} روپے/کلوگرام ({row['region']})\n"
                            else:
                                price_info = "\n[Current Market Prices - PKR/kg]\n"
                                for row in rows:
                                    price_value = f"{row['price_per_kg']:.2f}"
                                    price_info += f"{row['crop_name']}: {price_value} PKR/kg ({row['region']})\n"
                    except Exception as db_error:
                        print(f"Error fetching prices from database: {db_error}")
                        price_info = ""
                        
            except ImportError:
                price_info = ""
            except Exception as e:
                print(f"Error fetching market price: {e}")
                price_info = ""
        
        # Create a context-aware prompt
        context = f"""You are an agricultural assistant (Agri-Bot) for Pakistani farmers. 
Answer questions about farming, crops, prices, weather, pests, and agricultural practices.
Language preference: {'Urdu' if language == 'ur' else 'English'}
Keep responses concise, practical, and helpful. Always respond in the requested language.

{weather_info if weather_info else ''}
{price_info if price_info else ''}
{pest_info if pest_info else ''}

Question: {question}
Answer:"""
        
        response = model.generate_content(context)
        
        # Handle different response formats
        if hasattr(response, 'text'):
            result = response.text.strip()
        elif hasattr(response, 'candidates') and len(response.candidates) > 0:
            if hasattr(response.candidates[0], 'content'):
                result = response.candidates[0].content.parts[0].text.strip()
            else:
                result = str(response.candidates[0]).strip()
        else:
            result = str(response).strip()
        
        # Log successful API call (only first 50 chars to avoid spam)
        if result and len(result) > 0:
            print(f"✓ Gemini API response: {result[:50]}...")
            return result
        else:
            raise Exception("Empty response from Gemini API")
    except Exception as e:
        print(f"✗ Error calling Gemini API: {e}")
        print(f"   Question was: {question[:50]}...")
        return get_fallback_response(question, language)


def get_fallback_response(question: str, language: str) -> str:
    """
    Fallback keyword-based responses when Gemini API is not available.
    """
    question_lower = question.lower()
    
    # Check for pest query and try to get pest information
    is_pest, pest_name = detect_pest_query(question)
    if is_pest:
        try:
            import sqlite3
            conn = sqlite3.connect("kisaan_academy.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if pest_name:
                cursor.execute('''
                    SELECT * FROM pest_alerts 
                    WHERE pest_name_en LIKE ? OR pest_name_ur LIKE ?
                    ORDER BY created_at DESC LIMIT 1
                ''', (f"%{pest_name}%", f"%{pest_name}%"))
            else:
                # Search by crop
                crop_keywords = {
                    "wheat": "گندم",
                    "rice": "چاول",
                    "cotton": "کپاس",
                    "corn": "مکئی",
                }
                
                found_crop = None
                for crop, crop_ur in crop_keywords.items():
                    if crop in question_lower or crop_ur in question_lower:
                        found_crop = crop_ur
                        break
                
                if found_crop:
                    cursor.execute('''
                        SELECT * FROM pest_alerts 
                        WHERE crop_affected LIKE ?
                        ORDER BY created_at DESC LIMIT 1
                    ''', (f"%{found_crop}%",))
                else:
                    cursor.execute('SELECT * FROM pest_alerts ORDER BY created_at DESC LIMIT 1')
            
            pest = cursor.fetchone()
            conn.close()
            
            if pest:
                if language == "ur":
                    result = f"**{pest['pest_name_ur']}**\n"
                    result += f"فصل: {pest['crop_affected']}\n"
                    result += f"خطہ: {pest['region']}\n"
                    result += f"شدت: {pest['severity']}\n\n"
                    if pest.get('symptoms_ur'):
                        result += f"**علامات:**\n{pest['symptoms_ur']}\n\n"
                    if pest.get('prevention_ur'):
                        result += f"**بچاؤ کے طریقے:**\n{pest['prevention_ur']}\n\n"
                    if pest.get('treatment_ur'):
                        result += f"**علاج:**\n{pest['treatment_ur']}"
                    return result
                else:
                    result = f"**{pest['pest_name_en']}**\n"
                    result += f"Crop: {pest['crop_affected']}\n"
                    result += f"Region: {pest['region']}\n"
                    result += f"Severity: {pest['severity']}\n\n"
                    if pest.get('symptoms_en'):
                        result += f"**Symptoms:**\n{pest['symptoms_en']}\n\n"
                    if pest.get('prevention_en'):
                        result += f"**Prevention:**\n{pest['prevention_en']}\n\n"
                    if pest.get('treatment_en'):
                        result += f"**Treatment:**\n{pest['treatment_en']}"
                    return result
        except Exception as e:
            print(f"Error fetching pest data in fallback: {e}")
    
    # Check for price query and try to get real market data
    is_price, crop_name = detect_price_query(question)
    if is_price:
        try:
            from market_integration import get_current_market_price, format_price_for_chat
            if crop_name:
                price_data = get_current_market_price(crop_name)
                if price_data:
                    return format_price_for_chat(price_data, language)
        except:
            pass
        
        # Try database fallback
        try:
            import sqlite3
            conn = sqlite3.connect("kisaan_academy.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if crop_name:
                crop_name_ur = {"wheat": "گندم", "rice": "چاول", "cotton": "کپاس", "sugar": "چینی"}.get(crop_name, crop_name)
                cursor.execute('''
                    SELECT crop_name, price_per_kg, region FROM market_prices 
                    WHERE crop_name LIKE ? ORDER BY recorded_at DESC LIMIT 1
                ''', (f"%{crop_name_ur}%",))
                row = cursor.fetchone()
                
                if row:
                    price_value = f"{row['price_per_kg']:.2f}"
                    if language == "ur":
                        return f"{row['crop_name']} کی موجودہ قیمت: {price_value} روپے فی کلوگرام (PKR/kg) - {row['region']}"
                    else:
                        return f"Current price of {row['crop_name']}: {price_value} PKR per kg - {row['region']}"
            else:
                cursor.execute('SELECT crop_name, price_per_kg, region FROM market_prices ORDER BY recorded_at DESC LIMIT 3')
                rows = cursor.fetchall()
                
                if rows:
                    if language == "ur":
                        result = "موجودہ مارکیٹ قیمتیں (PKR/kg):\n"
                        for row in rows:
                            price_value = f"{row['price_per_kg']:.2f}"
                            result += f"{row['crop_name']}: {price_value} روپے/کلوگرام ({row['region']})\n"
                        return result
                    else:
                        result = "Current market prices (PKR/kg):\n"
                        for row in rows:
                            price_value = f"{row['price_per_kg']:.2f}"
                            result += f"{row['crop_name']}: {price_value} PKR/kg ({row['region']})\n"
                        return result
            conn.close()
        except Exception as e:
            print(f"Database error in fallback: {e}")
    
    # Check for weather query and try to get real weather data
    is_weather, city = detect_weather_query(question)
    if is_weather:
        try:
            from weather_integration import get_current_weather
            query_city = city if city else "Lahore"
            weather_data = get_current_weather(query_city)
            
            if weather_data:
                if language == "ur":
                    return f"{weather_data['city']} میں فی الوقت موسم:\nدرجہ حرارت: {weather_data['temperature_c']}°C (محسوس: {weather_data['feels_like_c']}°C)\nحالت: {weather_data['condition']}\nنمی: {weather_data['humidity']}%\nہوا: {weather_data['wind_kph']} کلومیٹر/گھنٹہ"
                else:
                    return f"Current weather in {weather_data['city']}:\nTemperature: {weather_data['temperature_c']}°C (Feels like: {weather_data['feels_like_c']}°C)\nCondition: {weather_data['condition']}\nHumidity: {weather_data['humidity']}%\nWind: {weather_data['wind_kph']} km/h"
        except:
            pass  # Fall through to keyword responses
    
    responses_ur = {
        "price": "قیمتوں کے لیے، براہ کرم مارکیٹ انٹیلی جنس ہب چیک کریں۔",
        "قیمت": "قیمتوں کے لیے، براہ کرم مارکیٹ انٹیلی جنس ہب چیک کریں۔",
        "disease": "فصلوں کی بیماریوں کے لیے، آپ کا مقامی زرعی ماہر سے مشورہ لینا بہتر ہوگا۔",
        "بیماری": "فصلوں کی بیماریوں کے لیے، آپ کا مقامی زرعی ماہر سے مشورہ لینا بہتر ہوگا۔",
        "compost": "کمپوسٹ بنانے کے لیے، براہ کرم Sustainable Practices Wiki میں دیکھیں۔",
        "کمپوسٹ": "کمپوسٹ بنانے کے لیے، براہ کرم Sustainable Practices Wiki میں دیکھیں۔",
        "water": "پانی کی بچت کے طریقوں کے لیے، ہمارے وسائل کیلکولیٹرز دیکھیں۔",
        "پانی": "پانی کی بچت کے طریقوں کے لیے، ہمارے وسائل کیلکولیٹرز دیکھیں۔",
    }
    
    responses_en = {
        "price": "Please check the Market Intelligence Hub for prices.",
        "disease": "For crop diseases, it's better to consult your local agricultural expert.",
        "compost": "For making compost, please check the Sustainable Practices Wiki.",
        "water": "For water conservation methods, see our resource calculators.",
    }
    
    responses = responses_ur if language == "ur" else responses_en
    
    for keyword, response in responses.items():
        if keyword in question_lower:
            return response
    
    default_ur = "میں آپ کی مدد کرنے کے لیے یہاں ہوں۔ براہ کرم اپنا سوال مزید تفصیل سے پوچھیں۔"
    default_en = "I'm here to help you. Please ask your question in more detail."
    
    return default_ur if language == "ur" else default_en


# Example usage
if __name__ == "__main__":
    # Test the integration
    test_questions = [
        "گندم کی قیمت کیا ہے؟",
        "میرے کپاس کے پتے پر دھبے ہیں، کیا کروں؟",
        "How to make compost?",
    ]
    
    for question in test_questions:
        lang = "ur" if any(ord(c) > 127 for c in question) else "en"
        answer = get_agri_response(question, lang)
        print(f"Q: {question}")
        print(f"A: {answer}\n")


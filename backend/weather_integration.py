"""
Weather API Integration for Live Weather Data
Using WeatherAPI.com
"""

import os
import requests
from typing import List, Optional, Dict
from datetime import datetime, timedelta

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Weather API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "99dd9e0dbf9344bebb2223518252110")
WEATHER_API_BASE = "http://api.weatherapi.com/v1"

def get_current_weather(city: str) -> Optional[Dict]:
    """
    Get current weather data for a specific city.
    
    Args:
        city: City name (e.g., "Multan", "Lahore", "Karachi")
        
    Returns:
        Dictionary with weather data or None if error
    """
    if not WEATHER_API_KEY:
        return None
    
    # Map city names (support Urdu names and common variations)
    city_mapping = {
        "multan": "Multan",
        "ملتان": "Multan",
        "lahore": "Lahore",
        "لاہور": "Lahore",
        "karachi": "Karachi",
        "کراچی": "Karachi",
        "islamabad": "Islamabad",
        "اسلام آباد": "Islamabad",
        "peshawar": "Peshawar",
        "پشاور": "Peshawar",
        "quetta": "Quetta",
        "کوئٹہ": "Quetta",
        "faisalabad": "Faisalabad",
        "فیصل آباد": "Faisalabad",
        "rawalpindi": "Rawalpindi",
        "راولپنڈی": "Rawalpindi",
        "gujranwala": "Gujranwala",
        "گوجرانوالہ": "Gujranwala",
        "sialkot": "Sialkot",
        "سیالکوٹ": "Sialkot",
    }
    
    # Normalize city name
    city_lower = city.lower().strip()
    mapped_city = city_mapping.get(city_lower, city.title())
    
    try:
        url = f"{WEATHER_API_BASE}/current.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": mapped_city,
            "aqi": "yes"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        location = data.get("location", {})
        current = data.get("current", {})
        condition = current.get("condition", {})
        
        weather_data = {
            "city": location.get("name", mapped_city),
            "region": location.get("region", ""),
            "country": location.get("country", ""),
            "temperature_c": current.get("temp_c", 0),
            "temperature_f": current.get("temp_f", 0),
            "feels_like_c": current.get("feelslike_c", 0),
            "feels_like_f": current.get("feelslike_f", 0),
            "condition": condition.get("text", ""),
            "humidity": current.get("humidity", 0),
            "wind_kph": current.get("wind_kph", 0),
            "wind_mph": current.get("wind_mph", 0),
            "wind_dir": current.get("wind_dir", ""),
            "pressure_mb": current.get("pressure_mb", 0),
            "precip_mm": current.get("precip_mm", 0),
            "uv_index": current.get("uv", 0),
            "visibility_km": current.get("vis_km", 0),
            "last_updated": current.get("last_updated", ""),
        }
        
        # Add air quality if available
        if "air_quality" in current:
            aq = current["air_quality"]
            weather_data["air_quality"] = {
                "us_epa_index": aq.get("us-epa-index", 0),
                "pm2_5": aq.get("pm2_5", 0),
                "pm10": aq.get("pm10", 0),
            }
        
        # Get forecast for today and tomorrow
        try:
            forecast_url = f"{WEATHER_API_BASE}/forecast.json"
            forecast_params = {
                "key": WEATHER_API_KEY,
                "q": mapped_city,
                "days": 2,
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            forecast = forecast_data.get("forecast", {}).get("forecastday", [])
            if forecast and len(forecast) > 0:
                today = forecast[0].get("day", {})
                weather_data["today"] = {
                    "max_temp_c": today.get("maxtemp_c", 0),
                    "min_temp_c": today.get("mintemp_c", 0),
                    "max_temp_f": today.get("maxtemp_f", 0),
                    "min_temp_f": today.get("mintemp_f", 0),
                    "condition": today.get("condition", {}).get("text", ""),
                    "maxwind_kph": today.get("maxwind_kph", 0),
                    "totalprecip_mm": today.get("totalprecip_mm", 0),
                }
            
            if forecast and len(forecast) > 1:
                tomorrow = forecast[1].get("day", {})
                weather_data["tomorrow"] = {
                    "max_temp_c": tomorrow.get("maxtemp_c", 0),
                    "min_temp_c": tomorrow.get("mintemp_c", 0),
                    "max_temp_f": tomorrow.get("maxtemp_f", 0),
                    "min_temp_f": tomorrow.get("mintemp_f", 0),
                    "condition": tomorrow.get("condition", {}).get("text", ""),
                    "maxwind_kph": tomorrow.get("maxwind_kph", 0),
                    "totalprecip_mm": tomorrow.get("totalprecip_mm", 0),
                }
        except:
            pass  # Forecast not critical
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for {city}: {e}")
        return None
    except Exception as e:
        print(f"Error processing weather data for {city}: {e}")
        return None

def fetch_weather_alerts_from_api(region: Optional[str] = None) -> List[Dict]:
    """
    Fetch weather alerts from WeatherAPI.com.
    
    Args:
        region: City/region name (e.g., "Lahore", "Karachi", "Islamabad")
        
    Returns:
        List of weather alert dictionaries
    """
    if not WEATHER_API_KEY:
        print("⚠ Warning: WEATHER_API_KEY not set. Cannot fetch weather data.")
        return []
    
    alerts = []
    
    # Map regions to city names for WeatherAPI
    region_to_city = {
        "Punjab": "Lahore",
        "Sindh": "Karachi",
        "KPK": "Peshawar",
        "Balochistan": "Quetta",
        "Lahore": "Lahore",
        "Karachi": "Karachi",
        "Islamabad": "Islamabad",
        "Peshawar": "Peshawar",
        "Quetta": "Quetta",
        "Multan": "Multan",
        "Faisalabad": "Faisalabad",
    }
    
    # Default cities if no region specified
    cities_to_check = []
    if region:
        city = region_to_city.get(region, region)
        cities_to_check = [city]
    else:
        # Check major Pakistani cities
        cities_to_check = ["Lahore", "Karachi", "Islamabad", "Peshawar", "Multan", "Faisalabad"]
    
    for city in cities_to_check:
        try:
            # Get current weather
            url = f"{WEATHER_API_BASE}/current.json"
            params = {
                "key": WEATHER_API_KEY,
                "q": city,
                "aqi": "yes"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            location = data.get("location", {})
            
            temp_c = current.get("temp_c", 0)
            condition = current.get("condition", {}).get("text", "").lower()
            wind_kph = current.get("wind_kph", 0)
            humidity = current.get("humidity", 0)
            aqi = current.get("air_quality", {}).get("us-epa-index", 0) if "air_quality" in current else 0
            
            # Check for extreme conditions and create alerts
            if temp_c > 40:
                alerts.append({
                    'region': region or city,
                    'alert_type': 'heatwave',
                    'severity': 'high',
                    'message_en': f'Extreme heat warning in {city}: Temperature is {temp_c}°C. Take precautions for crops.',
                    'message_ur': f'{city} میں شدید گرمی کی وارننگ: درجہ حرارت {temp_c}°C ہے۔ فصلوں کے لیے احتیاطی تدابیر اختیار کریں۔',
                    'valid_until': (datetime.now() + timedelta(days=1)).isoformat()
                })
            elif temp_c < 5:
                alerts.append({
                    'region': region or city,
                    'alert_type': 'cold_wave',
                    'severity': 'high',
                    'message_en': f'Cold wave warning in {city}: Temperature is {temp_c}°C. Protect sensitive crops.',
                    'message_ur': f'{city} میں سردی کی لہر کی وارننگ: درجہ حرارت {temp_c}°C ہے۔ حساس فصلوں کی حفاظت کریں۔',
                    'valid_until': (datetime.now() + timedelta(days=1)).isoformat()
                })
            
            if 'rain' in condition or 'storm' in condition or 'thunder' in condition:
                alerts.append({
                    'region': region or city,
                    'alert_type': 'heavy_rain',
                    'severity': 'medium',
                    'message_en': f'Rain/Storm alert in {city}: {condition.title()} conditions expected.',
                    'message_ur': f'{city} میں بارش/طوفان کی الرٹ: {condition.title()} حالات متوقع ہیں۔',
                    'valid_until': (datetime.now() + timedelta(days=1)).isoformat()
                })
            
            if wind_kph > 30:
                alerts.append({
                    'region': region or city,
                    'alert_type': 'strong_wind',
                    'severity': 'medium',
                    'message_en': f'Strong wind warning in {city}: Wind speed is {wind_kph} km/h.',
                    'message_ur': f'{city} میں تیز ہوا کی وارننگ: ہوا کی رفتار {wind_kph} کلومیٹر/گھنٹہ ہے۔',
                    'valid_until': (datetime.now() + timedelta(days=1)).isoformat()
                })
            
            if humidity > 80:
                alerts.append({
                    'region': region or city,
                    'alert_type': 'high_humidity',
                    'severity': 'medium',
                    'message_en': f'High humidity in {city}: {humidity}%. May increase disease risk in crops.',
                    'message_ur': f'{city} میں زیادہ نمی: {humidity}%۔ فصلوں میں بیماری کا خطرہ بڑھ سکتا ہے۔',
                    'valid_until': (datetime.now() + timedelta(days=1)).isoformat()
                })
            
            if aqi >= 4:  # Unhealthy air quality
                alerts.append({
                    'region': region or city,
                    'alert_type': 'air_quality',
                    'severity': 'medium',
                    'message_en': f'Poor air quality in {city}. May affect crop health.',
                    'message_ur': f'{city} میں ہوا کی ناقص معیار۔ فصلوں کی صحت متاثر ہو سکتی ہے۔',
                    'valid_until': (datetime.now() + timedelta(days=1)).isoformat()
                })
            
            # Get forecast for tomorrow
            try:
                forecast_url = f"{WEATHER_API_BASE}/forecast.json"
                forecast_params = {
                    "key": WEATHER_API_KEY,
                    "q": city,
                    "days": 3,
                    "alerts": "yes"
                }
                
                forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()
                
                # Check for alerts from API
                if "alerts" in forecast_data and "alert" in forecast_data["alerts"]:
                    for alert in forecast_data["alerts"]["alert"]:
                        alerts.append({
                            'region': region or city,
                            'alert_type': alert.get("event", "weather_alert"),
                            'severity': 'high' if alert.get("severity") == "Extreme" else 'medium',
                            'message_en': alert.get("headline", alert.get("desc", "Weather alert")),
                            'message_ur': alert.get("desc", "موسم کی الرٹ"),
                            'valid_until': alert.get("expires", (datetime.now() + timedelta(days=1)).isoformat())
                        })
                
                # Check forecast for extreme conditions
                forecast = forecast_data.get("forecast", {}).get("forecastday", [])
                if forecast:
                    tomorrow = forecast[0].get("day", {})
                    max_temp = tomorrow.get("maxtemp_c", 0)
                    min_temp = tomorrow.get("mintemp_c", 0)
                    maxwind = tomorrow.get("maxwind_kph", 0)
                    
                    if max_temp > 42:
                        alerts.append({
                            'region': region or city,
                            'alert_type': 'heatwave',
                            'severity': 'high',
                            'message_en': f'Tomorrow: Extreme heat expected in {city} ({max_temp}°C).',
                            'message_ur': f'کل: {city} میں شدید گرمی متوقع ({max_temp}°C)۔',
                            'valid_until': (datetime.now() + timedelta(days=2)).isoformat()
                        })
                    
                    if maxwind > 40:
                        alerts.append({
                            'region': region or city,
                            'alert_type': 'strong_wind',
                            'severity': 'medium',
                            'message_en': f'Tomorrow: Strong winds expected in {city} ({maxwind} km/h).',
                            'message_ur': f'کل: {city} میں تیز ہواؤں کی توقع ({maxwind} کلومیٹر/گھنٹہ)۔',
                            'valid_until': (datetime.now() + timedelta(days=2)).isoformat()
                        })
                        
            except Exception as e:
                print(f"Error fetching forecast for {city}: {e}")
                # Continue without forecast
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city}: {e}")
            continue
        except Exception as e:
            print(f"Error processing weather data for {city}: {e}")
            continue
    
    return alerts


def update_weather_alerts_in_db(alerts: List[Dict]):
    """
    Update weather alerts in database.
    
    Args:
        alerts: List of weather alert dictionaries
    """
    if not alerts:
        return
    
    import sqlite3
    
    DATABASE = "kisaan_academy.db"
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    for alert in alerts:
        # Check if similar alert already exists (avoid duplicates)
        cursor.execute('''
            SELECT id FROM weather_alerts 
            WHERE region = ? AND alert_type = ? AND created_at > datetime('now', '-1 hour')
            ORDER BY created_at DESC LIMIT 1
        ''', (
            alert.get('region'),
            alert.get('alert_type')
        ))
        
        existing = cursor.fetchone()
        
        if not existing:
            # Insert new alert
            cursor.execute('''
                INSERT INTO weather_alerts 
                (region, alert_type, severity, message_ur, message_en, valid_until, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.get('region'),
                alert.get('alert_type'),
                alert.get('severity', 'medium'),
                alert.get('message_ur', ''),
                alert.get('message_en', ''),
                alert.get('valid_until'),
                datetime.now().isoformat()
            ))
    
    conn.commit()
    conn.close()
    print(f"✓ Updated {len(alerts)} weather alerts in database")


# Test function
if __name__ == "__main__":
    print("Testing Weather API Integration...")
    print("\n1. Fetching weather alerts:")
    alerts = fetch_weather_alerts_from_api()
    print(f"   Found {len(alerts)} alerts")
    
    if alerts:
        print("\n2. Sample alerts:")
        for alert in alerts[:3]:
            print(f"   - {alert.get('region')}: {alert.get('message_en', '')[:60]}...")
        
        print("\n3. Updating database...")
        update_weather_alerts_in_db(alerts)
        print("   ✓ Done!")


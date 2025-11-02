"""
Market/Commodity Prices API Integration
Using RapidAPI Commodity Prices API
"""

import os
import http.client
import json
from typing import List, Optional, Dict
from datetime import datetime

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# RapidAPI Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "906eb927b3mshb92dc7f1f8ff7e9p1ec2c3jsn9ba32e99f5f1")
RAPIDAPI_HOST = "commodity-prices2.p.rapidapi.com"

def fetch_commodity_price(commodity_name: str) -> Optional[Dict]:
    """
    Fetch price for a specific commodity from RapidAPI
    
    Args:
        commodity_name: Name of commodity (e.g., "wheat", "rice", "cotton", "sugar")
        
    Returns:
        Dictionary with commodity price data or None if error
    """
    if not RAPIDAPI_KEY:
        return None
    
    try:
        conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }
        
        # Replace {name} with actual commodity name
        endpoint = f"/api/Commodity/{commodity_name}"
        conn.request("GET", endpoint, headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            result = json.loads(data.decode("utf-8"))
            return result
        else:
            print(f"API Error: {res.status} - {data.decode('utf-8')}")
            return None
            
    except Exception as e:
        print(f"Error fetching commodity price for {commodity_name}: {e}")
        return None

def fetch_all_commodities() -> List[Dict]:
    """
    Fetch prices for common agricultural commodities
    
    Returns:
        List of commodity price dictionaries
    """
    commodities = []
    
    # Common agricultural commodities in Pakistan
    commodity_names = [
        "wheat", "rice", "cotton", "sugar", "corn", "soybeans",
        "palm-oil", "sunflower-oil", "rapeseed-oil"
    ]
    
    for name in commodity_names:
        price_data = fetch_commodity_price(name)
        if price_data:
            commodities.append(price_data)
    
    return commodities

def get_current_market_price(crop_name: str) -> Optional[Dict]:
    """
    Get current market price for a crop (maps Urdu/English names to API commodity names)
    
    Args:
        crop_name: Crop name in Urdu or English
        
    Returns:
        Price data dictionary or None
    """
    # Map crop names to API commodity names
    crop_mapping = {
        # Urdu names
        "گندم": "wheat",
        "چاول": "rice",
        "کپاس": "cotton",
        "چینی": "sugar",
        "مکئی": "corn",
        
        # English names
        "wheat": "wheat",
        "rice": "rice",
        "cotton": "cotton",
        "sugar": "sugar",
        "corn": "corn",
        "maize": "corn",
        
        # Additional mappings
        "soybeans": "soybeans",
        "palm oil": "palm-oil",
        "sunflower oil": "sunflower-oil",
    }
    
    # Normalize input
    crop_lower = crop_name.lower().strip()
    
    # Check direct mapping
    api_name = crop_mapping.get(crop_name) or crop_mapping.get(crop_lower)
    
    if not api_name:
        # Try fuzzy matching
        for key, value in crop_mapping.items():
            if crop_lower in key.lower() or key.lower() in crop_lower:
                api_name = value
                break
    
    if api_name:
        return fetch_commodity_price(api_name)
    
    return None

def format_price_for_chat(price_data: Dict, language: str = "en") -> str:
    """
    Format price data into a readable string for chatbot in PKR
    
    Args:
        price_data: Commodity price dictionary from API or database
        language: Language preference ("ur" or "en")
        
    Returns:
        Formatted price string in PKR
    """
    if not price_data:
        return "Price information not available." if language == "en" else "قیمت کی معلومات دستیاب نہیں ہے۔"
    
    try:
        # Extract relevant fields (adjust based on actual API response structure)
        name = price_data.get("name", price_data.get("crop_name", "Commodity"))
        price = price_data.get("price", price_data.get("current_price", price_data.get("price_per_kg", "N/A")))
        unit = price_data.get("unit", "")
        change = price_data.get("change", price_data.get("price_change", None))
        
        # Format price to 2 decimal places if it's a number
        if isinstance(price, (int, float)):
            price_str = f"{price:.2f}"
        else:
            price_str = str(price)
        
        if language == "ur":
            response = f"{name} کی موجودہ قیمت: {price_str} روپے فی کلوگرام (PKR/kg)"
            if change:
                change_type = "اضافہ" if change > 0 else "کمی" if change < 0 else "بدلاو نہیں"
                response += f"\n{change_type}: {abs(change)} روپے"
            return response
        else:
            response = f"Current price of {name}: {price_str} PKR per kg"
            if change:
                change_type = "increased" if change > 0 else "decreased" if change < 0 else "no change"
                response += f"\n{change_type}: {abs(change)} PKR"
            return response
            
    except Exception as e:
        print(f"Error formatting price: {e}")
        return "Price information not available." if language == "en" else "قیمت کی معلومات دستیاب نہیں ہے۔"

def update_market_prices_in_db(commodities: List[Dict], region: str = "Pakistan"):
    """
    Update market prices in SQLite database
    
    Args:
        commodities: List of commodity price dictionaries from API
        region: Region name (default: Pakistan)
    """
    import sqlite3
    
    try:
        conn = sqlite3.connect("kisaan_academy.db")
        cursor = conn.cursor()
        
        for commodity in commodities:
            try:
                # Extract data from API response (adjust fields based on actual API structure)
                name = commodity.get("name", "")
                price = commodity.get("price", commodity.get("current_price", 0))
                
                # Map commodity names to Urdu crop names for display
                crop_name_mapping = {
                    "wheat": "گندم",
                    "rice": "چاول",
                    "cotton": "کپاس",
                    "sugar": "چینی",
                    "corn": "مکئی",
                }
                
                crop_name = crop_name_mapping.get(name.lower(), name)
                
                # Only insert if price is valid and not duplicate
                if price and isinstance(price, (int, float)) and price > 0:
                    # Check for duplicate entry (same crop, region within last 24 hours)
                    cursor.execute('''
                        SELECT id FROM market_prices 
                        WHERE crop_name = ? AND region = ? 
                        AND recorded_at > datetime('now', '-1 day')
                        LIMIT 1
                    ''', (crop_name, region))
                    
                    if not cursor.fetchone():
                        cursor.execute('''
                            INSERT INTO market_prices (crop_name, region, price_per_kg, mandi_name, recorded_at)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (crop_name, region, float(price), "RapidAPI", datetime.now()))
                    
            except Exception as e:
                print(f"Error inserting commodity {commodity.get('name', 'unknown')}: {e}")
                continue
        
        conn.commit()
        conn.close()
        print(f"✓ Updated {len(commodities)} market prices in database")
        
    except Exception as e:
        print(f"Error updating market prices in database: {e}")

def fetch_market_prices_from_api() -> List[Dict]:
    """
    Fetch latest market prices from RapidAPI for common commodities
    
    Returns:
        List of commodity price dictionaries
    """
    commodities = fetch_all_commodities()
    if commodities:
        update_market_prices_in_db(commodities)
    return commodities


# 🚨 IMPORTANT: Add Your Gemini API Key

## Current Status
The `.env` file exists but **still has the placeholder**. You need to add your **actual API key**.

## Quick Steps:

### 1. Open the file:
**Location:** `D:\Kisaan Academy\backend\.env`

You can:
- Double-click the file in Windows Explorer
- Or open in Notepad/VS Code

### 2. Current content (WRONG):
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Replace with your REAL key (CORRECT):
```
GEMINI_API_KEY=AIzaSyDH2oWkMZs3PkO2bpwMYZus3bYPtG9KqRQ
```
*(Replace the entire key after `=` with your actual key from Google)*

### 4. Get Your API Key:
1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"**
4. **Copy the key** (it starts with `AIza...`)

### 5. Save the file

### 6. Restart backend:
```powershell
python main.py
```

### 7. Check console - should see:
```
✓ Found API key (length: 39)
✓ Gemini API configured with gemini-1.5-flash
```

## ⚠️ Common Mistakes:

❌ **Wrong:**
- `GEMINI_API_KEY = your_key` (spaces around =)
- `GEMINI_API_KEY="your_key"` (quotes not needed)
- `GEMINI_API_KEY=your_gemini_api_key_here` (placeholder)

✅ **Correct:**
- `GEMINI_API_KEY=AIzaSy...your_actual_key`

## Test It:
After adding your key and restarting, ask the chatbot: **"What is rice price?"**
- ✅ **Should work:** AI-generated response about rice prices
- ❌ **Still broken:** "Please ask your question in more detail"

---
**The chatbot won't work until you replace the placeholder with your real API key!**


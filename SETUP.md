# Quick Setup Guide

## Backend Setup (FastAPI)

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Verify it's running:**
   - Open browser: `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`

## Frontend Setup (React)

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open in browser:**
   - Automatically opens at `http://localhost:3000`

## Database

The SQLite database (`kisaan_academy.db`) will be automatically created in the `backend` folder when you first run the backend server. Sample data is included.

## Troubleshooting

### Backend Issues

- **Port 8000 already in use:** Change the port in `main.py` or kill the process using port 8000
- **Missing dependencies:** Run `pip install -r requirements.txt` again
- **Database errors:** Delete `kisaan_academy.db` and restart the server to recreate it

### Frontend Issues

- **Port 3000 already in use:** React will prompt you to use another port
- **Module not found:** Run `npm install` again
- **API connection errors:** Make sure the backend is running on port 8000

## Development Tips

1. **Backend API Testing:**
   - Use the Swagger UI at `http://localhost:8000/docs`
   - Or test endpoints using curl or Postman

2. **Frontend Hot Reload:**
   - React development server supports hot reload
   - Changes will reflect automatically

3. **Database Management:**
   - Use SQLite browser tools or command line
   - Database file: `backend/kisaan_academy.db`

4. **Adding New Content:**
   - Courses: Insert into `courses` table
   - Wiki Articles: Insert into `wiki_articles` table
   - Market Prices: Insert into `market_prices` table (or set up web scraping)

## Production Deployment

### Backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend:
```bash
npm run build
```
Then serve the `build` folder with a web server (nginx, Apache, etc.)

## Environment Variables (Optional)

Create `.env` file in frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
```

For production, update this to your backend URL.


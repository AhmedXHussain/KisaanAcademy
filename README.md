# Kisaan Academy - کسان اکیڈمی

A comprehensive digital platform empowering farmers in Pakistan with knowledge, market intelligence, AI-powered support, and sustainable farming practices.

## 🎯 Project Overview

Kisaan Academy addresses critical challenges in Pakistan's agricultural sector:
- **Inefficient Resource Management**: Tools for water, energy, and fertilizer optimization
- **Market Volatility**: Live price tracking and demand forecasting
- **Technology Gap**: Access to modern farming techniques and AI-powered support

## ✨ Features

### 1. Learning Hub
- Interactive learning modules with videos and guides
- Courses on modern farming techniques, sustainable practices, and financial literacy
- Available in Urdu and English

### 2. Market Intelligence Hub
- Live price tracker for wholesale market (mandi) prices
- AI-driven demand forecasting
- Regional price comparisons

### 3. AI-Powered Support (Agri-Bot)
- LLM-powered chatbot (Gemini API integration ready)
- 24/7 support in local languages
- Weather and pest alerts

### 4. Sustainable Practices Wiki
- Waste management guides
- Resource calculators (water, fertilizer)
- Step-by-step sustainable farming practices

## 🛠️ Technology Stack

- **Frontend**: React with modern UI components
- **Backend**: Python FastAPI
- **Database**: SQLite
- **AI/LLM**: Gemini API (integration ready)
- **Data Analytics**: Time-series forecasting models

## 📦 Installation

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## 📁 Project Structure

```
Kisaan Academy/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── kisaan_academy.db    # SQLite database (created automatically)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## 🚀 Usage

1. Start the backend server first (port 8000)
2. Start the frontend development server (port 3000)
3. Navigate to `http://localhost:3000` in your browser
4. Explore the different modules:
   - **Learning Hub**: Browse courses and educational content
   - **Market Intelligence**: Check live prices and forecasts
   - **Agri-Bot**: Ask questions about farming
   - **Sustainable Wiki**: Learn about waste management and resource optimization

## 🌐 Language Support

The platform supports multiple languages:
- Urdu (اردو)
- English

Switch languages using the dropdown in the navbar.

## 🔧 Configuration

### API Configuration

Set the backend API URL in `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

Or create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
```

### Gemini API Integration

To enable the full AI chatbot functionality:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add the API key to the backend environment or update the chat endpoint in `backend/main.py`

## 📊 Database Schema

The SQLite database includes tables for:
- Users
- Courses (with multilingual content)
- Market Prices
- Weather Alerts
- Pest Alerts
- Wiki Articles
- Chat History

## 🎨 Features Implementation

- ✅ Responsive, mobile-first design
- ✅ Multilingual support (Urdu/English)
- ✅ Live price tracking
- ✅ Demand forecasting
- ✅ Weather and pest alerts
- ✅ Interactive learning modules
- ✅ Resource calculators
- ✅ AI chatbot interface (ready for Gemini integration)

## 🔮 Future Enhancements

- Full Gemini API integration for advanced AI responses
- Real-time data scraping from mandi websites
- Advanced Prophet/ARIMA forecasting models
- Voice input for Agri-Bot
- Push notifications for alerts
- Farmer community forum
- Mobile app version

## 📝 License

This project is developed for the BUILD4BΞTTΞR Hackathon.

## 👥 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ for Pakistani Farmers**


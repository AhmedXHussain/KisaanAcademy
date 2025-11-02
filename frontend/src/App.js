import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import LearningHub from './pages/LearningHub';
import MarketIntelligence from './pages/MarketIntelligence';
import AgriBot from './pages/AgriBot';
import SustainableWiki from './pages/SustainableWiki';
import AgriTools from './pages/AgriTools';
import './App.css';

function App() {
  const [language, setLanguage] = useState('ur');

  return (
    <Router>
      <div className="App" dir={language === 'ur' ? 'rtl' : 'ltr'}>
        <Navbar language={language} setLanguage={setLanguage} />
        <Routes>
          <Route path="/" element={<Home language={language} />} />
          <Route path="/learning" element={<LearningHub language={language} />} />
          <Route path="/market" element={<MarketIntelligence language={language} />} />
          <Route path="/agri-bot" element={<AgriBot language={language} />} />
          <Route path="/wiki" element={<SustainableWiki language={language} />} />
          <Route path="/tools" element={<AgriTools language={language} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;


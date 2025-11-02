import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiHome, FiBook, FiTrendingUp, FiMessageCircle, FiFeather, FiMenu, FiX, FiTool } from 'react-icons/fi';
import './Navbar.css';

const Navbar = ({ language, setLanguage }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const translations = {
    ur: {
      home: 'ہوم',
      learning: 'سیکھیں',
      market: 'مارکیٹ',
      bot: 'اگری بوٹ',
      wiki: 'وسٹا',
      tools: 'ٹولز',
      lang: 'Language'
    },
    en: {
      home: 'Home',
      learning: 'Learning',
      market: 'Market',
      bot: 'Agri-Bot',
      wiki: 'Wiki',
      tools: 'Tools',
      lang: 'زبان'
    }
  };

  const t = translations[language];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <FiFeather className="logo-icon" />
          <span>Kisaan Academy</span>
        </Link>

        <div className={isMenuOpen ? 'navbar-menu active' : 'navbar-menu'}>
          <Link 
            to="/" 
            className={`navbar-link ${isActive('/') ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(false)}
          >
            <FiHome /> <span>{t.home}</span>
          </Link>
          <Link 
            to="/learning" 
            className={`navbar-link ${isActive('/learning') ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(false)}
          >
            <FiBook /> <span>{t.learning}</span>
          </Link>
          <Link 
            to="/market" 
            className={`navbar-link ${isActive('/market') ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(false)}
          >
            <FiTrendingUp /> <span>{t.market}</span>
          </Link>
          <Link 
            to="/agri-bot" 
            className={`navbar-link ${isActive('/agri-bot') ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(false)}
          >
            <FiMessageCircle /> <span>{t.bot}</span>
          </Link>
          <Link 
            to="/wiki" 
            className={`navbar-link ${isActive('/wiki') ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(false)}
          >
            <FiFeather /> <span>{t.wiki}</span>
          </Link>
          <Link 
            to="/tools" 
            className={`navbar-link ${isActive('/tools') ? 'active' : ''}`}
            onClick={() => setIsMenuOpen(false)}
          >
            <FiTool /> <span>{t.tools}</span>
          </Link>
        </div>

        <div className="navbar-actions">
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value)}
            className="language-select"
          >
            <option value="ur">اردو</option>
            <option value="en">English</option>
          </select>
          <button 
            className="menu-toggle"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;


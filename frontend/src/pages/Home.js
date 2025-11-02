import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiBook, FiTrendingUp, FiMessageCircle, FiFeather, FiArrowRight } from 'react-icons/fi';
import { apiService } from '../services/api';
import './Home.css';

const Home = ({ language }) => {
  const [weatherAlerts, setWeatherAlerts] = useState([]);
  const [pestAlerts, setPestAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, [language]);

  const fetchAlerts = async () => {
    try {
      const [weatherResponse, pestsResponse] = await Promise.all([
        apiService.getWeatherAlerts(null, language),
        apiService.getPestAlerts(null, language),
      ]);
      
      // Handle response - FastAPI returns the array directly, but axios wraps it in .data
      const weatherData = Array.isArray(weatherResponse.data) ? weatherResponse.data : (weatherResponse.data?.data || []);
      const pestsData = Array.isArray(pestsResponse.data) ? pestsResponse.data : (pestsResponse.data?.data || []);
      
      console.log('Weather alerts received:', weatherData.length);
      console.log('Pest alerts received:', pestsData.length);
      
      setWeatherAlerts(weatherData.slice(0, 3));
      setPestAlerts(pestsData.slice(0, 3));
    } catch (error) {
      console.error('Error fetching alerts:', error);
      console.error('Error details:', error.response?.data || error.message);
      // Set empty arrays on error so UI shows "No alerts"
      setWeatherAlerts([]);
      setPestAlerts([]);
    } finally {
      setLoading(false);
    }
  };

  const translations = {
    ur: {
      heroTitle: 'کسان اکیڈمی میں خوش آمدید',
      heroSubtitle: 'کسانوں کو علم، اعداد و شمار، اور براہ راست مدد فراہم کرنے والا ایک جامع پلیٹ فارم',
      getStarted: 'شروع کریں',
      learnMore: 'مزید جانیں',
      features: 'خصوصیات',
      learningHub: 'سیکھنے کا مرکز',
      learningDesc: 'جدید کھیتی باڑی کی تکنیکوں کے بارے میں مفت کورسز اور تعلیم',
      marketIntelligence: 'مارکیٹ انٹیلی جنس',
      marketDesc: 'زندہ قیمتوں کا ٹریکر اور طلب کی پیش گوئی',
      agriBot: 'اگری بوٹ',
      botDesc: 'AI سے چلنے والا چیٹ بوٹ جو 24/7 سوالات کے جوابات دیتا ہے',
      wiki: 'پائیدار طریقوں کی ویکی',
      wikiDesc: 'فضلہ انتظام اور وسائل کے کیلکولیٹرز کے لیے عملی گائیڈز',
      recentAlerts: 'حالیہ الرٹس',
      weather: 'موسم',
      pests: 'کیڑے',
      viewAll: 'سب دیکھیں',
    },
    en: {
      heroTitle: 'Welcome to Kisaan Academy',
      heroSubtitle: 'A comprehensive platform empowering farmers with knowledge, data, and direct support',
      getStarted: 'Get Started',
      learnMore: 'Learn More',
      features: 'Features',
      learningHub: 'Learning Hub',
      learningDesc: 'Free courses and education on modern farming techniques',
      marketIntelligence: 'Market Intelligence',
      marketDesc: 'Live price tracker and demand forecasting',
      agriBot: 'Agri-Bot',
      botDesc: 'AI-powered chatbot answering questions 24/7',
      wiki: 'Sustainable Practices Wiki',
      wikiDesc: 'Practical guides for waste management and resource calculators',
      recentAlerts: 'Recent Alerts',
      weather: 'Weather',
      pests: 'Pests',
      viewAll: 'View All',
    },
  };

  const t = translations[language];

  return (
    <div className="home">
      <section className="hero">
        <div className="container">
          <h1 className="urdu-text">{t.heroTitle}</h1>
          <p className="hero-subtitle">{t.heroSubtitle}</p>
          <div className="hero-buttons">
            <Link to="/learning" className="btn btn-primary">
              {t.getStarted}
              <FiArrowRight />
            </Link>
            <Link to="/wiki" className="btn btn-outline">
              {t.learnMore}
            </Link>
          </div>
        </div>
      </section>

      <section className="features-section section">
        <div className="container">
          <h2 className="section-title">{t.features}</h2>
          <div className="features-grid grid grid-4">
            <Link to="/learning" className="feature-card card">
              <div className="feature-icon">
                <FiBook />
              </div>
              <h3>{t.learningHub}</h3>
              <p>{t.learningDesc}</p>
              <span className="feature-link">
                {t.learnMore} <FiArrowRight />
              </span>
            </Link>

            <Link to="/market" className="feature-card card">
              <div className="feature-icon">
                <FiTrendingUp />
              </div>
              <h3>{t.marketIntelligence}</h3>
              <p>{t.marketDesc}</p>
              <span className="feature-link">
                {t.learnMore} <FiArrowRight />
              </span>
            </Link>

            <Link to="/agri-bot" className="feature-card card">
              <div className="feature-icon">
                <FiMessageCircle />
              </div>
              <h3>{t.agriBot}</h3>
              <p>{t.botDesc}</p>
              <span className="feature-link">
                {t.learnMore} <FiArrowRight />
              </span>
            </Link>

            <Link to="/wiki" className="feature-card card">
              <div className="feature-icon">
                <FiFeather />
              </div>
              <h3>{t.wiki}</h3>
              <p>{t.wikiDesc}</p>
              <span className="feature-link">
                {t.learnMore} <FiArrowRight />
              </span>
            </Link>
          </div>
        </div>
      </section>

      <section className="alerts-section section">
        <div className="container">
          <h2 className="section-title">{t.recentAlerts}</h2>
          <div className="alerts-grid grid grid-2">
            <div className="alerts-card card">
              <h3>{t.weather}</h3>
              {weatherAlerts.length > 0 ? (
                <>
                  {weatherAlerts.map((alert) => (
                    <div key={alert.id} className={`alert alert-${alert.severity === 'high' ? 'danger' : 'warning'}`}>
                      <div>
                        <strong>{alert.region}</strong>
                        <p>{alert.message}</p>
                      </div>
                    </div>
                  ))}
                  <Link to="/agri-bot" className="view-all-link">
                    {t.viewAll} <FiArrowRight />
                  </Link>
                </>
              ) : (
                <p style={{ color: '#718096', textAlign: 'center', padding: '20px' }}>
                  {language === 'ur' ? 'کوئی الرٹ نہیں' : 'No alerts'}
                </p>
              )}
            </div>

            <div className="alerts-card card">
              <h3>{t.pests}</h3>
              {pestAlerts.length > 0 ? (
                <>
                  {pestAlerts.map((alert) => (
                    <div key={alert.id} className={`alert alert-${alert.severity === 'high' ? 'danger' : alert.severity === 'medium' ? 'warning' : 'info'}`}>
                      <div>
                        <strong>{alert.pest_name} - {alert.crop_affected}</strong>
                        <p>{alert.prevention ? alert.prevention.substring(0, 100) + '...' : ''}</p>
                      </div>
                    </div>
                  ))}
                  <Link to="/agri-bot" className="view-all-link">
                    {t.viewAll} <FiArrowRight />
                  </Link>
                </>
              ) : (
                <p style={{ color: '#718096', textAlign: 'center', padding: '20px' }}>
                  {language === 'ur' ? 'کوئی الرٹ نہیں' : 'No alerts'}
                </p>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;


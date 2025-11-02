import React, { useState, useEffect, useRef } from 'react';
import { FiSend, FiMessageCircle, FiUser } from 'react-icons/fi';
import { apiService } from '../services/api';
import './AgriBot.css';

const AgriBot = ({ language }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [alerts, setAlerts] = useState({ weather: [], pests: [] });
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchAlerts();
    // Add welcome message
    setMessages([{
      type: 'bot',
      text: language === 'ur' 
        ? 'السلام علیکم! میں آپ کا اگری بوٹ ہوں۔ میں آپ کی فصلوں، قیمتوں، موسم، اور کھیتی باڑی کے بارے میں کوئی بھی سوال پوچھ سکتے ہیں۔'
        : 'Hello! I am your Agri-Bot. You can ask me any questions about crops, prices, weather, and farming.',
      timestamp: new Date().toISOString(),
    }]);
  }, [language]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchAlerts = async () => {
    try {
      const [weather, pests] = await Promise.all([
        apiService.getWeatherAlerts(null, language),
        apiService.getPestAlerts(null, language),
      ]);
      setAlerts({
        weather: weather.data.slice(0, 5),
        pests: pests.data.slice(0, 5),
      });
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      type: 'user',
      text: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await apiService.sendChatMessage(input, null, language);
      const botMessage = {
        type: 'bot',
        text: response.data.answer,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'bot',
        text: language === 'ur' 
          ? 'معافی، میں اس وقت آپ کے سوال کا جواب نہیں دے سکتا۔ براہ کرم دوبارہ کوشش کریں۔'
          : 'Sorry, I cannot answer your question right now. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const translations = {
    ur: {
      title: 'اگری بوٹ',
      subtitle: 'AI سے چلنے والا چیٹ بوٹ جو 24/7 آپ کے سوالات کے جوابات دیتا ہے',
      placeholder: 'اپنا سوال یہاں لکھیں...',
      send: 'بھیجیں',
      weatherAlerts: 'موسم کی الرٹس',
      pestAlerts: 'کیڑے کی الرٹس',
      region: 'خطہ',
      severity: 'شدت',
      crop: 'فصل',
      prevention: 'بچاؤ',
      noAlerts: 'کوئی الرٹس نہیں',
      loading: 'جواب آ رہا ہے...',
    },
    en: {
      title: 'Agri-Bot',
      subtitle: 'AI-powered chatbot answering your questions 24/7',
      placeholder: 'Type your question here...',
      send: 'Send',
      weatherAlerts: 'Weather Alerts',
      pestAlerts: 'Pest Alerts',
      region: 'Region',
      severity: 'Severity',
      crop: 'Crop',
      prevention: 'Prevention',
      noAlerts: 'No alerts',
      loading: 'Getting response...',
    },
  };

  const t = translations[language];

  return (
    <div className="agri-bot">
      <section className="bot-header section">
        <div className="container">
          <h1 className="section-title">{t.title}</h1>
          <p className="section-subtitle">{t.subtitle}</p>
        </div>
      </section>

      <div className="bot-container">
        <div className="container">
          <div className="bot-layout">
            <div className="chat-section">
              <div className="chat-messages">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
                  >
                    <div className="message-icon">
                      {message.type === 'user' ? <FiUser /> : <FiMessageCircle />}
                    </div>
                    <div className="message-content">
                      <p>{message.text}</p>
                      <span className="message-time">
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="message bot-message">
                    <div className="message-icon">
                      <FiMessageCircle />
                    </div>
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <form className="chat-input-form" onSubmit={handleSend}>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={t.placeholder}
                  disabled={loading}
                />
                <button type="submit" disabled={loading || !input.trim()} className="send-button">
                  <FiSend />
                </button>
              </form>
            </div>

            <div className="alerts-sidebar">
              <div className="alerts-section">
                <h3>{t.weatherAlerts}</h3>
                {alerts.weather.length === 0 ? (
                  <p className="no-alerts">{t.noAlerts}</p>
                ) : (
                  alerts.weather.map((alert) => (
                    <div key={alert.id} className={`alert-card alert-${alert.severity === 'high' ? 'danger' : 'warning'}`}>
                      <strong>{alert.region}</strong>
                      <p>{alert.message}</p>
                    </div>
                  ))
                )}
              </div>

              <div className="alerts-section">
                <h3>{t.pestAlerts}</h3>
                {alerts.pests.length === 0 ? (
                  <p className="no-alerts">{t.noAlerts}</p>
                ) : (
                  alerts.pests.map((alert) => (
                    <div key={alert.id} className="alert-card alert-info">
                      <strong>{alert.pest_name} - {alert.crop_affected}</strong>
                      <p>{alert.prevention}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgriBot;


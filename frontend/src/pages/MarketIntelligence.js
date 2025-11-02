import React, { useState, useEffect } from 'react';
import { FiSearch, FiFilter } from 'react-icons/fi';
import { apiService } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './MarketIntelligence.css';

const MarketIntelligence = ({ language }) => {
  const [prices, setPrices] = useState([]);
  const [filteredPrices, setFilteredPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRegion, setFilterRegion] = useState('');

  useEffect(() => {
    fetchPrices();
  }, []);

  useEffect(() => {
    filterPrices();
  }, [searchTerm, filterRegion, prices]);

  const fetchPrices = async () => {
    try {
      const response = await apiService.getMarketPrices();
      setPrices(response.data);
      setFilteredPrices(response.data);
    } catch (error) {
      console.error('Error fetching prices:', error);
    } finally {
      setLoading(false);
    }
  };


  const filterPrices = () => {
    let filtered = [...prices];
    
    if (searchTerm) {
      filtered = filtered.filter(price => 
        price.crop_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (filterRegion) {
      filtered = filtered.filter(price => 
        price.region.toLowerCase() === filterRegion.toLowerCase()
      );
    }
    
    setFilteredPrices(filtered);
  };

  const uniqueRegions = [...new Set(prices.map(p => p.region))];
  const uniqueCrops = [...new Set(prices.map(p => p.crop_name))];

  // Prepare chart data
  const chartData = filteredPrices
    .slice(0, 30)
    .map(price => ({
      name: price.crop_name,
      price: price.price_per_kg,
      region: price.region,
    }));

  const translations = {
    ur: {
      title: 'مارکیٹ انٹیلی جنس',
      subtitle: 'زندہ قیمتوں کا ٹریکر',
      search: 'فصل تلاش کریں...',
      filterByRegion: 'خطے سے فلٹر کریں',
      allRegions: 'تمام خطے',
      livePrices: 'زندہ قیمتیں',
      crop: 'فصل',
      region: 'خطہ',
      price: 'قیمت (فی کلو)',
      mandi: 'منڈی',
      lastUpdated: 'آخری اپ ڈیٹ',
      noData: 'کوئی ڈیٹا نہیں ملا',
      loading: 'لوڈ ہو رہا ہے...',
    },
    en: {
      title: 'Market Intelligence',
      subtitle: 'Live price tracker',
      search: 'Search crop...',
      filterByRegion: 'Filter by Region',
      allRegions: 'All Regions',
      livePrices: 'Live Prices',
      crop: 'Crop',
      region: 'Region',
      price: 'Price (per kg)',
      mandi: 'Mandi',
      lastUpdated: 'Last Updated',
      noData: 'No data found',
      loading: 'Loading...',
    },
  };

  const t = translations[language];

  if (loading) {
    return (
      <div className="market-intelligence">
        <div className="container">
          <div className="spinner"></div>
          <p style={{ textAlign: 'center' }}>{t.loading}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="market-intelligence">
      <section className="market-header section">
        <div className="container">
          <h1 className="section-title">{t.title}</h1>
          <p className="section-subtitle">{t.subtitle}</p>

          <div className="market-filters">
            <div className="search-box">
              <FiSearch />
              <input
                type="text"
                placeholder={t.search}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="filter-box">
              <FiFilter />
              <select
                value={filterRegion}
                onChange={(e) => setFilterRegion(e.target.value)}
              >
                <option value="">{t.allRegions}</option>
                {uniqueRegions.map(region => (
                  <option key={region} value={region}>{region}</option>
                ))}
              </select>
            </div>
          </div>

          {chartData.length > 0 && (
            <div className="chart-card card">
              <h2>{t.livePrices}</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#28a745" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          <div className="prices-table-section">
            <h2>{t.livePrices}</h2>
            {filteredPrices.length === 0 ? (
              <div className="no-data">
                <p>{t.noData}</p>
              </div>
            ) : (
              <div className="prices-table card">
                <table>
                  <thead>
                    <tr>
                      <th>{t.crop}</th>
                      <th>{t.region}</th>
                      <th>{t.price}</th>
                      <th>{t.mandi}</th>
                      <th>{t.lastUpdated}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredPrices.slice(0, 50).map((price) => (
                      <tr key={price.id}>
                        <td>{price.crop_name}</td>
                        <td>{price.region}</td>
                        <td><strong>Rs. {price.price_per_kg.toFixed(2)}</strong></td>
                        <td>{price.mandi_name || '-'}</td>
                        <td>{new Date(price.recorded_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};

export default MarketIntelligence;


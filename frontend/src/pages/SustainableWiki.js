import React, { useState, useEffect } from 'react';
import { FiBook, FiSearch } from 'react-icons/fi';
import { apiService } from '../services/api';
import './SustainableWiki.css';

const SustainableWiki = ({ language }) => {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchArticles();
  }, [language, filterCategory]);

  const fetchArticles = async () => {
    try {
      const category = filterCategory === 'all' ? null : filterCategory;
      const response = await apiService.getWikiArticles(category, language);
      setArticles(response.data);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  // Remove duplicates by ID to ensure unique articles
  const uniqueArticles = articles.filter((article, index, self) =>
    index === self.findIndex((a) => a.id === article.id)
  );

  const filteredArticles = searchTerm
    ? uniqueArticles.filter(article =>
        article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        article.content.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : uniqueArticles;


  const translations = {
    ur: {
      title: 'پائیدار طریقوں کی ویکی',
      subtitle: 'پائیدار کھیتی باڑی اور وسائل کے انتظام کی عملی گائیڈز',
      search: 'تلاش کریں...',
      allCategories: 'تمام زمروں',
      wasteManagement: 'فضلہ انتظام',
      resourceManagement: 'وسائل کا انتظام',
      viewArticle: 'مکمل مضمون دیکھیں',
      backToWiki: 'ویکی پر واپس',
      tags: 'ٹیگز',
      noArticles: 'کوئی مضمون نہیں ملا',
      loading: 'لوڈ ہو رہا ہے...',
    },
    en: {
      title: 'Sustainable Practices Wiki',
      subtitle: 'Practical guides for sustainable farming and resource management',
      search: 'Search...',
      allCategories: 'All Categories',
      wasteManagement: 'Waste Management',
      resourceManagement: 'Resource Management',
      viewArticle: 'View Full Article',
      backToWiki: 'Back to Wiki',
      readMoreOnWikipedia: 'Read More on Wikipedia',
      tags: 'Tags',
      noArticles: 'No articles found',
      loading: 'Loading...',
    },
  };

  const t = translations[language];

  if (loading) {
    return (
      <div className="sustainable-wiki">
        <div className="container">
          <div className="spinner"></div>
          <p style={{ textAlign: 'center' }}>{t.loading}</p>
        </div>
      </div>
    );
  }

  if (selectedArticle) {
    return (
      <div className="sustainable-wiki">
        <div className="container">
          <button onClick={() => setSelectedArticle(null)} className="btn btn-outline">
            {t.backToWiki}
          </button>
          <div className="article-detail card">
            <h1>{selectedArticle.title}</h1>
            <div className="article-meta">
              <span className="article-category">{selectedArticle.category}</span>
              {selectedArticle.tags && (
                <div className="article-tags">
                  {selectedArticle.tags.split(',').map((tag, index) => (
                    <span key={index} className="tag">{tag.trim()}</span>
                  ))}
                </div>
              )}
            </div>
            <div className="article-content">
              <p>{selectedArticle.content}</p>
            </div>
            {selectedArticle.wiki_url && (
              <div className="wiki-link-section" style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid #e2e8f0' }}>
                <a 
                  href={selectedArticle.wiki_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn btn-primary"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}
                >
                  <FiBook /> {t.readMoreOnWikipedia || 'Read More on Wikipedia'}
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="sustainable-wiki">
      <section className="wiki-header section">
        <div className="container">
          <h1 className="section-title">{t.title}</h1>
          <p className="section-subtitle">{t.subtitle}</p>

          <div className="wiki-filters">
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
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
              >
                <option value="all">{t.allCategories}</option>
                <option value="waste_management">{t.wasteManagement}</option>
                <option value="resource_management">{t.resourceManagement}</option>
              </select>
            </div>
          </div>

          {filteredArticles.length === 0 ? (
            <div className="no-articles">
              <p>{t.noArticles}</p>
            </div>
          ) : (
            <div className="articles-grid grid grid-3">
              {filteredArticles.map((article) => (
                <div key={article.id} className="article-card card">
                  <div className="article-icon">
                    <FiBook />
                  </div>
                  <h3>{article.title}</h3>
                  <p className="article-preview">
                    {article.content.substring(0, 150)}...
                  </p>
                  <div className="article-footer">
                    <span className="article-category-badge">{article.category}</span>
                    <div className="article-actions" style={{ display: 'flex', gap: '8px', flexShrink: 0 }}>
                      {article.wiki_url && (
                        <a
                          href={article.wiki_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn btn-outline btn-sm"
                          onClick={(e) => e.stopPropagation()}
                          style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', whiteSpace: 'nowrap' }}
                        >
                          <FiBook /> Wiki
                        </a>
                      )}
                      <button
                        onClick={() => setSelectedArticle(article)}
                        className="btn btn-primary btn-sm"
                        style={{ whiteSpace: 'nowrap' }}
                      >
                        {t.viewArticle}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default SustainableWiki;


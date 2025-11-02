import React, { useState, useEffect } from 'react';
import { FiPlay, FiBookOpen, FiClock } from 'react-icons/fi';
import { apiService } from '../services/api';
import './LearningHub.css';

const LearningHub = ({ language }) => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchCourses();
  }, [language]);

  const fetchCourses = async () => {
    try {
      const response = await apiService.getCourses(language);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  // Remove duplicates by ID to ensure unique courses
  const uniqueCourses = courses.filter((course, index, self) =>
    index === self.findIndex((c) => c.id === course.id)
  );

  const filteredCourses = filter === 'all' 
    ? uniqueCourses 
    : uniqueCourses.filter(course => course.category === filter);

  const translations = {
    ur: {
      title: 'سیکھنے کا مرکز',
      subtitle: 'جدید کھیتی باڑی کی تکنیکوں، پائیدار طریقوں، اور مالی خواندگی کے بارے میں سیکھیں',
      all: 'تمام',
      sustainable: 'پائیدار طریقے',
      waste: 'فضلہ انتظام',
      crop: 'فصل کا انتظام',
      viewCourse: 'کورس دیکھیں',
      category: 'زمرہ',
      description: 'تفصیل',
      noCourses: 'کوئی کورس نہیں ملا',
      loading: 'لوڈ ہو رہا ہے...',
      watchVideo: 'ویڈیو دیکھیں',
      backToCourses: 'کورسز پر واپس',
    },
    en: {
      title: 'Learning Hub',
      subtitle: 'Learn about modern farming techniques, sustainable practices, and financial literacy',
      all: 'All',
      sustainable: 'Sustainable Practices',
      waste: 'Waste Management',
      crop: 'Crop Management',
      viewCourse: 'View Course',
      category: 'Category',
      description: 'Description',
      noCourses: 'No courses found',
      loading: 'Loading...',
      watchVideo: 'Watch Video',
      backToCourses: 'Back to Courses',
    },
  };

  const t = translations[language];

  if (loading) {
    return (
      <div className="learning-hub">
        <div className="container">
          <div className="spinner"></div>
          <p style={{ textAlign: 'center' }}>{t.loading}</p>
        </div>
      </div>
    );
  }

  if (selectedCourse) {
    return (
      <div className="learning-hub">
        <div className="container">
          <button onClick={() => setSelectedCourse(null)} className="btn btn-outline">
            {t.backToCourses}
          </button>
          <div className="course-detail card">
            <h1>{selectedCourse.title}</h1>
            <p className="course-category">{selectedCourse.category}</p>
            {selectedCourse.video_url && (
              <div className="video-section" style={{ marginBottom: '24px', padding: '20px', background: '#f7fafc', borderRadius: '8px' }}>
                <h3 style={{ marginBottom: '12px', fontSize: '1.2rem' }}>{t.watchVideoOnYouTube || 'Watch Video on YouTube'}</h3>
                <a 
                  href={selectedCourse.video_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn btn-primary"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', fontSize: '1rem', padding: '12px 24px' }}
                >
                  <FiPlay /> {t.watchVideo}
                </a>
                <p style={{ marginTop: '8px', fontSize: '0.9rem', color: '#718096' }}>
                  {language === 'ur' ? 'یوٹیوب پر تعلیمی ویڈیو دیکھیں' : 'Watch educational video on YouTube'}
                </p>
              </div>
            )}
            <div className="course-content">
              <h2>{t.description}</h2>
              <p>{selectedCourse.description}</p>
              <div className="content-text">
                {selectedCourse.content}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="learning-hub">
      <section className="learning-header section">
        <div className="container">
          <h1 className="section-title">{t.title}</h1>
          <p className="section-subtitle">{t.subtitle}</p>
          
          <div className="filter-buttons">
            <button
              className={filter === 'all' ? 'filter-btn active' : 'filter-btn'}
              onClick={() => setFilter('all')}
            >
              {t.all}
            </button>
            <button
              className={filter === 'sustainable_practices' ? 'filter-btn active' : 'filter-btn'}
              onClick={() => setFilter('sustainable_practices')}
            >
              {t.sustainable}
            </button>
            <button
              className={filter === 'waste_management' ? 'filter-btn active' : 'filter-btn'}
              onClick={() => setFilter('waste_management')}
            >
              {t.waste}
            </button>
          </div>

          {filteredCourses.length === 0 ? (
            <div className="no-courses">
              <p>{t.noCourses}</p>
            </div>
          ) : (
            <div className="courses-grid grid grid-3">
              {filteredCourses.map((course) => (
                <div key={course.id} className="course-card card">
                  {course.video_url && (
                    <div className="course-video-icon">
                      <FiPlay />
                    </div>
                  )}
                  <div className="course-header">
                    <span className="course-category-badge">{course.category}</span>
                    <FiBookOpen className="course-icon" />
                  </div>
                  <h3>{course.title}</h3>
                  <p className="course-description">{course.description}</p>
                  <button
                    onClick={() => setSelectedCourse(course)}
                    className="btn btn-primary"
                    style={{ width: '100%', marginTop: 'auto' }}
                  >
                    {t.viewCourse}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default LearningHub;


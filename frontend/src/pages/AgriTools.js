import React, { useState } from 'react';
import { FiDroplet, FiZap, FiPackage, FiTrash2 } from 'react-icons/fi';
import './AgriTools.css';

const AgriTools = ({ language }) => {
  const [activeTool, setActiveTool] = useState('water');
  const [calcValues, setCalcValues] = useState({
    area: '',
    cropType: '',
    irrigationType: '',
    soilType: '',
    energyUsage: '',
    wasteType: '',
    wasteAmount: '',
    fertilizerType: '',
  });
  const [result, setResult] = useState(null);

  const translations = {
    ur: {
      title: 'زرعی ٹولز',
      subtitle: 'پانی، کھاد، توانائی، اور فضلہ انتظام کے لیے کیلکولیٹرز',
      waterCalculator: 'پانی کا کیلکولیٹر',
      fertilizerCalculator: 'کھاد کا کیلکولیٹر',
      energyOptimization: 'توانائی کی بہتری',
      wasteManagement: 'فضلہ انتظام',
      area: 'رقبہ (ایکڑ)',
      cropType: 'فصل کی قسم',
      irrigationType: 'اریگیشن کی قسم',
      soilType: 'مٹی کی قسم',
      waterRequired: 'پانی کی ضرورت',
      fertilizerRequired: 'کھاد کی ضرورت',
      energySaved: 'توانائی کی بچت',
      wasteConverted: 'فضلہ تبدیل شدہ',
      calculate: 'حساب کریں',
      reset: 'دوبارہ',
      litersPerWeek: 'لیٹر فی ہفتہ',
      kg: 'کلوگرام',
      kwh: 'کلو واٹ گھنٹے',
      result: 'نتیجہ',
    },
    en: {
      title: 'Agricultural Tools',
      subtitle: 'Calculators for water, fertilizer, energy, and waste management',
      waterCalculator: 'Water Calculator',
      fertilizerCalculator: 'Fertilizer Calculator',
      energyOptimization: 'Energy Optimization',
      wasteManagement: 'Waste Management',
      area: 'Area (Acres)',
      cropType: 'Crop Type',
      irrigationType: 'Irrigation Type',
      soilType: 'Soil Type',
      waterRequired: 'Water Required',
      fertilizerRequired: 'Fertilizer Required',
      energySaved: 'Energy Saved',
      wasteConverted: 'Waste Converted',
      calculate: 'Calculate',
      reset: 'Reset',
      litersPerWeek: 'Liters per week',
      kg: 'Kilograms',
      kwh: 'KWh',
      result: 'Result',
    },
  };

  const t = translations[language];

  const handleCalculate = () => {
    const area = parseFloat(calcValues.area) || 0;
    
    if (area <= 0) {
      alert(language === 'ur' ? 'براہ کرم صحیح رقبہ درج کریں' : 'Please enter a valid area');
      return;
    }

    let calculation = null;

    switch (activeTool) {
      case 'water':
        // Water requirement calculation based on crop and irrigation type
        const baseWaterPerAcre = 27000; // liters per acre per week (average)
        const cropMultiplier = {
          wheat: 0.8,
          rice: 1.5,
          cotton: 1.2,
          vegetables: 1.3,
        };
        const irrigationMultiplier = {
          flood: 1.5,
          sprinkler: 1.0,
          drip: 0.6,
        };
        
        const crop = calcValues.cropType || 'wheat';
        const irrigation = calcValues.irrigationType || 'flood';
        
        const waterRequired = area * baseWaterPerAcre * 
          (cropMultiplier[crop] || 1) * 
          (irrigationMultiplier[irrigation] || 1);
        
        calculation = {
          label: t.waterRequired,
          value: waterRequired.toFixed(2),
          unit: t.litersPerWeek,
          details: language === 'ur' 
            ? `فصل: ${calcValues.cropType || 'عام'}, اریگیشن: ${calcValues.irrigationType || 'عام'}`
            : `Crop: ${calcValues.cropType || 'General'}, Irrigation: ${calcValues.irrigationType || 'General'}`,
        };
        break;

      case 'fertilizer':
        // Fertilizer requirement based on crop and area
        const fertilizerPerAcre = {
          wheat: 100,
          rice: 120,
          cotton: 80,
          vegetables: 150,
        };
        
        const fertilizerType = calcValues.fertilizerType || 'npk';
        const cropFert = calcValues.cropType || 'wheat';
        const fertilizerRequired = area * (fertilizerPerAcre[cropFert] || 100);
        
        calculation = {
          label: t.fertilizerRequired,
          value: fertilizerRequired.toFixed(2),
          unit: t.kg,
          details: language === 'ur'
            ? `فصل: ${cropFert}, کھاد کی قسم: ${fertilizerType}`
            : `Crop: ${cropFert}, Fertilizer Type: ${fertilizerType}`,
        };
        break;

      case 'energy':
        // Energy optimization calculation
        const currentUsage = parseFloat(calcValues.energyUsage) || 0;
        if (currentUsage <= 0) {
          alert(language === 'ur' ? 'براہ کرم توانائی کا استعمال درج کریں' : 'Please enter energy usage');
          return;
        }
        
        // Assuming 20% energy savings with optimization
        const energySaved = currentUsage * 0.20;
        const costSaved = energySaved * 15; // Assuming 15 rupees per KWh
        
        calculation = {
          label: t.energySaved,
          value: energySaved.toFixed(2),
          unit: t.kwh,
          details: language === 'ur'
            ? `بچت شدہ رقم: ${costSaved.toFixed(2)} روپے`
            : `Cost Saved: ₹${costSaved.toFixed(2)}`,
        };
        break;

      case 'waste':
        // Waste management calculation
        const wasteAmount = parseFloat(calcValues.wasteAmount) || 0;
        if (wasteAmount <= 0) {
          alert(language === 'ur' ? 'براہ کرم فضلے کی مقدار درج کریں' : 'Please enter waste amount');
          return;
        }
        
        // Conversion rates: 1 ton waste = ~300 kg compost
        const compostProduced = wasteAmount * 0.3;
        const biocharProduced = wasteAmount * 0.2;
        
        calculation = {
          label: t.wasteConverted,
          value: compostProduced.toFixed(2),
          unit: t.kg + ' (Compost)',
          details: language === 'ur'
            ? `بائیوچار: ${biocharProduced.toFixed(2)} کلوگرام`
            : `Biochar: ${biocharProduced.toFixed(2)} kg`,
        };
        break;

      default:
        return;
    }

    setResult(calculation);
  };

  const handleReset = () => {
    setCalcValues({
      area: '',
      cropType: '',
      irrigationType: '',
      soilType: '',
      energyUsage: '',
      wasteType: '',
      wasteAmount: '',
      fertilizerType: '',
    });
    setResult(null);
  };

  const tools = [
    {
      id: 'water',
      icon: <FiDroplet />,
      title: t.waterCalculator,
      description: language === 'ur' ? 'پانی کی ضرورت کا حساب' : 'Calculate water requirements',
    },
    {
      id: 'fertilizer',
      icon: <FiPackage />,
      title: t.fertilizerCalculator,
      description: language === 'ur' ? 'کھاد کی ضرورت کا حساب' : 'Calculate fertilizer needs',
    },
    {
      id: 'energy',
      icon: <FiZap />,
      title: t.energyOptimization,
      description: language === 'ur' ? 'توانائی کی بہتری' : 'Optimize energy usage',
    },
    {
      id: 'waste',
      icon: <FiTrash2 />,
      title: t.wasteManagement,
      description: language === 'ur' ? 'فضلہ انتظام کا حساب' : 'Calculate waste conversion',
    },
  ];

  return (
    <div className="agri-tools">
      <section className="tools-header section">
        <div className="container">
          <h1 className="section-title">{t.title}</h1>
          <p className="section-subtitle">{t.subtitle}</p>
        </div>
      </section>

      <div className="tools-container">
        <div className="container">
          <div className="tools-layout">
            <div className="tools-sidebar">
              <h3 style={{ marginBottom: '16px', color: '#2d3748' }}>
                {language === 'ur' ? 'ٹولز' : 'Tools'}
              </h3>
              <div className="tools-list">
                {tools.map((tool) => (
                  <button
                    key={tool.id}
                    onClick={() => {
                      setActiveTool(tool.id);
                      setResult(null);
                    }}
                    className={`tool-button ${activeTool === tool.id ? 'active' : ''}`}
                  >
                    <span className="tool-icon">{tool.icon}</span>
                    <div className="tool-info">
                      <div className="tool-title">{tool.title}</div>
                      <div className="tool-description">{tool.description}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <div className="tool-content">
              <div className="tool-card card">
                <div className="tool-header">
                  <h2>{tools.find(t => t.id === activeTool)?.title}</h2>
                  <p>{tools.find(t => t.id === activeTool)?.description}</p>
                </div>

                <div className="calculator-form">
                  <div className="form-group">
                    <label>{t.area} *</label>
                    <input
                      type="number"
                      value={calcValues.area}
                      onChange={(e) => setCalcValues({ ...calcValues, area: e.target.value })}
                      placeholder="0"
                      min="0"
                      step="0.1"
                    />
                  </div>

                  {activeTool === 'water' && (
                    <>
                      <div className="form-group">
                        <label>{t.cropType}</label>
                        <select
                          value={calcValues.cropType}
                          onChange={(e) => setCalcValues({ ...calcValues, cropType: e.target.value })}
                        >
                          <option value="">-- {language === 'ur' ? 'منتخب کریں' : 'Select'} --</option>
                          <option value="wheat">{language === 'ur' ? 'گندم' : 'Wheat'}</option>
                          <option value="rice">{language === 'ur' ? 'چاول' : 'Rice'}</option>
                          <option value="cotton">{language === 'ur' ? 'کپاس' : 'Cotton'}</option>
                          <option value="vegetables">{language === 'ur' ? 'سبزیاں' : 'Vegetables'}</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>{t.irrigationType}</label>
                        <select
                          value={calcValues.irrigationType}
                          onChange={(e) => setCalcValues({ ...calcValues, irrigationType: e.target.value })}
                        >
                          <option value="">-- {language === 'ur' ? 'منتخب کریں' : 'Select'} --</option>
                          <option value="flood">{language === 'ur' ? 'سیلاب اریگیشن' : 'Flood Irrigation'}</option>
                          <option value="sprinkler">{language === 'ur' ? 'سپرنکلر' : 'Sprinkler'}</option>
                          <option value="drip">{language === 'ur' ? 'ڈرپ اریگیشن' : 'Drip Irrigation'}</option>
                        </select>
                      </div>
                    </>
                  )}

                  {activeTool === 'fertilizer' && (
                    <>
                      <div className="form-group">
                        <label>{t.cropType}</label>
                        <select
                          value={calcValues.cropType}
                          onChange={(e) => setCalcValues({ ...calcValues, cropType: e.target.value })}
                        >
                          <option value="">-- {language === 'ur' ? 'منتخب کریں' : 'Select'} --</option>
                          <option value="wheat">{language === 'ur' ? 'گندم' : 'Wheat'}</option>
                          <option value="rice">{language === 'ur' ? 'چاول' : 'Rice'}</option>
                          <option value="cotton">{language === 'ur' ? 'کپاس' : 'Cotton'}</option>
                          <option value="vegetables">{language === 'ur' ? 'سبزیاں' : 'Vegetables'}</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>{language === 'ur' ? 'کھاد کی قسم' : 'Fertilizer Type'}</label>
                        <select
                          value={calcValues.fertilizerType}
                          onChange={(e) => setCalcValues({ ...calcValues, fertilizerType: e.target.value })}
                        >
                          <option value="">-- {language === 'ur' ? 'منتخب کریں' : 'Select'} --</option>
                          <option value="npk">{language === 'ur' ? 'NPK' : 'NPK'}</option>
                          <option value="urea">{language === 'ur' ? 'یوریا' : 'Urea'}</option>
                          <option value="dap">{language === 'ur' ? 'DAP' : 'DAP'}</option>
                          <option value="organic">{language === 'ur' ? 'نامیاتی' : 'Organic'}</option>
                        </select>
                      </div>
                    </>
                  )}

                  {activeTool === 'energy' && (
                    <div className="form-group">
                      <label>{language === 'ur' ? 'موجودہ توانائی کا استعمال (KWh)' : 'Current Energy Usage (KWh)'}</label>
                      <input
                        type="number"
                        value={calcValues.energyUsage}
                        onChange={(e) => setCalcValues({ ...calcValues, energyUsage: e.target.value })}
                        placeholder="0"
                        min="0"
                        step="0.1"
                      />
                    </div>
                  )}

                  {activeTool === 'waste' && (
                    <>
                      <div className="form-group">
                        <label>{language === 'ur' ? 'فضلے کی قسم' : 'Waste Type'}</label>
                        <select
                          value={calcValues.wasteType}
                          onChange={(e) => setCalcValues({ ...calcValues, wasteType: e.target.value })}
                        >
                          <option value="">-- {language === 'ur' ? 'منتخب کریں' : 'Select'} --</option>
                          <option value="crop">{language === 'ur' ? 'فصل کا فضلہ' : 'Crop Waste'}</option>
                          <option value="organic">{language === 'ur' ? 'نامیاتی فضلہ' : 'Organic Waste'}</option>
                          <option value="manure">{language === 'ur' ? 'گوبر' : 'Manure'}</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>{language === 'ur' ? 'فضلے کی مقدار (ٹن)' : 'Waste Amount (Tons)'}</label>
                        <input
                          type="number"
                          value={calcValues.wasteAmount}
                          onChange={(e) => setCalcValues({ ...calcValues, wasteAmount: e.target.value })}
                          placeholder="0"
                          min="0"
                          step="0.1"
                        />
                      </div>
                    </>
                  )}

                  <div className="form-actions">
                    <button onClick={handleCalculate} className="btn btn-primary">
                      {t.calculate}
                    </button>
                    <button onClick={handleReset} className="btn btn-outline">
                      {t.reset}
                    </button>
                  </div>

                  {result && (
                    <div className="calculation-result">
                      <h3>{t.result}</h3>
                      <div className="result-card">
                        <div className="result-value">
                          <span className="result-number">{result.value}</span>
                          <span className="result-unit">{result.unit}</span>
                        </div>
                        <div className="result-label">{result.label}</div>
                        {result.details && (
                          <div className="result-details">{result.details}</div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgriTools;


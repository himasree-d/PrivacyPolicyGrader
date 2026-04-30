import React, { useState } from 'react';
import { Shield, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!url) return;
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, name: 'UI Analysis' }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed. Check your API key or backend status.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="bg-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
      </div>
      
      <div className="app-container">
        <div className="header">
          <h1>Privacy Grader</h1>
          <p>Transparent evaluation of data ethics, powered by advanced reasoning.</p>
        </div>

        <div className="input-section">
          <div className="input-group">
            <input 
              type="text" 
              placeholder="Paste a Privacy Policy URL..." 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={handleAnalyze} disabled={loading}>
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Loader2 className="animate-spin" size={18} /> Analyzing
                </span>
              ) : 'Evaluate'}
            </button>
          </div>
          {error && <p style={{ color: '#a65d5d', marginTop: '1rem', textAlign: 'center', fontSize: '1rem', fontWeight: '600' }}>{error}</p>}
        </div>

        {result && (
          <div className="results-grid">
            <div className="grade-card">
              <h2>Official Grade</h2>
              <div className="grade-letter">
                {result.grade}
              </div>
              <div className="risk-score-label">Risk Exposure: {result.final_risk_score}%</div>
              <div className="justification-text">
                {result.justification}
              </div>
            </div>

            <div className="details-card">
              <div className="detail-item">
                <h3><Shield size={24} color="var(--accent)" strokeWidth={2.5} /> Data Collected</h3>
                <ul>
                  {result.data_collected?.map((item, i) => <li key={i}>{item}</li>)}
                </ul>
              </div>
              
              <div className="detail-item">
                <h3><AlertTriangle size={24} color="#a65d5d" strokeWidth={2.5} /> Critical Red Flags</h3>
                <ul className="red-flags">
                  {result.red_flags?.map((item, i) => <li key={i}>{item}</li>)}
                </ul>
              </div>

              <div className="detail-item">
                <h3><CheckCircle size={24} color="var(--primary)" strokeWidth={2.5} /> Your Rights</h3>
                <ul>
                  {result.user_rights?.map((item, i) => <li key={i}>{item}</li>)}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default App;

import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to fetch results');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Logistics Knowledge Base Search</h1>
        <div className="search-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your logistics query..."
            className="search-input"
          />
          <button onClick={handleSearch} disabled={loading} className="search-button">
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
        {results && (
          <div className="results">
            <h2>Query: {results.query}</h2>
            {results.result.map((res, index) => (
              <div key={index} className="result-section">
                <h3>{res.type === 'regular_result' ? 'Standard Results' : 'Expanded Results'}</h3>
                <ul>
                  {res.response.map((item) => (
                    <li key={item.rank} className="result-item">
                      <p>{item.query}</p>
                      <small>Rank: {item.rank} | Score: {item.score.toFixed(4)}</small>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;

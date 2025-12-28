import React, { useState } from 'react';
import ImageInput from './components/ImageInput';
import AnalysisResult from './components/AnalysisResult';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { analyzeProduct, analyzeProductUpload } from './api';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('url'); // 'url' or 'upload'

  const handleAnalyzeUrl = async (urls) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeProduct(urls);
      setResult(data);
    } catch (err) {
      setError(err.message || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeUpload = async (files) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeProductUpload(files);
      setResult(data);
    } catch (err) {
      setError(err.message || "Upload analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <Navbar />
      <div className="main-content">
        <div className="tabs">
          <button
            className={activeTab === 'url' ? 'active' : ''}
            onClick={() => setActiveTab('url')}
          >
            Image URLs
          </button>
          <button
            className={activeTab === 'upload' ? 'active' : ''}
            onClick={() => setActiveTab('upload')}
          >
            Upload Files
          </button>
        </div>

        {activeTab === 'url' ? (
          <ImageInput onAnalyze={handleAnalyzeUrl} isLoading={loading} />
        ) : (
          <FileUpload onAnalyze={handleAnalyzeUpload} isLoading={loading} />
        )}

        {error && <div className="error-message">Error: {error}</div>}

        <AnalysisResult result={result} />
      </div>
      <Footer />
    </div>
  );
}

// Temporary inline component until moved to own file
function FileUpload({ onAnalyze, isLoading }) {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFiles.length > 0) {
      onAnalyze(selectedFiles);
    }
  };

  return (
    <div className="input-section">
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileChange}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || selectedFiles.length === 0}>
          {isLoading ? 'Running Analysis...' : 'Analyze Uploads'}
        </button>
      </form>
      <div className="file-preview">
        {selectedFiles.length > 0 && <p>{selectedFiles.length} file(s) selected:</p>}
        {selectedFiles.map((f, i) => <div key={i}>• {f.name}</div>)}
      </div>
    </div>
  );
}

export default App;

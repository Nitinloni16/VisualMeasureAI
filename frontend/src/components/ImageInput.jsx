import React, { useState } from 'react';

const ImageInput = ({ onAnalyze, isLoading }) => {
    const [urls, setUrls] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const urlList = urls.split('\n').map(u => u.trim()).filter(u => u);
        if (urlList.length > 0) {
            onAnalyze(urlList);
        }
    };

    return (
        <div className="input-section">
            <h2>Product Images</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={urls}
                    onChange={(e) => setUrls(e.target.value)}
                    placeholder="Enter image URLs (one per line)..."
                    rows={5}
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading || !urls.trim()}>
                    {isLoading ? 'Analyzing...' : 'Analyze Product'}
                </button>
            </form>
        </div>
    );
};

export default ImageInput;

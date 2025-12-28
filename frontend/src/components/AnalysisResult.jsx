import React from 'react';

const DimensionBar = ({ label, value, leftLabel, rightLabel }) => {
    // Map -5 to +5 range to 0 to 100%
    // -5 => 0%, 0 => 50%, +5 => 100%
    const percentage = ((value + 5) / 10) * 100;

    return (
        <div className="dimension-row">
            <div className="dimension-header">
                <span>{leftLabel}</span>
                <span className="dimension-title">{label} ({value})</span>
                <span>{rightLabel}</span>
            </div>
            <div className="progress-bar-container">
                <div
                    className="progress-bar-fill"
                    style={{ width: `${percentage}%` }}
                ></div>
                <div className="center-marker"></div>
            </div>
        </div>
    );
};

const AnalysisResult = ({ result }) => {
    if (!result) return null;

    const { continuous_dimensions, discrete_attributes, metadata } = result;

    return (
        <div className="results-section">
            <h2>Analysis Results</h2>

            <div className="result-card">
                <h3>Continuous Dimensions</h3>
                <DimensionBar
                    label="Gender Expression"
                    value={continuous_dimensions.gender_expression}
                    leftLabel="Masculine"
                    rightLabel="Feminine"
                />
                <DimensionBar
                    label="Visual Weight"
                    value={continuous_dimensions.visual_weight}
                    leftLabel="Sleek/Light"
                    rightLabel="Bold/Heavy"
                />
                <DimensionBar
                    label="Embellishment"
                    value={continuous_dimensions.embellishment}
                    leftLabel="Simple"
                    rightLabel="Ornate"
                />
                <DimensionBar
                    label="Unconventionality"
                    value={continuous_dimensions.unconventionality}
                    leftLabel="Classic"
                    rightLabel="Avant-Garde"
                />
                <DimensionBar
                    label="Formality"
                    value={continuous_dimensions.formality}
                    leftLabel="Casual"
                    rightLabel="Formal"
                />
            </div>

            <div className="result-card">
                <h3>Discrete Attributes</h3>
                <div className="tags">
                    <span className={discrete_attributes.has_wirecore ? "tag active" : "tag"}>
                        Wirecore: {discrete_attributes.has_wirecore ? 'Yes' : 'No'}
                    </span>
                    <span className={discrete_attributes.is_transparent ? "tag active" : "tag"}>
                        Transparent: {discrete_attributes.is_transparent ? 'Yes' : 'No'}
                    </span>
                    <span className={discrete_attributes.looks_like_kids_product ? "tag active" : "tag"}>
                        Kids Product: {discrete_attributes.looks_like_kids_product ? 'Yes' : 'No'}
                    </span>
                </div>
                <p><strong>Frame Shape:</strong> {discrete_attributes.frame_shape}</p>
                <p><strong>Dominant Colors:</strong> {discrete_attributes.dominant_colors.join(', ')}</p>
                {discrete_attributes.texture_pattern && (
                    <p><strong>Texture/Pattern:</strong> {discrete_attributes.texture_pattern}</p>
                )}
            </div>

            <div className="result-card metadata">
                <h3>Visual Metadata</h3>
                <div className="metadata-grid">
                    <div className="meta-item">
                        <span className="meta-label">AI Confidence</span>
                        <span className="meta-value score">
                            {Math.round(metadata.confidence_score * 100)}%
                        </span>
                    </div>

                </div>
                {metadata.is_occluded_or_ambiguous && (
                    <div className="warning-banner">
                        ⚠️ High Ambiguity / Occlusion Detected
                    </div>
                )}
            </div>

            <div className="result-card json-export">
                <h3>Raw JSON</h3>
                <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
        </div>
    );
};

export default AnalysisResult;

import React from 'react';

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-logo">
                    <span role="img" aria-label="logo">📏</span> VisualMeasure AI
                </div>
                <div className="navbar-links">
                    {/* Future links can go here */}
                    <span className="navbar-tag">v1.0</span>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;

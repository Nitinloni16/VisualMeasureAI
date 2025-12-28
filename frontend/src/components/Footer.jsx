import React from 'react';

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-container">
                <p>&copy; {new Date().getFullYear()} Visual Product Measurement System.</p>
                <p className="footer-credits">
                    Designed & Built with ❤️ by <a href="#" target="_blank" rel="noopener noreferrer">Nitinkumar Loni</a>
                </p>
            </div>
        </footer>
    );
}

export default Footer;

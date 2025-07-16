import React from 'react';

const Spinner: React.FC<{ size?: number }> = ({ size = 32 }) => (
  <div
    role="status"
    aria-label="Cargando"
    style={{
      display: 'inline-block',
      width: size,
      height: size,
      border: '4px solid #e0e0e0',
      borderTop: '4px solid #2196F3',
      borderRadius: '50%',
      animation: 'spin 1s linear infinite',
    }}
  />
);

export default Spinner;

// Add keyframes for spin in global CSS (index.css):
// @keyframes spin { 100% { transform: rotate(360deg); } } 
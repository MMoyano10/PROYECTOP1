import React from 'react';

interface OnboardingModalProps {
  onClose: () => void;
}

const OnboardingModal: React.FC<OnboardingModalProps> = ({ onClose }) => (
  <div
    role="dialog"
    aria-modal="true"
    tabIndex={-1}
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      animation: 'fadeIn 0.4s',
    }}
  >
    <div className="card" style={{ maxWidth: 420, width: '90%', padding: 32, textAlign: 'center', position: 'relative' }}>
      <h2 style={{ marginBottom: 16 }}>¡Bienvenido/a!</h2>
      <p style={{ marginBottom: 16 }}>
        Explora la librería de imágenes.<br />
        Usa las categorías y tags para filtrar.<br />
        Haz clic en una imagen para ver detalles.<br />
        {` `}
        {` `}
        <strong>¿Eres admin?</strong> Usa el panel para gestionar usuarios, categorías, tags y assets.
      </p>
      <button className="button" onClick={onClose} autoFocus style={{ marginTop: 16 }}>
        ¡Entendido!
      </button>
    </div>
    <style>{`
      @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    `}</style>
  </div>
);

export default OnboardingModal; 
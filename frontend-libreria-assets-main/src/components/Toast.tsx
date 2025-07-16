import React, { useEffect } from 'react';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'info';
  onClose: () => void;
}

const bgColor = {
  success: '#4CAF50',
  error: '#F44336',
  info: '#2196F3',
};

const Toast: React.FC<ToastProps> = ({ message, type = 'info', onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      role="status"
      aria-live="polite"
      className="card"
      style={{
        position: 'fixed',
        bottom: 32,
        left: '50%',
        transform: 'translateX(-50%)',
        minWidth: 240,
        maxWidth: '90vw',
        background: bgColor[type],
        color: '#fff',
        boxShadow: '0 6px 18px rgba(33,150,243,0.15)',
        zIndex: 3000,
        animation: 'fadeInUp 0.4s',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 16,
        fontWeight: 500,
      }}
    >
      <span>{message}</span>
      <button
        className="button"
        style={{ background: 'rgba(0,0,0,0.15)', color: '#fff', fontSize: 18, padding: '0 10px' }}
        onClick={onClose}
        aria-label="Cerrar notificación"
      >
        ×
      </button>
      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(40px) translateX(-50%); }
          to { opacity: 1; transform: translateY(0) translateX(-50%); }
        }
      `}</style>
    </div>
  );
};

export default Toast; 
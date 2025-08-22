import React from 'react';

const Footer: React.FC = () => (
  <footer
    style={{
      width: '100%',
      background: 'var(--color-bg-paper, #fff)',
      color: 'var(--color-text-secondary, #757575)',
      borderTop: '1px solid var(--color-border, #e0e0e0)',
      padding: '16px 0',
      textAlign: 'center',
      fontSize: '1rem',
      marginTop: 32,
    }}
  >
    <span>
      &copy; {new Date().getFullYear()} Mi Librería de Imágenes &mdash;
      <a
        href="/privacy"
        style={{ color: 'var(--color-primary, #2196F3)', margin: '0 8px' }}
        target="_blank"
        rel="noopener noreferrer"
      >
        Política de Privacidad
      </a>
      |
      <a
        href="mailto:soporte@tusitio.com"
        style={{ color: 'var(--color-primary, #2196F3)', margin: '0 8px' }}
      >
        Soporte
      </a>
    </span>
  </footer>
);

export default Footer; 
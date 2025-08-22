import React from 'react';
import { theme } from '../theme';

interface NavbarProps {
  userName?: string;
  isAdmin?: boolean;
  onLogout: () => void;
  onToggleDarkMode: () => void;
  darkMode: boolean;
  children?: React.ReactNode;
}

const Navbar: React.FC<NavbarProps> = ({ userName, isAdmin, onLogout, onToggleDarkMode, darkMode, children }) => {
  return (
    <nav
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 100,
        background: theme.colors.background.paper,
        borderBottom: `1px solid ${theme.colors.border}`,
        boxShadow: theme.shadows.small,
        padding: theme.spacing.sm,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        minHeight: 56,
      }}
      aria-label="Main navigation"
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: theme.spacing.md }}>
        <span style={{ fontWeight: 700, fontSize: '1.2rem', color: theme.colors.primary }}>
          {isAdmin ? 'Admin' : 'Librería'}
        </span>
        {userName && (
          <span style={{ color: theme.colors.text.secondary, fontSize: '1rem' }}>
            Hola, <strong>{userName}</strong>
          </span>
        )}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: theme.spacing.md }}>
        {children}
        <button
          aria-label={darkMode ? 'Activar modo claro' : 'Activar modo oscuro'}
          onClick={onToggleDarkMode}
          style={{
            background: 'none',
            border: 'none',
            color: theme.colors.primary,
            fontSize: '1.2rem',
            cursor: 'pointer',
            marginRight: theme.spacing.sm,
          }}
        >
          {darkMode ? '🌙' : '☀️'}
        </button>
        <button
          onClick={onLogout}
          style={{
            background: 'transparent',
            border: `1px solid ${theme.colors.error}`,
            color: theme.colors.error,
            padding: '6px 12px',
            borderRadius: 4,
            cursor: 'pointer',
            fontWeight: 500,
          }}
        >
          Cerrar sesión
        </button>
      </div>
    </nav>
  );
};

export default Navbar; 
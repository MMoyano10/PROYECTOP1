import React from 'react';
import { theme } from '../theme';

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, title }) => {
  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: theme.colors.background.main,
      padding: theme.spacing.md,
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        backgroundColor: theme.colors.background.paper,
        borderRadius: theme.borderRadius.large,
        boxShadow: theme.shadows.medium,
        padding: theme.spacing.xl,
      }}>
        {title && (
          <h1 style={{
            color: theme.colors.text.primary,
            marginBottom: theme.spacing.lg,
            fontSize: '2rem',
            fontWeight: 'bold',
            borderBottom: `2px solid ${theme.colors.primary}`,
            paddingBottom: theme.spacing.sm,
          }}>
            {title}
          </h1>
        )}
        {children}
      </div>
    </div>
  );
};

export default Layout; 
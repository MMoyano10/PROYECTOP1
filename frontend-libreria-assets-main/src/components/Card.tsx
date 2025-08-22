import React from 'react';
import { theme } from '../theme';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  style?: React.CSSProperties;
  className?: string;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({ children, title, style, className, onClick }) => {
  return (
    <div
      className={`card${className ? ' ' + className : ''}`}
      style={style}
      onClick={onClick}
    >
      {title && (
        <h2
          style={{
            color: theme.colors.text.primary,
            fontSize: '1.25rem',
            marginBottom: theme.spacing.md,
            paddingBottom: theme.spacing.sm,
            borderBottom: `1px solid ${theme.colors.border}`,
          }}
        >
          {title}
        </h2>
      )}
      {children}
    </div>
  );
};

export default Card; 
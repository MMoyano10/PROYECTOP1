import React from 'react';
import { theme } from '../theme';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  size?: 'small' | 'medium' | 'large';
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  style,
  ...props
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return {
          backgroundColor: theme.colors.primary,
          color: theme.colors.text.light,
        };
      case 'secondary':
        return {
          backgroundColor: theme.colors.secondary,
          color: theme.colors.text.light,
        };
      case 'success':
        return {
          backgroundColor: theme.colors.success,
          color: theme.colors.text.light,
        };
      case 'warning':
        return {
          backgroundColor: theme.colors.warning,
          color: theme.colors.text.light,
        };
      case 'error':
        return {
          backgroundColor: theme.colors.error,
          color: theme.colors.text.light,
        };
      default:
        return {};
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          padding: `${theme.spacing.xs} ${theme.spacing.sm}`,
          fontSize: '0.875rem',
        };
      case 'large':
        return {
          padding: `${theme.spacing.md} ${theme.spacing.lg}`,
          fontSize: '1.125rem',
        };
      default:
        return {
          padding: `${theme.spacing.sm} ${theme.spacing.md}`,
          fontSize: '1rem',
        };
    }
  };

  return (
    <button
      style={{
        ...getVariantStyles(),
        ...getSizeStyles(),
        border: 'none',
        borderRadius: theme.borderRadius.medium,
        cursor: 'pointer',
        fontWeight: 600,
        transition: 'all 0.2s ease-in-out',
        boxShadow: theme.shadows.small,
        ...style,
      }}
      onMouseOver={(e) => {
        e.currentTarget.style.opacity = '0.9';
        e.currentTarget.style.transform = 'translateY(-1px)';
      }}
      onMouseOut={(e) => {
        e.currentTarget.style.opacity = '1';
        e.currentTarget.style.transform = 'translateY(0)';
      }}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button; 
export const theme = {
  mode: 'light', // 'light' or 'dark'
  colors: {
    primary: '#2196F3',
    primaryHover: '#1976D2',
    primaryActive: '#1565C0',
    secondary: '#607D8B',
    secondaryHover: '#455A64',
    secondaryActive: '#263238',
    accent: '#FF4081',
    accentHover: '#F50057',
    accentActive: '#C51162',
    success: '#4CAF50',
    successHover: '#388E3C',
    warning: '#FFC107',
    warningHover: '#FFA000',
    error: '#F44336',
    errorHover: '#C62828',
    info: '#29B6F6',
    infoHover: '#0288D1',
    background: {
      main: '#F5F5F5',
      paper: '#FFFFFF',
      dark: '#212121',
      light: '#FFFFFF',
      darkPaper: '#23272f',
      gradient: 'linear-gradient(135deg, #2196F3 0%, #21CBF3 100%)',
    },
    text: {
      primary: '#212121',
      secondary: '#757575',
      light: '#FFFFFF',
      dark: '#E0E0E0',
      accent: '#FF4081',
      success: '#4CAF50',
      warning: '#FFC107',
      error: '#F44336',
      info: '#29B6F6',
    },
    border: '#E0E0E0',
    darkBorder: '#333',
  },
  shadows: {
    small: '0 2px 4px rgba(0,0,0,0.1)',
    medium: '0 4px 8px rgba(0,0,0,0.1)',
    large: '0 8px 16px rgba(0,0,0,0.1)',
    hover: '0 6px 18px rgba(33,150,243,0.15)',
  },
  borderRadius: {
    small: '4px',
    medium: '8px',
    large: '16px',
    pill: '999px',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
};

export const getTheme = (mode: 'light' | 'dark') => {
  if (mode === 'dark') {
    return {
      ...theme,
      mode: 'dark',
      colors: {
        ...theme.colors,
        background: {
          ...theme.colors.background,
          main: '#181A20',
          paper: '#23272f',
        },
        text: {
          ...theme.colors.text,
          primary: '#E0E0E0',
          secondary: '#B0B0B0',
          light: '#FFFFFF',
        },
        border: '#333',
      },
    };
  }
  return { ...theme, mode: 'light' };
}; 
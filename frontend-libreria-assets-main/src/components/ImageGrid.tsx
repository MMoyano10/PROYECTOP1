// ImageGrid.tsx
import React from 'react';
import { theme } from '../theme';
import Card from './Card';

interface ImageGridProps {
  images: Array<{
    id_asset: number;
    nombre?: string;
    url_imagen?: string;
    filename?: string;
    ruta?: string;
  }>;
  onImageClick?: (image: any) => void;
  loading?: boolean;
}

const ImageGrid: React.FC<ImageGridProps> = ({ images, onImageClick, loading }) => {
  if (loading) {
    return (
      <div className="grid">
        {Array.from({ length: 8 }).map((_, i) => (
          <div className="card skeleton" key={i} style={{ height: 260 }} />
        ))}
      </div>
    );
  }
  return (
    <div className="grid">
      {images.map((image) => {
        // Usar los campos reales del backend, con fallback para compatibilidad
        const imgSrc = image.url_imagen || image.ruta || '';
        const imgName = image.nombre || image.filename || '';
        return (
          <Card
            key={image.id_asset}
            style={{
              cursor: onImageClick ? 'pointer' : 'default',
              transition: 'transform 0.2s ease-in-out',
            }}
            className={onImageClick ? 'hover-lift' : ''}
            onClick={() => onImageClick?.(image)}
          >
            <img
              src={imgSrc}
              alt={imgName}
              style={{
                width: '100%',
                height: '200px',
                objectFit: 'cover',
                borderRadius: theme.borderRadius.small,
                marginBottom: theme.spacing.sm,
              }}
            />
            <h3 style={{
              color: theme.colors.text.primary,
              fontSize: '1rem',
              margin: 0,
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}>
              {imgName}
            </h3>
          </Card>
        );
      })}
    </div>
  );
};

export default ImageGrid;

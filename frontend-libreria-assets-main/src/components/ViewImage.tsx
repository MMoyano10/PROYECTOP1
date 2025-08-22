import React, { useEffect } from 'react';
import { Socket } from 'socket.io-client';
import { theme } from '../theme';

interface ViewImageProps {
  image: {
    id_asset: number;
    nombre?: string;
    url_imagen?: string;
    filename?: string;
    ruta?: string;
  };
  socket: Socket;
  onClose: () => void;
  locked: boolean;
}

const ViewImage: React.FC<ViewImageProps> = ({ image, socket, onClose, locked }) => {
  useEffect(() => {
    if (!locked) {
      socket.emit('lock_asset', { asset_id: image.id_asset });
      return () => {
        socket.emit('unlock_asset', { asset_id: image.id_asset });
      };
    }
  }, [image.id_asset, locked, socket]);

  const imgSrc = image.url_imagen || image.ruta || '';
  const imgName = image.nombre || image.filename || '';

  return (
    <div className="modal" style={{ zIndex: 1000 }}>
      <div className="modal-content">
        <button onClick={onClose} style={{ float: 'right' }}>Cerrar</button>
        <img
          src={imgSrc}
          alt={imgName}
          style={{
            width: '100%',
            maxHeight: '60vh',
            objectFit: 'contain',
            borderRadius: theme.borderRadius.small,
            marginBottom: theme.spacing.sm,
          }}
        />
        <h2>{imgName}</h2>
        {locked && <div style={{ color: 'red' }}>Esta imagen está siendo vista por otro usuario.</div>}
      </div>
    </div>
  );
};

export default ViewImage;

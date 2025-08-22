import { useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

const SOCKET_URL = 'http://localhost:8000'; // Cambia si usas otro puerto

export function useSocket(onEvents: (socket: Socket) => void) {
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    const socket = io(SOCKET_URL, {
      path: '/socket.io',
      transports: ['websocket', 'polling'],
      withCredentials: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });
    // Debug de errores de conexión
    socket.on('connect_error', (err) => {
      console.error('Socket connect_error:', err?.message || err);
    });
    socket.on('error', (err) => {
      console.error('Socket error:', err);
    });

    socketRef.current = socket;
    onEvents(socket);
    return () => {
      socket.disconnect();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return socketRef;
}

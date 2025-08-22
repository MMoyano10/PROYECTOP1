// frontend-libreria-assets-main/src/components/LogList.tsx

import React, { useEffect, useState, useRef } from "react";
import { api } from "../api";
import Spinner from './Spinner';

interface Log {
  id_log: number;
  id_usuario: number | null;
  id_asset: number | null;
  id_categoria: number | null;
  id_tag: number | null;
  id_usuario_afectado: number | null;
  accion: string;
  valores_antes: string | null;
  valores_despues: string | null;
  entidad: string | null;
  fecha_registro: string;
}

export default function LogList(props: { currentUserId: number }) {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    // Asegurarnos de pasar siempre el header X-User-Id
    api
      .get<Log[]>("/logs/", {
        headers: {
          "X-User-Id": String(props.currentUserId),
        },
      })
      .then((res) => {
        if (Array.isArray(res.data)) {
          setLogs(res.data);
        } else {
          console.error("Respuesta inesperada de /api/logs/:", res.data);
          setError("La respuesta no es un arreglo de logs");
        }
      })
      .catch((err) => {
        console.error("Error al cargar logs:", err);
        setError("Error al cargar lista de logs");
      })
      .finally(() => {
        setLoading(false);
      });

    // WebSocket para logs en tiempo real
    const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const wsUrl = `${wsProtocol}://${window.location.hostname}:8000/ws/logs`;
    const ws = new window.WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const newLog: Log = JSON.parse(event.data);
        setLogs((prev) => [newLog, ...prev].slice(0, 100)); // Máximo 100 logs
      } catch {}
    };
    ws.onerror = () => {
      // Silenciar error de conexión si el backend no está listo
    };
    ws.onclose = () => {};

    return () => {
      ws.close();
    };
  }, [props.currentUserId]);

  const formatJsonValues = (jsonString: string | null) => {
    if (!jsonString) return "-";
    try {
      const parsed = JSON.parse(jsonString);
      return (
        <pre style={{ 
          fontSize: '12px', 
          margin: 0, 
          whiteSpace: 'pre-wrap',
          maxWidth: '200px',
          overflow: 'hidden',
          textOverflow: 'ellipsis'
        }}>
          {JSON.stringify(parsed, null, 2)}
        </pre>
      );
    } catch {
      return jsonString;
    }
  };

  const getEntityDisplay = (log: Log) => {
    if (log.entidad) {
      return log.entidad.charAt(0).toUpperCase() + log.entidad.slice(1);
    }
    if (log.id_asset) return "Asset";
    if (log.id_categoria) return "Categoría";
    if (log.id_tag) return "Tag";
    if (log.id_usuario_afectado) return "Usuario";
    return "-";
  };

  const getEntityId = (log: Log) => {
    if (log.id_asset) return log.id_asset;
    if (log.id_categoria) return log.id_categoria;
    if (log.id_tag) return log.id_tag;
    if (log.id_usuario_afectado) return log.id_usuario_afectado;
    return "-";
  };

  if (loading) return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 80 }}><Spinner size={32} /></div>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!logs.length) return <p>No hay registros en el log.</p>;

  return (
    <div>
      <h3>Registros de Log Detallados</h3>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: '14px' }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>ID Log</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>Usuario</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>Entidad</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>ID Entidad</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>Acción</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>Valores Antes</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>Valores Después</th>
              <th style={{ border: "1px solid #ccc", padding: 8, backgroundColor: '#f5f5f5' }}>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((l) => (
              <tr key={l.id_log}>
                <td style={{ border: "1px solid #ccc", padding: 8 }}>
                  {l.id_log}
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8 }}>
                  {l.id_usuario || "-"}
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8 }}>
                  {getEntityDisplay(l)}
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8 }}>
                  {getEntityId(l)}
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8 }}>
                  <span style={{ 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    fontSize: '12px',
                    backgroundColor: l.accion.includes('create') ? '#d4edda' : 
                                   l.accion.includes('update') ? '#fff3cd' : 
                                   l.accion.includes('delete') ? '#f8d7da' : '#e2e3e5',
                    color: l.accion.includes('create') ? '#155724' : 
                          l.accion.includes('update') ? '#856404' : 
                          l.accion.includes('delete') ? '#721c24' : '#383d41'
                  }}>
                    {l.accion}
                  </span>
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8, maxWidth: '200px' }}>
                  {formatJsonValues(l.valores_antes)}
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8, maxWidth: '200px' }}>
                  {formatJsonValues(l.valores_despues)}
                </td>
                <td style={{ border: "1px solid #ccc", padding: 8 }}>
                  {new Date(l.fecha_registro).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

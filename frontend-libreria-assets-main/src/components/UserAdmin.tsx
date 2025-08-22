import React, { useEffect, useState } from "react";
import { api } from "../api";
import Spinner from './Spinner';
import Button from './Button';
import Card from './Card';
import { getTheme } from '../theme';

interface User {
  id_usuario: number;
  nombre: string;
  email: string;
  is_admin: boolean;
}

interface UserAdminProps {
  currentUserId: number;
  showToast?: (msg: string, type?: 'success' | 'error' | 'info') => void;
}

export default function UserAdmin(props: UserAdminProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    password: '',
    is_admin: false,
  });

  const theme = getTheme("light");

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await api.get<User[]>("/users/", {
        headers: {
          "X-User-Id": String(props.currentUserId),
        },
      });
      
      if (Array.isArray(res.data)) {
        setUsers(res.data);
      } else {
        console.error("Respuesta inesperada de /api/users/:", res.data);
        setError("La respuesta no es un arreglo de usuarios");
      }
    } catch (err) {
      console.error("Error al cargar usuarios:", err);
      setError("Error al cargar lista de usuarios");
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setSelectedUser(null);
    setFormData({ nombre: '', email: '', password: '', is_admin: false });
    setError(null);
    setIsModalOpen(true);
  };

  const handleEdit = (user: User) => {
    setSelectedUser(user);
    setFormData({
      nombre: user.nombre,
      email: user.email,
      password: '', // No mostrar password actual
      is_admin: user.is_admin,
    });
    setError(null);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (id === props.currentUserId) {
      setError("No puedes eliminar tu propio usuario");
      if (props.showToast) props.showToast("No puedes eliminar tu propio usuario", 'error');
      return;
    }

    if (window.confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      try {
        await api.delete(`/users/${id}`, {
          headers: {
            "X-User-Id": String(props.currentUserId),
          },
        });
        fetchUsers();
        if (props.showToast) props.showToast('Usuario eliminado correctamente', 'success');
      } catch (err) {
        setError('Error al eliminar el usuario');
        if (props.showToast) props.showToast('Error al eliminar el usuario', 'error');
        console.error(err);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      if (selectedUser) {
        // Actualizar usuario
        const payload: any = {
          nombre: formData.nombre,
          email: formData.email,
          is_admin: formData.is_admin,
        };
        if (formData.password) {
          payload.password = formData.password;
        }
        
        await api.put(`/users/${selectedUser.id_usuario}`, payload, {
          headers: {
            "X-User-Id": String(props.currentUserId),
          },
        });
        if (props.showToast) props.showToast('Usuario actualizado correctamente', 'success');
      } else {
        // Crear usuario
        await api.post('/users/', {
          nombre: formData.nombre,
          email: formData.email,
          password: formData.password,
          is_admin: formData.is_admin,
        }, {
          headers: {
            "X-User-Id": String(props.currentUserId),
          },
        });
        if (props.showToast) props.showToast('Usuario creado correctamente', 'success');
      }
      setIsModalOpen(false);
      fetchUsers();
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Error al guardar el usuario';
      setError(msg);
      if (props.showToast) props.showToast(msg, 'error');
      console.error(err);
    }
  };

  if (loading) return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 80 }}><Spinner size={32} /></div>;
  if (error && !isModalOpen) return <p style={{ color: "red" }}>{error}</p>;
  if (!users.length && !isModalOpen) return <p>No hay usuarios registrados.</p>;

  return (
    <div>
      <div style={{ marginBottom: theme.spacing.lg }}>
        <Button onClick={handleCreate} variant="primary">
          Crear Nuevo Usuario
        </Button>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: theme.spacing.lg,
      }}>
        {users.map((user) => (
          <Card key={user.id_usuario}>
            <h3 style={{ marginBottom: theme.spacing.sm }}>{user.nombre}</h3>
            <p style={{ color: theme.colors.text.secondary, marginBottom: theme.spacing.sm }}>
              {user.email}
            </p>
            <p style={{ color: theme.colors.text.secondary, marginBottom: theme.spacing.md }}>
              {user.is_admin ? "👑 Administrador" : "👤 Usuario"}
            </p>
            <div style={{ display: 'flex', gap: theme.spacing.sm }}>
              <Button
                variant="secondary"
                size="small"
                onClick={() => handleEdit(user)}
              >
                Editar
              </Button>
              <Button
                variant="error"
                size="small"
                onClick={() => handleDelete(user.id_usuario)}
                disabled={user.id_usuario === props.currentUserId}
              >
                Eliminar
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Modal para crear/editar usuario */}
      {isModalOpen && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <Card style={{ width: '400px', maxWidth: '90%' }}>
            <h2 style={{ marginBottom: theme.spacing.lg }}>
              {selectedUser ? 'Editar Usuario' : 'Crear Usuario'}
            </h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
              <div>
                <label htmlFor="user-nombre" style={{ fontWeight: 500 }}>
                  Nombre
                </label>
                <input
                  id="user-nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                  aria-required="true"
                />
              </div>
              <div>
                <label htmlFor="user-email" style={{ fontWeight: 500 }}>
                  Email
                </label>
                <input
                  id="user-email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  aria-required="true"
                />
              </div>
              <div>
                <label htmlFor="user-password" style={{ fontWeight: 500 }}>
                  Contraseña {selectedUser && '(dejar vacío para no cambiar)'}
                </label>
                <input
                  id="user-password"
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required={!selectedUser}
                  aria-required={!selectedUser}
                />
              </div>
              <div>
                <label style={{ fontWeight: 500, display: 'flex', alignItems: 'center', gap: theme.spacing.sm }}>
                  <input
                    type="checkbox"
                    checked={formData.is_admin}
                    onChange={(e) => setFormData({ ...formData, is_admin: e.target.checked })}
                  />
                  Es administrador
                </label>
              </div>
              {error && (
                <div style={{ color: theme.colors.error, marginBottom: theme.spacing.sm }}>
                  {error}
                </div>
              )}
              <div style={{ display: 'flex', gap: theme.spacing.sm, justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  className="button"
                  onClick={() => { setIsModalOpen(false); setError(null); }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="button"
                  disabled={!formData.nombre || !formData.email || (!selectedUser && !formData.password)}
                >
                  {selectedUser ? 'Guardar' : 'Crear'}
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}

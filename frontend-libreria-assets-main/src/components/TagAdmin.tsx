import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { theme } from '../theme';
import Layout from './Layout';
import Card from './Card';
import Button from './Button';

interface Tag {
  id_tag: number;
  nombre: string;
}

interface TagAdminProps {
  showToast?: (msg: string, type?: 'success' | 'error' | 'info') => void;
}

const TagAdmin: React.FC<TagAdminProps> = ({ showToast }) => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedTag, setSelectedTag] = useState<Tag | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTags();
  }, []);

  const fetchTags = async () => {
    try {
      const response = await api.get('/tags/');
      setTags(response.data);
    } catch (err) {
      setError('Error al cargar los tags');
      if (showToast) showToast('Error al cargar los tags', 'error');
      console.error(err);
    }
  };

  const handleCreate = () => {
    setSelectedTag(null);
    setFormData({ nombre: '' });
    setError('');
    setIsModalOpen(true);
  };

  const handleEdit = (tag: Tag) => {
    setSelectedTag(tag);
    setFormData({
      nombre: tag.nombre,
    });
    setError('');
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este tag?')) {
      try {
        await api.delete(`/tags/${id}`);
        fetchTags();
        if (showToast) showToast('Tag eliminado correctamente', 'success');
      } catch (err) {
        setError('Error al eliminar el tag');
        if (showToast) showToast('Error al eliminar el tag', 'error');
        console.error(err);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const payload = {
        nombre: formData.nombre || '',
      };
      if (selectedTag) {
        await api.put(`/tags/${selectedTag.id_tag}`, payload);
        if (showToast) showToast('Tag actualizado correctamente', 'success');
      } else {
        await api.post('/tags/', payload);
        if (showToast) showToast('Tag creado correctamente', 'success');
      }
      setIsModalOpen(false);
      fetchTags();
    } catch (err: any) {
      // Mostrar mensaje específico del backend si existe
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Error al guardar el tag';
      setError(msg);
      if (showToast) showToast(msg, 'error');
      console.error(err);
    }
  };

  return (
    <Layout title="Administración de Tags">
      <div style={{ marginBottom: theme.spacing.lg }}>
        <Button onClick={handleCreate} variant="primary">
          Crear Nuevo Tag
        </Button>
      </div>

      {error && (
        <div style={{ color: theme.colors.error, marginBottom: theme.spacing.md }}>
          {error}
        </div>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
        gap: theme.spacing.lg,
      }}>
        {tags.map((tag) => (
          <Card key={tag.id_tag}>
            <h3 style={{ marginBottom: theme.spacing.md }}>{tag.nombre}</h3>
            <div style={{ display: 'flex', gap: theme.spacing.sm }}>
              <Button
                variant="secondary"
                size="small"
                onClick={() => handleEdit(tag)}
              >
                Editar
              </Button>
              <Button
                variant="error"
                size="small"
                onClick={() => handleDelete(tag.id_tag)}
              >
                Eliminar
              </Button>
            </div>
          </Card>
        ))}
      </div>

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
              {selectedTag ? 'Editar Tag' : 'Crear Tag'}
            </h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
              <div>
                <label htmlFor="tag-nombre" style={{ fontWeight: 500 }}>
                  Nombre
                </label>
                <input
                  id="tag-nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                  aria-required="true"
                />
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
                  onClick={() => { setIsModalOpen(false); setError(''); }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="button"
                  disabled={!formData.nombre}
                >
                  {selectedTag ? 'Guardar' : 'Crear'}
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </Layout>
  );
};

export default TagAdmin;

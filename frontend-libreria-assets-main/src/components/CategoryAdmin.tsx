import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { theme } from '../theme';
import Layout from './Layout';
import Card from './Card';
import Button from './Button';

interface Category {
  id_categoria: number;
  nombre: string;
  descripcion: string;
}

interface CategoryAdminProps {
  showToast?: (msg: string, type?: 'success' | 'error' | 'info') => void;
}

const CategoryAdmin: React.FC<CategoryAdminProps> = ({ showToast }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await api.get('/categories/');
      setCategories(response.data);
    } catch (err) {
      setError('Error al cargar las categorías');
      if (showToast) showToast('Error al cargar las categorías', 'error');
      console.error(err);
    }
  };
  

  const handleCreate = () => {
    setSelectedCategory(null);
    setFormData({ nombre: '', descripcion: '' });
    setError('');
    setIsModalOpen(true);
  };

  const handleEdit = (category: Category) => {
    setSelectedCategory(category);
    setFormData({
      nombre: category.nombre,
      descripcion: category.descripcion,
    });
    setError('');
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar esta categoría?')) {
      try {
        await api.delete(`/categories/${id}`);
        fetchCategories();
        if (showToast) showToast('Categoría eliminada correctamente', 'success');
      } catch (err) {
        setError('Error al eliminar la categoría');
        if (showToast) showToast('Error al eliminar la categoría', 'error');
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
        descripcion: formData.descripcion || '',
      };
      if (selectedCategory) {
        await api.put(`/categories/${selectedCategory.id_categoria}`, payload);
        if (showToast) showToast('Categoría actualizada correctamente', 'success');
      } else {
        await api.post('/categories/', payload);
        if (showToast) showToast('Categoría creada correctamente', 'success');
      }
      setIsModalOpen(false);
      fetchCategories();
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Error al guardar la categoría';
      setError(msg);
      if (showToast) showToast(msg, 'error');
      console.error(err);
    }
  };

  return (
    <Layout title="Administración de Categorías">
      <div style={{ marginBottom: theme.spacing.lg }}>
        <Button onClick={handleCreate} variant="primary">
          Crear Nueva Categoría
        </Button>
      </div>

      {error && (
        <div style={{ color: theme.colors.error, marginBottom: theme.spacing.md }}>
          {error}
        </div>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: theme.spacing.lg,
      }}>
        {categories.map((category) => (
          <Card key={category.id_categoria}>
            <h3 style={{ marginBottom: theme.spacing.sm }}>{category.nombre}</h3>
            <p style={{ color: theme.colors.text.secondary, marginBottom: theme.spacing.md }}>
              {category.descripcion}
            </p>
            <div style={{ display: 'flex', gap: theme.spacing.sm }}>
              <Button
                variant="secondary"
                size="small"
                onClick={() => handleEdit(category)}
              >
                Editar
              </Button>
              <Button
                variant="error"
                size="small"
                onClick={() => handleDelete(category.id_categoria)}
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
              {selectedCategory ? 'Editar Categoría' : 'Crear Categoría'}
            </h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
              <div>
                <label htmlFor="cat-nombre" style={{ fontWeight: 500 }}>
                  Nombre
                </label>
                <input
                  id="cat-nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                  aria-required="true"
                />
              </div>
              <div>
                <label htmlFor="cat-desc" style={{ fontWeight: 500 }}>
                  Descripción
                </label>
                <textarea
                  id="cat-desc"
                  value={formData.descripcion}
                  onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                  required
                  aria-required="true"
                  style={{ minHeight: '100px', resize: 'vertical' }}
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
                  disabled={!formData.nombre || !formData.descripcion}
                >
                  {selectedCategory ? 'Guardar' : 'Crear'}
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </Layout>
  );
};

export default CategoryAdmin;

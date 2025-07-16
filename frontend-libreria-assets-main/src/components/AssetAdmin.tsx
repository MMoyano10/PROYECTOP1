import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { theme } from '../theme';
import Layout from './Layout';
import Card from './Card';
import Button from './Button';

interface Asset {
  id_asset: number;
  nombre: string;
  descripcion: string;
  url_imagen: string;
  id_categoria: number;
  tags?: Tag[]; // Assuming Asset model has a 'tags' field
}

interface Category {
  id_categoria: number;
  nombre: string;
}

interface Tag {
  id_tag: number;
  nombre: string;
}

interface AssetAdminProps {
  showToast?: (msg: string, type?: 'success' | 'error' | 'info') => void;
}

const AssetAdmin: React.FC<AssetAdminProps> = ({ showToast }) => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    url_imagen: '',
    id_categoria: '',
  });
  const [error, setError] = useState('');
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedTags, setSelectedTags] = useState<number[]>([]);

  useEffect(() => {
    fetchAssets();
    fetchCategories();
    fetchTags();
  }, []);

  const fetchAssets = async () => {
    try {
      const response = await api.get('/assets/');
      setAssets(response.data);
    } catch (err) {
      setError('Error al cargar los assets');
      if (showToast) showToast('Error al cargar los assets', 'error');
      console.error(err);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/categories/');
      setCategories(response.data);
    } catch (err) {
      setError('Error al cargar las categorías');
      console.error(err);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await api.get('/tags/');
      setTags(response.data);
    } catch (err) {
      console.error('Error al cargar los tags', err);
    }
  };

  const handleCreate = () => {
    setSelectedAsset(null);
    setFormData({ nombre: '', descripcion: '', url_imagen: '', id_categoria: '' });
    setSelectedTags([]);
    setError('');
    setIsModalOpen(true);
  };

  const handleEdit = (asset: Asset) => {
    // Extraer solo el nombre del archivo de la ruta url_imagen
    let imagenNombre = '';
    if (asset.url_imagen) {
      const partes = asset.url_imagen.split('/');
      imagenNombre = partes[partes.length - 1];
    }
    setSelectedAsset(asset);
    setFormData({
      nombre: asset.nombre,
      descripcion: asset.descripcion,
      url_imagen: imagenNombre, // solo el nombre para el select
      id_categoria: asset.id_categoria.toString(),
    });
    setSelectedTags(asset.tags ? asset.tags.map((t: Tag) => t.id_tag) : []);
    setError('');
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este asset?')) {
      try {
        await api.delete(`/assets/${id}`);
        fetchAssets();
        if (showToast) showToast('Asset eliminado correctamente', 'success');
      } catch (err) {
        setError('Error al eliminar el asset');
        if (showToast) showToast('Error al eliminar el asset', 'error');
        console.error(err);
      }
    }
  };

  const handleTagChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, option => Number(option.value));
    setSelectedTags(selected);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      // Construir la ruta completa para url_imagen
      const urlImagenCompleta = formData.url_imagen ? `/images/${formData.url_imagen}` : '';
      const payload = {
        nombre: formData.nombre || '',
        descripcion: formData.descripcion || '',
        url_imagen: urlImagenCompleta,
        id_categoria: parseInt(formData.id_categoria),
        tags: selectedTags, // Se enviará al backend si está soportado
      };
      if (selectedAsset) {
        await api.put(`/assets/${selectedAsset.id_asset}`, payload);
        if (showToast) showToast('Asset actualizado correctamente', 'success');
      } else {
        await api.post('/assets/', payload);
        if (showToast) showToast('Asset creado correctamente', 'success');
      }
      setIsModalOpen(false);
      fetchAssets();
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Error al guardar el asset';
      setError(msg);
      if (showToast) showToast(msg, 'error');
      console.error(err);
    }
  };

  // Lista de imágenes extraída de images.txt
  const imageOptions = [
    "bebida1.jpg","bebida10.jpg","bebida2.jpg","bebida3.jpg","bebida3.png","bebida4.jpg","bebida5.jpg","bebida6.jpg","bebida7.jpg","bebida8.jpg","bebida9.jpg","bosque1.jpg","bosque10.jpg","bosque2.jpg","bosque3.jpg","bosque4.jpg","bosque5.jpg","bosque6.jpg","bosque7.jpg","bosque8.jpg","bosque9.jpg","calle1.jpg","calle10.jpg","calle2.jpg","calle3.jpg","calle4.jpg","calle5.jpg","calle7.jpg","calles6.jpg","calles8.jpg","calles9.jpg","computadora1.jpg","computadora10.jpg","computadora2.jpg","computadora3.jpg","computadora4.jpg","computadora5.jpg","computadora6.jpg","computadora7.jpg","computadora8.jpg","computadora9.jpg","edificio1.jpg","edificio10.jpg","edificio2.jpg","edificio3.jpg","edificio4.jpg","edificio5.jpg","edificio6.jpg","edificio7.jpg","edificio8.jpg","edificio9.jpg","escultura1.jpg","escultura10.jpg","escultura2.jpg","escultura3.jpg","escultura4.jpg","escultura5.jpg","escultura6.jpg","escultura7.jpg","escultura8.jpg","escultura9.jpg","fruta1.jpg","fruta10.jpg","fruta2.jpg","fruta3.jpg","fruta4.jpg","fruta5.jpg","fruta6.jpg","fruta7.jpg","fruta8.jpg","fruta9.jpg","gato1.jpg","gato10.jpg","gato2.jpg","gato3.jpg","gato4.jpg","gato5.jpg","gato6.jpg","gato7.jpg","gato8.jpg","gato9.jpg","graffiti1.jpg","graffiti10.jpg","graffiti2.jpg","graffiti3.jpg","graffiti4.jpg","graffiti5.jpg","graffiti6.jpg","graffiti7.jpg","graffiti8.jpg","graffiti9.jpg","montana1.jpg","montana10.jpg","montana2.jpg","montana3.jpg","montana4.jpg","montana5.jpg","montana6.jpg","montana7.jpg","montana8.jpg","montana9.jpg","pajaro1.jpg","pajaro10.jpg","pajaro2.jpg","pajaro3.jpg","pajaro4.jpg","pajaro5.jpg","pajaro6.jpg","pajaro7.jpg","pajaro8.jpg","pajaro9.jpg","perro1.jpg","perro10.jpg","perro2.jpg","perro3.jpg","perro4.jpg","perro5.jpg","perro6.jpg","perro7.jpg","perro8.jpg","perro9.jpg","pintura1.jpg","pintura10.jpg","pintura2.jpg","pintura3.jpg","pintura4.jpg","pintura5.jpg","pintura6.jpg","pintura7.jpg","pintura8.jpg","pintura9.jpg","postre1.jpg","postre10.jpg","postre2.jpg","postre3.jpg","postre4.jpg","postre5.jpg","postre6.jpg","postre7.jpg","postre8.jpg","postre9.jpg","puente1.jpg","puente10.jpg","puente2.jpg","puente3.jpg","puente4.jpg","puente5.jpg","puente6.jpg","puente7.jpg","puente8.jpg","puente9.jpg","rio1.jpg","rio10.jpg","rio2.jpg","rio3.jpg","rio4.jpg","rio5.jpg","rio6.jpg","rio7.jpg","rio8.jpg","rio9.jpg","robot1.jpg","robot10.jpg","robot2.jpg","robot3.jpg","robot4.jpg","robot5.jpg","robot6.jpg","robot7.jpg","robot8.jpg","robot9.jpg","smartphone1.jpg","smartphone10.jpg","smartphone2.jpg","smartphone3.jpg","smartphone4.jpg","smartphone5.jpg","smartphone6.jpg","smartphone7.jpg","smartphone8.jpg","smartphone9.jpg"];

  return (
    <Layout title="Administración de Assets">
      <div style={{ marginBottom: theme.spacing.lg }}>
        <Button onClick={handleCreate} variant="primary">
          Crear Nuevo Asset
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
        {assets.map((asset) => (
          <Card key={asset.id_asset}>
            <img
              src={asset.url_imagen}
              alt={asset.nombre}
              style={{
                width: '100%',
                height: '200px',
                objectFit: 'cover',
                borderRadius: theme.borderRadius.small,
                marginBottom: theme.spacing.sm,
              }}
            />
            <h3 style={{ marginBottom: theme.spacing.sm }}>{asset.nombre}</h3>
            <p style={{ marginBottom: theme.spacing.sm }}>{asset.descripcion}</p>
            <div style={{ display: 'flex', gap: theme.spacing.sm }}>
              <Button
                variant="secondary"
                size="small"
                onClick={() => handleEdit(asset)}
              >
                Editar
              </Button>
              <Button
                variant="error"
                size="small"
                onClick={() => handleDelete(asset.id_asset)}
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
              {selectedAsset ? 'Editar Asset' : 'Crear Asset'}
            </h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
              <div>
                <label htmlFor="asset-nombre" style={{ fontWeight: 500 }}>
                  Nombre
                </label>
                <input
                  id="asset-nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                  aria-required="true"
                />
              </div>
              <div>
                <label htmlFor="asset-descripcion" style={{ fontWeight: 500 }}>
                  Descripción
                </label>
                <textarea
                  id="asset-descripcion"
                  value={formData.descripcion}
                  onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                  required
                  aria-required="true"
                  style={{ minHeight: '60px', resize: 'vertical' }}
                />
              </div>
              <div>
                <label htmlFor="asset-categoria" style={{ fontWeight: 500 }}>
                  Categoría
                </label>
                <select
                  id="asset-categoria"
                  value={formData.id_categoria}
                  onChange={(e) => setFormData({ ...formData, id_categoria: e.target.value })}
                  required
                  aria-required="true"
                >
                  <option value="">Seleccionar categoría</option>
                  {categories.map((category) => (
                    <option key={category.id_categoria} value={category.id_categoria}>
                      {category.nombre}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="asset-imagen" style={{ fontWeight: 500 }}>
                  Imagen
                </label>
                <select
                  id="asset-imagen"
                  value={formData.url_imagen}
                  onChange={e => setFormData({ ...formData, url_imagen: e.target.value })}
                  required
                  aria-required="true"
                >
                  <option value="">Seleccionar imagen</option>
                  {imageOptions.map(img => (
                    <option key={img} value={img}>{img}</option>
                  ))}
                </select>
                {formData.url_imagen && (
                  <img
                    src={`/images/${formData.url_imagen}`}
                    alt="Preview"
                    style={{ width: '100%', maxHeight: 180, objectFit: 'contain', marginTop: 8, borderRadius: 8 }}
                  />
                )}
              </div>
              <div>
                <label htmlFor="asset-tags" style={{ fontWeight: 500 }}>
                  Tags
                </label>
                <select
                  id="asset-tags"
                  multiple
                  value={selectedTags.map(String)}
                  onChange={handleTagChange}
                  style={{ minHeight: 80 }}
                >
                  {tags.map(tag => (
                    <option key={tag.id_tag} value={tag.id_tag}>{tag.nombre}</option>
                  ))}
                </select>
                <small>Ctrl+Click o Shift+Click para seleccionar varios</small>
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
                  disabled={!formData.nombre || !formData.descripcion || !formData.id_categoria}
                >
                  {selectedAsset ? 'Guardar' : 'Crear'}
                </button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </Layout>
  );
};

export default AssetAdmin;

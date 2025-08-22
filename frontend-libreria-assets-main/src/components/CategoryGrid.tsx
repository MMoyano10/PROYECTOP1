import React, { useState, useEffect } from "react";
import { api } from "../api";
import Spinner from './Spinner';

interface Category {
  id_categoria: number;
  nombre: string;
}

export default function CategoryGrid(props: {
  onSelectCategory: (id: number) => void;
}) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .get<Category[]>("/categories/")
      .then((res) => {
        setCategories(res.data);
      })
      .catch((err) => {
        console.error("Error al cargar categorías:", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="grid" style={{ marginBottom: 16 }}>
        {Array.from({ length: 6 }).map((_, i) => (
          <button key={i} className="button skeleton" style={{ height: 40, width: 120 }} disabled />
        ))}
      </div>
    );
  }

  return (
    <div className="grid" style={{ marginBottom: 16 }}>
      {categories.map((cat) => (
        <button
          key={cat.id_categoria}
          onClick={() => props.onSelectCategory(cat.id_categoria)}
          className="button"
        >
          {cat.nombre}
        </button>
      ))}
    </div>
  );
}

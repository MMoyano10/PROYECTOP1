import React, { useState, useEffect } from "react";
import { api } from "../api";
import Spinner from './Spinner';

interface Tag {
  id_tag: number;
  nombre: string;
}

export default function TagGrid(props: {
  categoryId: number;
  onSelectTag: (id: number) => void;
}) {
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!props.categoryId) {
      setTags([]);
      return;
    }
    setLoading(true);
    api
      .get<Tag[]>(`/tags/?category=${props.categoryId}`)
      .then((res) => {
        setTags(res.data);
      })
      .catch((err) => {
        console.error("Error al cargar tags:", err);
        setTags([]);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [props.categoryId]);

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
      {tags.map((tag) => (
        <button
          key={tag.id_tag}
          onClick={() => props.onSelectTag(tag.id_tag)}
          className="button"
        >
          {tag.nombre}
        </button>
      ))}
    </div>
  );
}

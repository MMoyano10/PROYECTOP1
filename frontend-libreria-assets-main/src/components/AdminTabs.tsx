import React, { useState } from "react";
import UserAdmin from "./UserAdmin";
import CategoryAdmin from "./CategoryAdmin";
import TagAdmin from "./TagAdmin";
import AssetAdmin from "./AssetAdmin";

interface Props {
  currentUserId: number;
  showToast?: (msg: string, type?: 'success' | 'error' | 'info') => void;
}

export default function AdminTabs(props: Props) {
  const [activeTab, setActiveTab] = useState<
    "users" | "categories" | "tags" | "assets"
  >("users");

  return (
    <div>
      {/* Botones para cambiar de pestaña */}
      <div style={{ marginBottom: 16 }}>
        <button
          onClick={() => setActiveTab("users")}
          style={{
            marginRight: 8,
            padding: "6px 12px",
            backgroundColor: activeTab === "users" ? "#3498db" : "#ecf0f1",
            color: activeTab === "users" ? "#fff" : "#333",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Usuarios
        </button>

        <button
          onClick={() => setActiveTab("categories")}
          style={{
            marginRight: 8,
            padding: "6px 12px",
            backgroundColor:
              activeTab === "categories" ? "#3498db" : "#ecf0f1",
            color: activeTab === "categories" ? "#fff" : "#333",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Categorías
        </button>

        <button
          onClick={() => setActiveTab("tags")}
          style={{
            marginRight: 8,
            padding: "6px 12px",
            backgroundColor: activeTab === "tags" ? "#3498db" : "#ecf0f1",
            color: activeTab === "tags" ? "#fff" : "#333",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Tags
        </button>

        <button
          onClick={() => setActiveTab("assets")}
          style={{
            padding: "6px 12px",
            backgroundColor: activeTab === "assets" ? "#3498db" : "#ecf0f1",
            color: activeTab === "assets" ? "#fff" : "#333",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Imágenes
        </button>
      </div>

      {/* Contenido de la pestaña activa */}
      {activeTab === "users" && (
        <UserAdmin currentUserId={props.currentUserId} />
      )}
      {activeTab === "categories" && <CategoryAdmin showToast={props.showToast} />}
      {activeTab === "tags" && <TagAdmin showToast={props.showToast} />}
      {activeTab === "assets" && <AssetAdmin showToast={props.showToast} />}
    </div>
  );
}

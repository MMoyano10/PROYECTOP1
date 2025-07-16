// frontend-libreria-assets-main/src/App.tsx

import React, { useEffect, useState } from "react";
import { api } from "./api";
import AuthForm from "./components/AuthForm";
import CategoryGrid from "./components/CategoryGrid";
import TagGrid from "./components/TagGrid";
import ImageGrid from "./components/ImageGrid";
import LogList from "./components/LogList";
import AdminTabs from "./components/AdminTabs";
import Layout from "./components/Layout";
import Navbar from "./components/Navbar";
import { getTheme } from "./theme";
import Spinner from "./components/Spinner";
import OnboardingModal from "./components/OnboardingModal";
import Toast from "./components/Toast";
import Footer from "./components/Footer";

interface User {
  id_usuario: number;
  nombre: string;
  email: string;
  is_admin: boolean;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [selectedCategoryId, setSelectedCategoryId] =
    useState<number | null>(null);
  const [selectedTagId, setSelectedTagId] = useState<number | null>(null);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });
  const theme = getTheme(darkMode ? 'dark' : 'light');
  const [images, setImages] = useState<any[]>([]);
  const [imagesLoading, setImagesLoading] = useState(false);
  const [imagesError, setImagesError] = useState<string | null>(null);
  const [showOnboarding, setShowOnboarding] = useState(() => {
    return localStorage.getItem('onboardingDismissed') !== 'true';
  });
  const [toast, setToast] = useState<{ message: string; type?: 'success' | 'error' | 'info' } | null>(null);
  const showToast = (message: string, type?: 'success' | 'error' | 'info') => {
    setToast({ message, type });
  };

  useEffect(() => {
    document.body.style.background = theme.colors.background.main;
    document.body.className = darkMode ? 'dark-mode' : '';
    localStorage.setItem('darkMode', darkMode ? 'true' : 'false');
  }, [darkMode, theme.colors.background.main]);

  // 1) Al montar, chequeamos si ya hay un usuario guardado en localStorage
  useEffect(() => {
    const stored = localStorage.getItem("currentUser");
    if (stored) {
      try {
        const u: User = JSON.parse(stored);
        setCurrentUser(u);
      } catch (e) {
        console.error("Error parseando currentUser en localStorage:", e);
        localStorage.removeItem("currentUser");
      }
    }
  }, []);

  // 2) Función para cerrar sesión
  const handleLogout = async () => {
    try {
      await api.post('/users/logout');
    } catch (e) {
      // Ignorar errores de logout
    }
    setCurrentUser(null);
    localStorage.removeItem("currentUser");
    localStorage.removeItem("access_token");
    setSelectedCategoryId(null);
    setSelectedTagId(null);
    setImages([]);
    setImagesLoading(false);
    setImagesError(null);
  };

  // 3) Método genérico para crear un log
  const enviarLog = (accion: string, idAsset?: number) => {
    if (!currentUser || !accion) return;

    // Construimos el JSON exacto que espera el servicio de Logs:
    const payload: any = {
      id_usuario: currentUser.id_usuario,
      accion: String(accion),
    };
    // Si hubo un asset (imagen) relacionado, lo agregamos:
    if (idAsset !== undefined && idAsset !== null) {
      payload.id_asset = idAsset;
    }

    // Elimina cualquier campo undefined
    Object.keys(payload).forEach(key => {
      if (payload[key] === undefined) delete payload[key];
    });

    // Ahora sí hacemos la petición a /logs/ (recordar: baseURL ya es http://localhost:8000/api)
    api
      .post("/logs/", payload, {
        headers: {
          "X-User-Id": String(currentUser.id_usuario),
        },
      })
      .catch((err) => {
        // En caso de error 422/500, imprímelo para depurar
        if (err.response && err.response.data) {
          console.error("Detalle error al crear log:", err.response.data);
        } else {
          console.error("Error al crear log:", err);
        }
      });
  };

  // 4) Callbacks de selección
  const onSelectCategory = (categoriaId: number) => {
    setSelectedCategoryId(categoriaId);
    setSelectedTagId(null);
    enviarLog(`Seleccionó categoría: ${categoriaId}`);
  };

  const onSelectTag = (tagId: number) => {
    setSelectedTagId(tagId);
    enviarLog(`Seleccionó tag: ${tagId}`);
  };

  const onImageClick = (filename: string) => {
    enviarLog(`Visualizó imagen: ${filename}`);
  };

  useEffect(() => {
    if (selectedCategoryId !== null && selectedTagId !== null) {
      setImagesLoading(true);
      setImagesError(null);
      api
        .get(`/assets/?category=${selectedCategoryId}&tag=${selectedTagId}`)
        .then((res) => {
          setImages(res.data);
        })
        .catch((err) => {
          setImagesError("Error al cargar imágenes");
          setImages([]);
        })
        .finally(() => {
          setImagesLoading(false);
        });
    } else {
      setImages([]);
    }
  }, [selectedCategoryId, selectedTagId]);

  const handleDismissOnboarding = () => {
    setShowOnboarding(false);
    localStorage.setItem('onboardingDismissed', 'true');
  };

  // 5) Si no hay usuario logueado, mostrar formulario
  if (!currentUser) {
    return (
      <>
        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
        <AuthForm
          onLoginSuccess={(loginData: LoginResponse) => {
            setCurrentUser(loginData.user);
            localStorage.setItem("currentUser", JSON.stringify(loginData.user));
          }}
          onLoginError={(msg) => showToast(msg, 'error')}
        />
        <Footer />
      </>
    );
  }

  // 6) Si el usuario NO es admin, vista normal con logout
  if (currentUser && !currentUser.is_admin) {
    return (
      <>
        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
        {showOnboarding && <OnboardingModal onClose={handleDismissOnboarding} />}
        <Navbar
          userName={currentUser.nombre}
          isAdmin={false}
          onLogout={handleLogout}
          onToggleDarkMode={() => setDarkMode((d) => !d)}
          darkMode={darkMode}
        />
        <Layout title="Mi Librería de Imágenes">
          <CategoryGrid onSelectCategory={onSelectCategory} />
          {selectedCategoryId !== null && (
            <>
              <h2>Tags para categoría {selectedCategoryId}</h2>
              <TagGrid
                categoryId={selectedCategoryId}
                onSelectTag={onSelectTag}
              />
            </>
          )}
          {selectedCategoryId !== null && selectedTagId !== null && (
            <>
              <h2>
                Imágenes para cat={selectedCategoryId} ↔ tag={selectedTagId}
              </h2>
              {imagesLoading ? (
                <ImageGrid loading images={[]} />
              ) : imagesError ? (
                <p style={{ color: 'red' }}>{imagesError}</p>
              ) : (
                <ImageGrid
                  images={images}
                  onImageClick={onImageClick}
                />
              )}
            </>
          )}
        </Layout>
        <Footer />
      </>
    );
  }

  // 7) Si el usuario ES admin, muestro panel de administración + logs
  return (
    <>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      {showOnboarding && <OnboardingModal onClose={handleDismissOnboarding} />}
      <Navbar
        userName={currentUser.nombre}
        isAdmin={true}
        onLogout={handleLogout}
        onToggleDarkMode={() => setDarkMode((d) => !d)}
        darkMode={darkMode}
      />
      <Layout title="Panel de Administración">
        <AdminTabs currentUserId={currentUser.id_usuario} showToast={showToast} />
        <hr style={{ margin: "24px 0" }} />
        <h2>Logs de actividad</h2>
        <LogList currentUserId={currentUser.id_usuario} />
      </Layout>
      <Footer />
    </>
  );
}

// frontend-libreria-assets-main/src/App.tsx

import React, { useEffect, useState } from "react";
import type { AxiosError } from "axios";
import { api } from "./api";
import AuthForm from "./components/AuthForm";
import CategoryGrid from "./components/CategoryGrid";
import TagGrid from "./components/TagGrid";
import ImageGrid from "./components/ImageGrid";
import ViewImage from "./components/ViewImage";
import { useSocket } from "./hooks/useSocket";
import { Socket } from "socket.io-client";
// Nota: no llames hooks fuera de un componente. Todo uso de hooks va dentro de App().
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
  const [selectedImage, setSelectedImage] = useState<any | null>(null);
  const [lockedAssets, setLockedAssets] = useState<{ [id: number]: boolean }>({});
  const socketRef = useSocket((socket: Socket) => {
    socket.on("asset_locked", ({ asset_id, locked }) => {
      setLockedAssets((prev) => ({ ...prev, [asset_id]: locked }));
    });
    socket.on("asset_unlocked", ({ asset_id }) => {
      setLockedAssets((prev) => {
        const copy = { ...prev };
        delete copy[asset_id];
        return copy;
      });
    });
  });
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
    // Si tenemos token pero no user, intentamos cargar /users/me
    const token = localStorage.getItem('access_token');
    const stored = localStorage.getItem("currentUser");
    if (token && !stored) {
      api.get<User>('/users/me')
        .then((res: { data: User }) => {
          localStorage.setItem('currentUser', JSON.stringify(res.data as User));
          setCurrentUser(res.data as User);
        })
        .catch(() => {
          // token inválido
          localStorage.removeItem('access_token');
        });
    }
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
      .catch((err: unknown) => {
        const e = err as AxiosError<any>;
        // En caso de error 422/500, imprímelo para depurar
        if (e?.response?.data) {
          console.error("Detalle error al crear log:", e.response.data);
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

  const onImageClick = (image: any) => {
    setSelectedImage(image);
    enviarLog(`Visualizó imagen: ${image.filename || image.nombre}`);
  };

  useEffect(() => {
    if (selectedCategoryId !== null && selectedTagId !== null) {
      setImagesLoading(true);
      setImagesError(null);
      api
        .get(`/assets/?category=${selectedCategoryId}&tag=${selectedTagId}`)
        .then((res: { data: any[] }) => {
          setImages(res.data as any[]);
        })
        .catch((_err: unknown) => {
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
          onLoginError={(msg: string) => showToast(msg, 'error')}
        />
        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <a
            href="http://localhost:8000/api/users/auth/google"
            style={{
              display: 'inline-block',
              padding: '10px 16px',
              borderRadius: 6,
              background: '#4285F4',
              color: 'white',
              textDecoration: 'none',
              fontWeight: 600,
            }}
          >
            Continuar con Google
          </a>
        </div>
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
          onToggleDarkMode={() => setDarkMode((d: boolean) => !d)}
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
              {selectedImage && socketRef.current && (
                <ViewImage
                  image={selectedImage}
                  socket={socketRef.current}
                  onClose={() => setSelectedImage(null)}
                  locked={lockedAssets[selectedImage.id_asset] && lockedAssets[selectedImage.id_asset] !== false}
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
  onToggleDarkMode={() => setDarkMode((d: boolean) => !d)}
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

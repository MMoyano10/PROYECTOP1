// frontend-libreria-assets-main/src/components/AuthForm.tsx

import React, { useState } from "react";
import { api } from "../api";
import { theme } from '../theme';
import Layout from './Layout';
import Button from './Button';
import Card from './Card';

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id_usuario: number;
    nombre: string;
    email: string;
    is_admin: boolean;
  };
}

interface AuthFormProps {
  onLoginSuccess: (userData: LoginResponse) => void;
  onLoginError?: (msg: string) => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ onLoginSuccess, onLoginError }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [emailTouched, setEmailTouched] = useState(false);

  const isEmailValid = email.match(/^\S+@\S+\.\S+$/);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    api
      .post<LoginResponse>("/users/login", { email, password })
      .then((res) => {
        // Guardar el token en localStorage
        localStorage.setItem("access_token", res.data.access_token);
        onLoginSuccess(res.data);
      })
      .catch((err) => {
        const msg = err.response?.data?.detail || "Error al iniciar sesión";
        setError(msg);
        if (onLoginError) onLoginError(msg);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Layout title="Iniciar Sesión">
      <Card style={{ maxWidth: '400px', margin: '0 auto' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.md }}>
          <div>
            <label htmlFor="login-email" style={{ fontWeight: 500 }}>
              Email
            </label>
            <input
              id="login-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onBlur={() => setEmailTouched(true)}
              aria-invalid={emailTouched && !isEmailValid ? 'true' : 'false'}
              aria-describedby="email-error"
              required
            />
            {emailTouched && !isEmailValid && (
              <span id="email-error" style={{ color: theme.colors.error, fontSize: '0.95em' }}>
                Ingresa un email válido.
              </span>
            )}
          </div>
          <div>
            <label htmlFor="login-password" style={{ fontWeight: 500 }}>
              Contraseña
            </label>
            <input
              id="login-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && (
            <div style={{ color: theme.colors.error, marginBottom: theme.spacing.sm }}>
              {error}
            </div>
          )}
          <button type="submit" className="button" disabled={loading || (emailTouched && !isEmailValid)}>
            {loading ? "Autenticando…" : "Ingresar"}
          </button>
        </form>
      </Card>
    </Layout>
  );
};

export default AuthForm;

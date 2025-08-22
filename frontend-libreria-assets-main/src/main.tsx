import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// Captura token de OAuth si viene en query (?token=...)
const url = new URL(window.location.href);
const tokenFromOAuth = url.searchParams.get('token');
if (tokenFromOAuth) {
  localStorage.setItem('access_token', tokenFromOAuth);
  // limpiar la query para no dejar el token en la barra
  url.searchParams.delete('token');
  window.history.replaceState({}, document.title, url.pathname + url.search + url.hash);
}

ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

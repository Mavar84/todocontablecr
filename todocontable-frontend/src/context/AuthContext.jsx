import React from "react";
import { createContext, useState } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));

  function guardarSesion(datos, jwt) {
    setUsuario(datos);
    setToken(jwt);
    localStorage.setItem("token", jwt);
  }

  function cerrarSesion() {
    setUsuario(null);
    setToken(null);
    localStorage.removeItem("token");
  }

  return (
    <AuthContext.Provider value={{ usuario, token, guardarSesion, cerrarSesion }}>
      {children}
    </AuthContext.Provider>
  );
}

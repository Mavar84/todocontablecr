import api from "./apiClient";

export async function loginUsuario(credenciales) {
  const respuesta = await api.post("/login", credenciales);
  return respuesta.data;
}

export async function registrarUsuario(datos) {
  const respuesta = await api.post("/signup", datos);
  return respuesta.data;
}

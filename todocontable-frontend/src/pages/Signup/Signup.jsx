import React, { useState, useContext } from "react";
import { TextField, Button, Card, CardContent, Typography } from "@mui/material";
import { crearUsuario } from "../../api/auth";
import { AuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [confirmarContrasena, setConfirmarContrasena] = useState("");
  const [error, setError] = useState("");
  const [mensajeExito, setMensajeExito] = useState("");

  if (!token) {
    return (
      <Typography variant="h6" sx={{ padding: 3 }}>
        Debe iniciar sesión como administrador para crear nuevos usuarios.
      </Typography>
    );
  }

  async function manejarRegistro(e) {
    e.preventDefault();
    setError("");
    setMensajeExito("");

    if (contrasena !== confirmarContrasena) {
      setError("Las contraseñas no coinciden");
      return;
    }

    try {
      const nuevoUsuario = {
        nombre: nombre,
        correo: correo,
        contrasena: contrasena
      };

      await crearUsuario(nuevoUsuario);

      setMensajeExito("Usuario creado correctamente.");
      
      setTimeout(() => {
        navigate("/dashboard");
      }, 1200);

    } catch (err) {
      setError("Error al registrar. Verifique los datos o permisos.");
    }
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <Card sx={{ width: 420, padding: 3 }}>
        <CardContent>
          <Typography variant="h5" sx={{ textAlign: "center", marginBottom: 2 }}>
            Registrar Nuevo Usuario
          </Typography>

          {error && (
            <Typography color="error" sx={{ marginBottom: 2 }}>
              {error}
            </Typography>
          )}

          {mensajeExito && (
            <Typography sx={{ marginBottom: 2, color: "green" }}>
              {mensajeExito}
            </Typography>
          )}

          <form onSubmit={manejarRegistro}>

            <TextField
              fullWidth
              label="Nombre completo"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              sx={{ marginBottom: 2 }}
            />

            <TextField
              fullWidth
              label="Correo electrónico"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              sx={{ marginBottom: 2 }}
            />

            <TextField
              fullWidth
              label="Contraseña"
              type="password"
              value={contrasena}
              onChange={(e) => setContrasena(e.target.value)}
              sx={{ marginBottom: 2 }}
            />

            <TextField
              fullWidth
              label="Confirmar contraseña"
              type="password"
              value={confirmarContrasena}
              onChange={(e) => setConfirmarContrasena(e.target.value)}
              sx={{ marginBottom: 3 }}
            />

            <Button fullWidth variant="contained" type="submit">
              Crear Usuario
            </Button>

            <Button
              fullWidth
              sx={{ marginTop: 1 }}
              variant="outlined"
              onClick={() => navigate("/dashboard")}
            >
              Cancelar
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

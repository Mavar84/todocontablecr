import React, { useState, useContext } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { TextField, Button, Card, CardContent, Typography } from "@mui/material";
import { AuthContext } from "../../context/AuthContext";
import { loginUsuario } from "../../api/auth";

export default function Login() {
  const { guardarSesion } = useContext(AuthContext);
  const navigate = useNavigate();

  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState("");

  async function manejarLogin(e) {
    e.preventDefault();
    setError("");

    try {
      const datos = await loginUsuario({
        correo: correo,
        contrasena: contrasena,
      });

      /* -------------------------------------------------------
         Guardar token + usuario SIEMPRE (admin o normal)
      ------------------------------------------------------- */
      guardarSesion(datos.usuario, datos.access_token);

      /* -------------------------------------------------------
         Lógica nueva según 'access_type'
      ------------------------------------------------------- */

      if (datos.access_type === "new_user_creator") {
        navigate("/signup");   // Página para registrar usuarios
        return;
      }

      // Usuario normal → dashboard
      navigate("/dashboard");

    } catch (err) {
      setError("Credenciales incorrectas");
    }
  }

  const { token } = useContext(AuthContext);

  if (token) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div style={{
      width: "100%",
      height: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "#f4f4f4",
    }}>
      <Card sx={{ width: 380, padding: 2 }}>
        <CardContent>
          <Typography variant="h5" sx={{ textAlign: "center", marginBottom: 2 }}>
            Inicio de Sesión
          </Typography>

          {error && (
            <Typography color="error" sx={{ marginBottom: 2 }}>
              {error}
            </Typography>
          )}

          <form onSubmit={manejarLogin}>
            <TextField
              fullWidth
              label="Correo"
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
              sx={{ marginBottom: 3 }}
            />

            <Button fullWidth variant="contained" type="submit">
              Ingresar
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

import React from "react";
import { useContext } from "react";
import { Grid, Card, CardContent, Typography } from "@mui/material";
import { AuthContext } from "../../context/AuthContext";

export default function Dashboard() {
  const { usuario } = useContext(AuthContext);

  return (
    <div style={{ padding: "20px" }}>
      <Typography variant="h4" sx={{ marginBottom: 3 }}>
        Bienvenido(a){usuario ? `, ${usuario.nombre}` : ""}
      </Typography>

      <Grid container spacing={3}>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Cuentas contables</Typography>
              <Typography variant="h4" sx={{ marginTop: 1 }}>
                0
              </Typography>
              <Typography variant="body2">Registradas en el sistema</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Clientes</Typography>
              <Typography variant="h4" sx={{ marginTop: 1 }}>
                0
              </Typography>
              <Typography variant="body2">Activos</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Proveedores</Typography>
              <Typography variant="h4" sx={{ marginTop: 1 }}>
                0
              </Typography>
              <Typography variant="body2">En total</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Asientos diarios</Typography>
              <Typography variant="h4" sx={{ marginTop: 1 }}>
                0
              </Typography>
              <Typography variant="body2">Registrados este mes</Typography>
            </CardContent>
          </Card>
        </Grid>

      </Grid>

      <Card sx={{ marginTop: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 2 }}>
            Información del usuario
          </Typography>

          {usuario ? (
            <>
              <Typography>Nombre: {usuario.nombre}</Typography>
              <Typography>Correo: {usuario.correo}</Typography>
              <Typography>Rol: {usuario.rol}</Typography>
            </>
          ) : (
            <Typography>No hay información de usuario cargada.</Typography>
          )}
        </CardContent>
      </Card>

    </div>
  );
}

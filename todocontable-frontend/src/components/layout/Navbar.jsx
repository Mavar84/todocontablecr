import React, { useContext } from "react";
import { AppBar, Toolbar, Typography, IconButton, Button } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { AuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar({ toggleSidebar }) {
  const { cerrarSesion } = useContext(AuthContext);
  const navigate = useNavigate();

  function manejarLogout() {
    cerrarSesion();               // limpia usuario + token en contexto
    localStorage.removeItem("token");
    navigate("/");                // vuelve al login
  }

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        zIndex: 1400,
        background: "rgba(15, 31, 50, 0.55)",
        backdropFilter: "blur(10px)",
        borderBottom: "1px solid rgba(255,255,255,0.2)",
      }}
    >
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        
        {/* Menú izquierda */}
        <div style={{ display: "flex", alignItems: "center" }}>
          <IconButton color="inherit" onClick={toggleSidebar} edge="start">
            <MenuIcon />
          </IconButton>

          <Typography variant="h6" sx={{ marginLeft: 2, color: "#e2e8f0" }}>
            TodoContableCR
          </Typography>
        </div>

        {/* Botón Logout derecha */}
        <Button
          onClick={manejarLogout}
          sx={{
            color: "#e2e8f0",
            border: "1px solid rgba(255,255,255,0.3)",
            padding: "6px 14px",
            textTransform: "none",
            "&:hover": {
              background: "rgba(255,255,255,0.15)",
            }
          }}
        >
          Logout
        </Button>

      </Toolbar>
    </AppBar>
  );
}

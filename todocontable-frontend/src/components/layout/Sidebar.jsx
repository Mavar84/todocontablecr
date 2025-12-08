
import React from "react";
import { Drawer, List, ListItem, ListItemText, ListItemButton } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function Sidebar({ open, toggleSidebar }) {
  const navigate = useNavigate();

  function ir(ruta) {
    navigate(ruta);
    toggleSidebar();
  }

  return (
    <Drawer open={open} onClose={toggleSidebar}>
      <List sx={{ width: 260 }}>
        <ListItem disablePadding>
          <ListItemButton onClick={() => ir("/dashboard")}>
            <ListItemText primary="Dashboard" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton onClick={() => ir("/catalogo-cuentas")}>
            <ListItemText primary="Catálogo de Cuentas" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton onClick={() => ir("/usuarios")}>
            <ListItemText primary="Usuarios" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton onClick={() => ir("/clientes")}>
            <ListItemText primary="Clientes" />
          </ListItemButton>
        </ListItem>

      </List>
    </Drawer>
  );
}

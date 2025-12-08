import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { token } = useContext(AuthContext);

  // Si NO hay token → mandar al login
  if (!token) {
    return <Navigate to="/" replace />;
  }

  // Si hay token → permitir acceso
  return children;
}

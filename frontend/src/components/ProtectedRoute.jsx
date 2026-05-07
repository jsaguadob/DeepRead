import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children, requireAdmin, requireProfesor }) {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;

  if (requireAdmin && user.rol !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  if (requireProfesor && user.rol === 'estudiante') {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

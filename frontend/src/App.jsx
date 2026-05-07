import { Routes, Route } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LoadingSkeleton from './components/LoadingSkeleton';
import { ToastContainer } from './components/Toast';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Lecturas from './pages/Lecturas';
import LecturaDetalle from './pages/LecturaDetalle';
import Quiz from './pages/Quiz';
import QuizManage from './pages/QuizManage';
import Progreso from './pages/Progreso';
import Actividades from './pages/Actividades';
import ActividadResolver from './pages/ActividadResolver';
import Grupos from './pages/Grupos';
import GrupoDetalle from './pages/GrupoDetalle';
import GrupoCalificaciones from './pages/GrupoCalificaciones';
import AdminPanel from './pages/AdminPanel';
import AdminInstituciones from './pages/AdminInstituciones';
import AdminEstadisticas from './pages/AdminEstadisticas';

export default function App() {
  const { loading } = useAuth();

  if (loading) return <LoadingSkeleton />;

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/lecturas" element={<ProtectedRoute><Lecturas /></ProtectedRoute>} />
        <Route path="/lecturas/:id" element={<ProtectedRoute><LecturaDetalle /></ProtectedRoute>} />
        <Route path="/lecturas/:id/quiz" element={<ProtectedRoute><Quiz /></ProtectedRoute>} />
        <Route path="/lecturas/:id/quiz/manage" element={<ProtectedRoute requireProfesor><QuizManage /></ProtectedRoute>} />
        <Route path="/progreso" element={<ProtectedRoute><Progreso /></ProtectedRoute>} />
        <Route path="/actividades" element={<ProtectedRoute><Actividades /></ProtectedRoute>} />
        <Route path="/actividades/:id" element={<ProtectedRoute><ActividadResolver /></ProtectedRoute>} />
        <Route path="/grupos" element={<ProtectedRoute><Grupos /></ProtectedRoute>} />
        <Route path="/grupos/:id" element={<ProtectedRoute><GrupoDetalle /></ProtectedRoute>} />
        <Route path="/grupos/:id/calificaciones" element={<ProtectedRoute requireProfesor><GrupoCalificaciones /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute requireAdmin><AdminPanel /></ProtectedRoute>} />
        <Route path="/admin/instituciones" element={<ProtectedRoute requireAdmin><AdminInstituciones /></ProtectedRoute>} />
        <Route path="/admin/estadisticas" element={<ProtectedRoute requireAdmin><AdminEstadisticas /></ProtectedRoute>} />
      </Routes>
    </Layout>
  );
}

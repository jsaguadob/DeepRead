import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { ToastContainer } from './Toast';
import AIChatWidget from './AIChatWidget';
import {
  faBook, faTachometerAlt, faChartLine, faUsers, faGraduationCap,
  faGamepad, faPlus, faSignOutAlt, faBars, faTimes, faStar, faCrown
} from '@fortawesome/free-solid-svg-icons';

export default function Layout({ children }) {
  const { user, logout, isAdmin, isProfesor } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-frost-50">
      <ToastContainer />
      <header className="bg-gradient-to-r from-void-800 to-void-600 text-white shadow-lg">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-3 text-xl font-heading font-bold">
              <FontAwesomeIcon icon={faBook} className="text-iris-400 text-2xl" />
              <span className="bg-gradient-to-r from-iris-400 to-flare-400 bg-clip-text text-transparent">
                DeepRead
              </span>
            </Link>

            {/* Desktop nav */}
            <div className="hidden lg:flex items-center gap-0.5">
              {user ? (
                <>
                  <NavLink to="/dashboard" icon={faTachometerAlt} label="Dashboard" />
                  <NavLink to="/lecturas" icon={faBook} label="Lecturas" />
                  <NavLink to="/progreso" icon={faChartLine} label="Progreso" />
                  <NavLink to="/actividades" icon={faGamepad} label="Actividades" />
                  <NavLink to="/grupos" icon={faUsers} label="Grupos" />
                  {isAdmin() && (
                    <>
                      <NavLink to="/admin" icon={faCrown} label="Admin" />
                      <NavLink to="/admin/estadisticas" icon={faChartLine} label="Stats" />
                      <NavLink to="/lecturas?crear=true" icon={faPlus} label="Nueva" />
                    </>
                  )}

                  <div className="flex items-center gap-2 ml-3 pl-3 border-l border-white/20">
                    <div className="flex items-center gap-1 text-iris-400 text-xs">
                      <FontAwesomeIcon icon={faStar} className="text-[10px]" />
                      <span className="font-semibold">{user.puntos_totales}</span>
                    </div>
                    <span className="bg-iris-500/20 text-iris-300 px-1.5 py-0.5 rounded text-[10px] font-semibold">
                      Nv.{user.nivel_actual}
                    </span>
                    <span className="bg-white/10 px-1.5 py-0.5 rounded text-[10px] capitalize">
                      {user.rol}
                    </span>
                    <button onClick={handleLogout}
                      className="bg-red-500/20 hover:bg-red-500/40 text-red-300 px-2 py-1 rounded text-xs transition">
                      <FontAwesomeIcon icon={faSignOutAlt} />
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-white/80 hover:text-white px-4 py-2 transition">Iniciar Sesión</Link>
                  <Link to="/register"
                    className="bg-iris-500 hover:bg-iris-600 text-white px-5 py-2 rounded-lg font-medium transition shadow-lg shadow-iris-500/25">
                    Registrarse
                  </Link>
                </>
              )}
            </div>

            {/* Mobile menu button */}
            <button onClick={() => setMenuOpen(!menuOpen)} className="lg:hidden text-xl p-1">
              <FontAwesomeIcon icon={menuOpen ? faTimes : faBars} />
            </button>
          </div>

          {/* Mobile nav */}
          {menuOpen && (
            <div className="lg:hidden pb-3 border-t border-white/10 pt-2 space-y-0.5 text-sm">
              {user ? (
                <>
                  <MobileNavLink to="/dashboard" label="Dashboard" onClick={() => setMenuOpen(false)} />
                  <MobileNavLink to="/lecturas" label="Lecturas" onClick={() => setMenuOpen(false)} />
                  <MobileNavLink to="/progreso" label="Mi Progreso" onClick={() => setMenuOpen(false)} />
                  <MobileNavLink to="/actividades" label="Actividades" onClick={() => setMenuOpen(false)} />
                  <MobileNavLink to="/grupos" label="Mis Grupos" onClick={() => setMenuOpen(false)} />
                  {isAdmin() && (
                    <>
                      <MobileNavLink to="/admin/estadisticas" label="Estadísticas" onClick={() => setMenuOpen(false)} />
                      <MobileNavLink to="/lecturas?crear=true" label="+ Crear Lectura" onClick={() => setMenuOpen(false)} />
                      <MobileNavLink to="/admin" label="Panel Admin" onClick={() => setMenuOpen(false)} />
                      <MobileNavLink to="/admin/instituciones" label="Instituciones" onClick={() => setMenuOpen(false)} />
                    </>
                  )}

                  <div className="flex items-center gap-3 pt-3 pb-2 border-t border-white/10 mt-2">
                    <span className="text-iris-400"><FontAwesomeIcon icon={faStar} /> {user.puntos_totales} pts</span>
                    <span className="bg-white/10 px-2 py-0.5 rounded-full text-xs">Nv.{user.nivel_actual}</span>
                    <span className="bg-white/10 px-2 py-0.5 rounded-full text-xs capitalize">{user.rol}</span>
                  </div>
                  <button onClick={() => { handleLogout(); setMenuOpen(false); }}
                    className="flex items-center gap-2 text-red-300 py-2 w-full">
                    <FontAwesomeIcon icon={faSignOutAlt} /> Cerrar Sesión
                  </button>
                </>
              ) : (
                <>
                  <MobileNavLink to="/login" label="Iniciar Sesión" onClick={() => setMenuOpen(false)} />
                  <MobileNavLink to="/register" label="Registrarse" onClick={() => setMenuOpen(false)} />
                </>
              )}
            </div>
          )}
        </nav>
      </header>

      <main className="flex-1">
        {children}
      </main>

      <footer className="bg-void-800 text-white/60 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <FontAwesomeIcon icon={faBook} className="text-iris-400" />
            <span className="font-heading font-bold text-white/80">DeepRead</span>
          </div>
          <p className="text-sm">Mejora tu lectura crítica</p>
          <p className="text-xs mt-1">Desarrollado para estudiantes y educadores</p>
        </div>
      </footer>
      {user && (isAdmin() || isProfesor()) && <AIChatWidget />}
    </div>
  );
}

function NavLink({ to, icon, label }) {
  return (
    <Link to={to}
      className="flex items-center gap-1 text-white/70 hover:text-white px-2 py-1.5 rounded-lg hover:bg-white/5 transition text-xs font-medium">
      <FontAwesomeIcon icon={icon} className="text-[10px]" />
      {label}
    </Link>
  );
}

function MobileNavLink({ to, label, onClick }) {
  return (
    <Link to={to} onClick={onClick}
      className="block text-white/70 hover:text-white py-2 px-2 rounded hover:bg-white/5 transition">
      {label}
    </Link>
  );
}

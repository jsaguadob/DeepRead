import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { stats } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook, faStar, faTrophy, faFire, faArrowRight, faChartLine } from '@fortawesome/free-solid-svg-icons';

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);

  useEffect(() => {
    stats.getProgress().then(res => setData(res.data)).catch(() => {});
  }, []);

  if (!data) return <div className="p-8 text-center text-void-400">Cargando...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">
            Dashboard
          </h1>
          <p className="text-void-400 mt-1">Bienvenido, {user.username}</p>
        </div>
        <Link to="/lecturas"
          className="bg-iris-500 hover:bg-iris-600 text-white px-5 py-2.5 rounded-xl font-medium transition shadow-lg shadow-iris-500/25 flex items-center gap-2">
          Explorar Lecturas <FontAwesomeIcon icon={faArrowRight} />
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard icon={faBook} label="Lecturas Completadas" value={data.lecturas_completadas.length} color="text-iris-400" bg="bg-iris-50" />
        <StatCard icon={faStar} label="Puntos Totales" value={user.puntos_totales} color="text-flare-500" bg="bg-flare-50" />
        <StatCard icon={faTrophy} label="Nivel Actual" value={`Nv. ${user.nivel_actual}`} color="text-teal-500" bg="bg-teal-50" />
        <StatCard icon={faFire} label="Racha" value={`${user.racha_dias || 0} días`} color="text-iris-400" bg="bg-iris-50" />
      </div>

      {/* Progress Bar */}
      <div className="bg-white rounded-2xl shadow-sm p-6 mb-8 border border-frost-200">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-heading font-semibold text-void-800">Progreso al Nivel {user.nivel_actual + 1}</h3>
          <span className="text-sm text-void-400">
            {user.puntos_totales} / {data.puntos_necesarios} pts
          </span>
        </div>
        <div className="h-3 bg-frost-200 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-iris-400 to-flare-400 rounded-full transition-all duration-700"
            style={{ width: `${Math.min(data.progreso_nivel, 100)}%` }} />
        </div>
      </div>

      {/* Recent readings */}
      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
        <h3 className="font-heading font-semibold text-void-800 mb-4 flex items-center gap-2">
          <FontAwesomeIcon icon={faChartLine} className="text-teal-500" />
          Lecturas Recientes
        </h3>
        {data.lecturas_completadas.length > 0 ? (
          <div className="space-y-3">
            {data.lecturas_completadas.slice(0, 5).map((l, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-frost-100 last:border-0">
                <span className="text-void-700">{l.titulo}</span>
                <div className="flex items-center gap-3">
                  <span className="text-xs px-2 py-0.5 rounded-full bg-teal-50 text-teal-600">Nv.{l.nivel}</span>
                  <span className="text-sm text-flare-500 font-medium">+{l.puntos}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-void-400 text-sm">No has completado lecturas aún.</p>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color, bg }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 card-hover">
      <div className={`w-10 h-10 ${bg} rounded-xl flex items-center justify-center mb-3`}>
        <FontAwesomeIcon icon={icon} className={color} />
      </div>
      <p className="text-2xl font-heading font-bold text-void-800">{value}</p>
      <p className="text-sm text-void-400">{label}</p>
    </div>
  );
}

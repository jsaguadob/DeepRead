import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { stats } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faBook, faStar, faTrophy, faFire, faBrain, faTimesCircle } from '@fortawesome/free-solid-svg-icons';

export default function Progreso() {
  const { user } = useAuth();
  const [data, setData] = useState(null);

  useEffect(() => {
    stats.getProgress().then(res => setData(res.data)).catch(() => {});
  }, []);

  if (!data) return <div className="p-8 text-center text-void-400">Cargando...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center gap-3 mb-8">
        <FontAwesomeIcon icon={faChartLine} className="text-3xl text-iris-400" />
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">Mi Progreso</h1>
          <p className="text-void-400">Historial de aprendizaje</p>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard icon={faBook} label="Completadas" value={data.lecturas_completadas.length} color="text-teal-500" bg="bg-teal-50" />
        <StatCard icon={faStar} label="Puntos" value={user.puntos_totales} color="text-flare-500" bg="bg-flare-50" />
        <StatCard icon={faTrophy} label="Nivel" value={`Nv. ${user.nivel_actual}`} color="text-iris-400" bg="bg-iris-50" />
        <StatCard icon={faFire} label="Racha" value={`${user.racha_dias || 0} días`} color="text-iris-500" bg="bg-iris-50" />
      </div>

      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mb-8">
        <h3 className="font-heading font-semibold text-void-800 mb-3">Progreso al Nivel {user.nivel_actual + 1}</h3>
        <div className="h-3 bg-frost-200 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-iris-400 to-flare-400 rounded-full transition-all"
            style={{ width: `${Math.min(data.progreso_nivel, 100)}%` }} />
        </div>
        <p className="text-sm text-void-400 mt-2">{user.puntos_totales} / {data.puntos_necesarios} pts</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
        <h3 className="font-heading font-semibold text-void-800 mb-4 flex items-center gap-2">
          <FontAwesomeIcon icon={faBook} className="text-teal-500" />
          Lecturas Completadas ({data.lecturas_completadas.length})
        </h3>
        {data.lecturas_completadas.length > 0 ? (
          <div className="space-y-3">
            {data.lecturas_completadas.map((l, i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-frost-100 last:border-0">
                <div>
                  <p className="text-void-700 font-medium">{l.titulo}</p>
                  <p className="text-xs text-void-400">{l.fecha ? new Date(l.fecha).toLocaleDateString() : ''}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    l.nivel === 1 ? 'bg-teal-50 text-teal-600' :
                    l.nivel === 2 ? 'bg-flare-50 text-flare-600' :
                    'bg-iris-50 text-iris-600'
                  }`}>Nv.{l.nivel}</span>
                  <span className="text-sm text-flare-500 font-semibold">+{l.puntos}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-void-400 text-sm">No has completado lecturas aún. ¡Empieza ahora!</p>
        )}
      </div>

      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mt-6">
        <h3 className="font-heading font-semibold text-void-800 mb-4 flex items-center gap-2">
          <FontAwesomeIcon icon={faBrain} className="text-iris-500" />
          Historial de Quizzes ({data.quiz_historial?.length || 0})
        </h3>
        <div className="flex items-center gap-2 mb-4 text-sm text-void-400">
          <FontAwesomeIcon icon={faTimesCircle} className="text-red-400" />
          Total errores acumulados: <span className="font-semibold text-red-500">{data.total_fallos || 0}</span>
        </div>
        {data.quiz_historial?.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-frost-200">
                  <th className="p-2 text-left text-void-500 font-medium">Lectura</th>
                  <th className="p-2 text-center text-void-500 font-medium">Intentos</th>
                  <th className="p-2 text-center text-void-500 font-medium">%</th>
                  <th className="p-2 text-center text-void-500 font-medium">Errores</th>
                  <th className="p-2 text-center text-void-500 font-medium">Estado</th>
                </tr>
              </thead>
              <tbody>
                {data.quiz_historial.map((q, i) => (
                  <tr key={i} className="border-b border-frost-100">
                    <td className="p-2 text-void-700">{q.lectura}</td>
                    <td className="p-2 text-center text-void-600">{q.intentos}</td>
                    <td className="p-2 text-center text-void-600">{q.porcentaje?.toFixed(0)}%</td>
                    <td className="p-2 text-center text-red-500 font-medium">{q.fallos}</td>
                    <td className="p-2 text-center">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        q.aprobado ? 'bg-teal-50 text-teal-600' : 'bg-red-50 text-red-500'
                      }`}>
                        {q.aprobado ? 'Aprobado' : 'Fallado'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-void-400 text-sm">No has realizado quizzes aún.</p>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color, bg }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
      <div className={`w-9 h-9 ${bg} rounded-xl flex items-center justify-center mb-2`}>
        <FontAwesomeIcon icon={icon} className={color} />
      </div>
      <p className="text-xl font-heading font-bold text-void-800">{value}</p>
      <p className="text-xs text-void-400">{label}</p>
    </div>
  );
}

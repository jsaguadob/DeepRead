import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { stats } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faChartLine, faUsers, faBook, faGraduationCap, faTrophy, faStar, faFire } from '@fortawesome/free-solid-svg-icons';

export default function AdminEstadisticas() {
  const [data, setData] = useState(null);

  useEffect(() => {
    stats.getAdminMetrics()
      .then(res => setData(res.data))
      .catch(() => {});
  }, []);

  if (!data) return <div className="p-8 text-center text-void-400">Cargando...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <Link to="/admin" className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver al Panel
      </Link>

      <div className="flex items-center gap-3 mb-8">
        <FontAwesomeIcon icon={faChartLine} className="text-3xl text-iris-400" />
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">Estadísticas del Sistema</h1>
          <p className="text-void-400">Métricas generales de DeepRead</p>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
          <div className="w-9 h-9 bg-void-50 rounded-xl flex items-center justify-center mb-2">
            <FontAwesomeIcon icon={faUsers} className="text-void-600" />
          </div>
          <p className="text-2xl font-heading font-bold text-void-800">{data.total_usuarios}</p>
          <p className="text-xs text-void-400">Total Usuarios</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
          <div className="w-9 h-9 bg-teal-50 rounded-xl flex items-center justify-center mb-2">
            <FontAwesomeIcon icon={faFire} className="text-teal-600" />
          </div>
          <p className="text-2xl font-heading font-bold text-void-800">{data.usuarios_activos}</p>
          <p className="text-xs text-void-400">Usuarios Activos</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
          <div className="w-9 h-9 bg-flare-50 rounded-xl flex items-center justify-center mb-2">
            <FontAwesomeIcon icon={faBook} className="text-flare-600" />
          </div>
          <p className="text-2xl font-heading font-bold text-void-800">{data.total_lecturas}</p>
          <p className="text-xs text-void-400">Total Lecturas</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
          <div className="w-9 h-9 bg-iris-50 rounded-xl flex items-center justify-center mb-2">
            <FontAwesomeIcon icon={faStar} className="text-iris-500" />
          </div>
          <p className="text-2xl font-heading font-bold text-void-800">{data.lecturas_completadas}</p>
          <p className="text-xs text-void-400">Lecturas Completadas</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* Points & Levels */}
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
          <h3 className="font-heading font-semibold text-void-800 mb-4">Puntos y Niveles</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-void-500">Puntos promedio</span>
              <span className="font-semibold text-void-800">{data.puntos_promedio}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-void-500">Puntos totales sistema</span>
              <span className="font-semibold text-flare-500">{data.puntos_totales_sistema}</span>
            </div>
            <div className="border-t border-frost-200 pt-4">
              <p className="text-sm font-medium text-void-600 mb-3">Distribución por niveles</p>
              <div className="space-y-2">
                {[1, 2, 3].map(n => (
                  <div key={n} className="flex items-center gap-3">
                    <span className="text-sm text-void-400 w-16">Nivel {n}</span>
                    <div className="flex-1 h-2.5 bg-frost-200 rounded-full overflow-hidden">
                      <div className="h-full bg-iris-400 rounded-full"
                        style={{ width: `${data.total_usuarios > 0 ? ((data.niveles?.[n] || 0) / data.total_usuarios * 100) : 0}%` }} />
                    </div>
                    <span className="text-sm font-medium text-void-600 w-10 text-right">{data.niveles?.[n] || 0}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quizzes & Activities */}
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
          <h3 className="font-heading font-semibold text-void-800 mb-4">Quizzes y Actividades</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-void-500">Quizzes realizados</span>
              <span className="font-semibold text-void-800">{data.quices_totales}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-void-500">Quizzes aprobados</span>
              <span className="font-semibold text-teal-500">{data.quices_aprobados}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-void-500">Actividades completadas</span>
              <span className="font-semibold text-iris-500">{data.actividades_completadas}</span>
            </div>
            <div className="border-t border-frost-200 pt-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-void-500">Total respuestas incorrectas</span>
                <span className="font-semibold text-red-500">{data.total_fallos}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Top Students */}
      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
        <h3 className="font-heading font-semibold text-void-800 mb-4 flex items-center gap-2">
          <FontAwesomeIcon icon={faTrophy} className="text-flare-500" /> Top 10 Estudiantes
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-frost-50">
              <tr>
                <th className="p-3 text-left text-sm font-medium text-void-600">#</th>
                <th className="p-3 text-left text-sm font-medium text-void-600">Estudiante</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Puntos</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Nivel</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Lecturas</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Quizzes</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Fallos</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Actividades</th>
              </tr>
            </thead>
            <tbody>
              {data.top_estudiantes?.map((e, i) => (
                <tr key={i} className="border-t border-frost-100 hover:bg-frost-50 transition">
                  <td className="p-3 text-center text-void-400">{i + 1}</td>
                  <td className="p-3 font-medium text-void-700">{e.username}</td>
                  <td className="p-3 text-center font-semibold text-flare-500">{e.puntos}</td>
                  <td className="p-3 text-center">
                    <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-void-50 text-void-600">
                      Nv.{e.nivel}
                    </span>
                  </td>
                  <td className="p-3 text-center text-void-600">{e.completadas}</td>
                  <td className="p-3 text-center text-void-600">{e.quices}</td>
                  <td className="p-3 text-center text-void-600">{e.fallos}</td>
                  <td className="p-3 text-center text-void-600">{e.actividades}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

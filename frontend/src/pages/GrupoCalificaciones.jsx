import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { groups } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faGraduationCap, faStar, faBook, faTrophy, faMedal, faChevronDown, faChevronUp, faTimesCircle, faCheckCircle, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

const medals = [faMedal, faMedal, faMedal];
const medalColors = ['text-flare-500', 'text-gray-400', 'text-amber-600'];

export default function GrupoCalificaciones() {
  const { id } = useParams();
  const [expanded, setExpanded] = useState(null);
  const [data, setData] = useState(null);

  const [error, setError] = useState(null);

  useEffect(() => {
    groups.getGrades(id).then(res => setData(res.data)).catch(err => {
      setError(err.response?.data?.error || 'Error al cargar calificaciones');
    });
  }, [id]);

  if (error) return <div className="p-8 text-center text-red-500 font-medium">{error}</div>;
  if (!data) return <div className="p-8 text-center text-void-400">Cargando...</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <Link to={`/grupos/${id}`} className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver al Grupo
      </Link>

      <div className="flex items-center gap-3 mb-8">
        <FontAwesomeIcon icon={faGraduationCap} className="text-3xl text-iris-400" />
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">Calificaciones</h1>
          <p className="text-void-400">{data.grupo.nombre}</p>
        </div>
      </div>

      <div className="grid sm:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-void-800">{data.estudiantes.length}</p>
          <p className="text-sm text-void-400">Estudiantes</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-flare-500">
            {data.estudiantes.reduce((s, e) => s + e.puntos, 0)}
          </p>
          <p className="text-sm text-void-400">Puntos totales</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-teal-500">
            {data.estudiantes.reduce((s, e) => s + (e.lecturas_completadas || 0), 0)}
          </p>
          <p className="text-sm text-void-400">Lecturas completadas</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-red-500">
            {data.estudiantes.reduce((s, e) => s + (e.quizzes_fallados || 0), 0)}
          </p>
          <p className="text-sm text-void-400">Quizzes fallados</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-frost-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-frost-100">
              <tr>
                <th className="p-3 text-sm font-medium text-void-600 w-10"></th>
                <th className="p-3 text-left text-sm font-medium text-void-600">#</th>
                <th className="p-3 text-left text-sm font-medium text-void-600">Estudiante</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Puntos</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Lect.</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Quiz OK</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Quiz Fall</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Fallos</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Nivel</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Días</th>
              </tr>
            </thead>
            <tbody>
              {data.estudiantes.map((e, i) => {
                const isExpanded = expanded === e.id;
                return (
                  <>
                    <tr key={e.id} className="border-t border-frost-100 hover:bg-frost-50 transition cursor-pointer"
                      onClick={() => setExpanded(isExpanded ? null : e.id)}>
                      <td className="p-3 text-center text-void-300">
                        <FontAwesomeIcon icon={isExpanded ? faChevronUp : faChevronDown} />
                      </td>
                      <td className="p-3 text-center">
                        {i < 3 ? (
                          <FontAwesomeIcon icon={medals[i]} className={medalColors[i]} />
                        ) : (
                          <span className="text-void-400 text-sm">{i + 1}</span>
                        )}
                      </td>
                      <td className="p-3 font-medium text-void-700">{e.username}</td>
                      <td className="p-3 text-center font-semibold text-flare-500">{e.puntos}</td>
                      <td className="p-3 text-center text-void-600">{e.lecturas_completadas}</td>
                      <td className="p-3 text-center text-teal-600 font-medium">{e.quizzes_completados}</td>
                      <td className="p-3 text-center">
                        {(e.quizzes_fallados || 0) > 0 ? (
                          <span className="text-red-500 font-medium">{e.quizzes_fallados}</span>
                        ) : (
                          <span className="text-void-300">0</span>
                        )}
                      </td>
                      <td className="p-3 text-center">
                        {(e.total_fallos || 0) > 0 ? (
                          <span className="text-red-500 font-medium">{e.total_fallos}</span>
                        ) : (
                          <span className="text-void-300">0</span>
                        )}
                      </td>
                      <td className="p-3 text-center">
                        <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-void-50 text-void-600">
                          Nv.{e.nivel}
                        </span>
                      </td>
                      <td className="p-3 text-center text-void-600">{e.dias_activos}</td>
                    </tr>
                    {isExpanded && (
                      <tr key={`${e.id}-detail`}>
                        <td colSpan={10} className="p-0">
                          <div className="bg-void-50 px-6 py-4 border-t border-frost-200">
                            <h4 className="text-sm font-semibold text-void-700 mb-3">Detalle por lectura</h4>
                            {e.lecturas?.length > 0 ? (
                              <div className="space-y-2">
                                {e.lecturas.map((l, li) => (
                                  <div key={li} className="bg-white rounded-xl p-3 border border-frost-200 flex items-center justify-between text-sm">
                                    <div className="flex items-center gap-3 min-w-0">
                                      <span className="text-void-700 font-medium truncate">{l.titulo}</span>
                                      {l.completada_sin_quiz && (
                                        <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-red-50 text-red-500 border border-red-200 whitespace-nowrap">
                                          <FontAwesomeIcon icon={faExclamationTriangle} className="mr-1" />
                                          Sin quiz
                                        </span>
                                      )}
                                    </div>
                                    <div className="flex items-center gap-4 shrink-0">
                                      {l.quiz_aprobado ? (
                                        <span className="text-teal-600 text-xs"><FontAwesomeIcon icon={faCheckCircle} /> Aprobado</span>
                                      ) : l.intentos > 0 ? (
                                        <span className="text-red-400 text-xs"><FontAwesomeIcon icon={faTimesCircle} /> Fallado</span>
                                      ) : (
                                        <span className="text-void-300 text-xs">Sin intentar</span>
                                      )}
                                      <span className="text-void-400 text-xs">{l.intentos} intento(s)</span>
                                      <span className="text-red-400 text-xs">{l.fallos} error(es)</span>
                                      <span className="text-flare-500 font-semibold text-xs">+{l.puntos} pts</span>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-sm text-void-400">Sin actividad</p>
                            )}
                          </div>
                        </td>
                      </tr>
                    )}
                  </>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

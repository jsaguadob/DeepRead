import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { readings, activities } from '../services/api';
import { toast } from '../components/Toast';
import StudentAIChatWidget from '../components/StudentAIChatWidget';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClock, faStar, faArrowLeft, faCheckCircle, faBrain, faGamepad, faPlus, faTrash, faPen, faQuestionCircle, faPuzzlePiece, faSpellCheck, faListCheck, faLock } from '@fortawesome/free-solid-svg-icons';

export default function LecturaDetalle() {
  const { id } = useParams();
  const { user, isAdmin, isProfesor } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [completando, setCompletando] = useState(false);
  const [showActForm, setShowActForm] = useState(false);
  const [actForm, setActForm] = useState({ tipo: 'seleccionar', titulo: '', contenido: '', solucion: '', puntos: 5 });
  const [creandoAct, setCreandoAct] = useState(false);

  useEffect(() => {
    readings.get(id)
      .then(res => setData(res.data))
      .catch(err => {
        toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al cargar lectura' });
        navigate('/lecturas');
      });
  }, [id, navigate]);

  const handleComplete = async () => {
    setCompletando(true);
    try {
      const res = await readings.complete(id);
      toast({ type: res.data.sin_quiz ? 'warning' : 'success', mesteal: res.data.message });
      readings.get(id).then(r => setData(r.data));
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al completar' });
    } finally {
      setCompletando(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('¿Eliminar esta lectura definitivamente?')) return;
    try {
      await readings.delete(id);
      toast({ mesteal: 'Lectura eliminada' });
      navigate('/lecturas');
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al eliminar' });
    }
  };

  const handleCreateActivity = async (e) => {
    e.preventDefault();
    setCreandoAct(true);
    try {
      const payload = { ...actForm, lectura_id: parseInt(id) };
      if (actForm.tipo === 'sopa') {
        payload.contenido = actForm.contenido.toUpperCase();
        payload.solucion = 'sopa';
      }
      await activities.create(payload);
      toast({ mesteal: 'Actividad creada' });
      setShowActForm(false);
      setActForm({ tipo: 'seleccionar', titulo: '', contenido: '', solucion: '', puntos: 5 });
      readings.get(id).then(r => setData(r.data));
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al crear actividad' });
    } finally {
      setCreandoAct(false);
    }
  };

  const actUpdate = (f, v) => setActForm(p => ({ ...p, [f]: v }));

  if (!data) return <div className="p-8 text-center text-void-400">Cargando...</div>;
  const { lectura, progreso, tiene_quiz, quiz_completado, sin_intentos, total_preguntas, actividades } = data;

  if (lectura.cerrada && !isAdmin() && !isProfesor()) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12">
        <Link to="/lecturas" className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
          <FontAwesomeIcon icon={faArrowLeft} /> Volver a Lecturas
        </Link>
        <div className="bg-white rounded-2xl shadow-sm p-8 border border-red-200 text-center">
          <FontAwesomeIcon icon={faLock} className="text-5xl text-red-400 mb-4" />
          <h1 className="text-2xl font-heading font-bold text-void-800 mb-2">Lectura Cerrada</h1>
          <p className="text-void-500 mb-2">Esta lectura se encuentra cerrada y no está disponible en este momento.</p>
          {lectura.fecha_cierre && (
            <p className="text-sm text-void-400">Fecha de cierre: {new Date(lectura.fecha_cierre).toLocaleDateString()}</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <Link to="/lecturas" className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver a Lecturas
      </Link>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-2xl shadow-sm p-8 border border-frost-200">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  lectura.nivel === 1 ? 'bg-teal-50 text-teal-600' :
                  lectura.nivel === 2 ? 'bg-flare-50 text-flare-600' :
                  'bg-iris-50 text-iris-600'
                }`}>
                  Nivel {lectura.nivel}
                </span>
                {lectura.categoria && (
                  <span className="text-sm text-void-400 bg-frost-100 px-3 py-1 rounded-full">
                    {lectura.categoria}
                  </span>
                )}
              </div>
              <span className="text-flare-500 font-semibold flex items-center gap-1">
                <FontAwesomeIcon icon={faStar} /> +{lectura.puntos_recompensa} pts
              </span>
            </div>

            <h1 className="text-3xl font-heading font-bold text-void-800 mb-6">{lectura.titulo}</h1>

            <div className="text-gray-700 leading-relaxed whitespace-pre-line">
              {lectura.contenido}
            </div>

            {/* Complete button */}
            <div className="mt-8 pt-6 border-t border-frost-200">
              {progreso?.completada ? (
                <div className="bg-teal-50 border-2 border-teal-500 rounded-xl p-4 text-center">
                  <FontAwesomeIcon icon={faCheckCircle} className="text-teal-500 text-xl mr-2" />
                  <span className="text-teal-700 font-bold">Lectura completada</span>
                </div>
              ) : tiene_quiz && !quiz_completado && !sin_intentos ? (
                <div className="bg-flare-50 border-2 border-flare-400 rounded-xl p-4 text-center">
                  <p className="text-flare-700 font-bold">Completa el quiz para terminar esta lectura</p>
                </div>
              ) : (() => {
                const puntosFinales = sin_intentos ? Math.max(1, Math.floor(lectura.puntos_recompensa / 5)) : lectura.puntos_recompensa;
                return (
                  <div>
                    {sin_intentos && (
                      <div className="bg-red-50 border-2 border-red-300 rounded-xl p-4 mb-3 text-center">
                        <p className="text-red-700 text-sm font-medium">
                          Agotaste los intentos del quiz. Puedes completar la lectura pero recibirás solo <strong>{puntosFinales} pts</strong> en lugar de {lectura.puntos_recompensa}.
                        </p>
                      </div>
                    )}
                    <button onClick={handleComplete} disabled={completando}
                      className="w-full bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-white py-3 rounded-xl font-medium transition">
                      {completando ? 'Completando...' : 'Marcar como Leída'}
                    </button>
                  </div>
                );
              })()}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 sticky top-4 space-y-6">
            <div>
              <h3 className="font-heading font-semibold text-void-800 mb-3">Información</h3>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-void-400">Tiempo estimado</p>
                  <p className="font-medium text-void-700 flex items-center gap-1">
                    <FontAwesomeIcon icon={faClock} className="text-void-300" /> {lectura.tiempo_estimado_minutos} minutos
                  </p>
                </div>
                <div>
                  <p className="text-void-400">Puntos</p>
                  <p className="font-medium text-flare-500 flex items-center gap-1">
                    <FontAwesomeIcon icon={faStar} /> +{lectura.puntos_recompensa}
                  </p>
                </div>
                <div>
                  <p className="text-void-400">Nivel</p>
                  <p className="font-medium text-void-700">Nivel {lectura.nivel}</p>
                </div>
                <div>
                  <p className="text-void-400">Categoría</p>
                  <p className="font-medium text-void-700 capitalize">{lectura.categoria || 'General'}</p>
                </div>
              </div>
            </div>

            {/* Quiz */}
            {tiene_quiz && !isAdmin() && !isProfesor() && (
              <div className="pt-5 border-t border-frost-200">
                {quiz_completado ? (
                  <p className="text-sm text-teal-600 font-semibold flex items-center gap-1">
                    <FontAwesomeIcon icon={faCheckCircle} /> Quiz completado
                  </p>
                ) : sin_intentos ? (
                  <div className="bg-red-50 border border-red-200 rounded-xl p-3 text-center">
                    <p className="text-sm text-red-600 font-medium">Sin intentos disponibles</p>
                  </div>
                ) : (
                  <>
                    <p className="text-sm text-void-400 mb-3">{total_preguntas} preguntas</p>
                    <Link to={`/lecturas/${id}/quiz`}
                      className="block w-full bg-iris-500 hover:bg-iris-600 text-white py-2.5 rounded-xl text-center font-medium transition">
                      <FontAwesomeIcon icon={faBrain} className="mr-1.5" /> Responder Quiz
                    </Link>
                  </>
                )}
              </div>
            )}

            {/* Activities */}
            {actividades?.length > 0 && (
              <div className="pt-5 border-t border-frost-200">
                <p className="text-sm text-void-400 mb-3">Actividades ({actividades.length})</p>
                <div className="space-y-2">
                  {actividades.map(a => (
                    <Link key={a.id} to={`/actividades/${a.id}`}
                      className="flex items-center gap-2 bg-teal-50 hover:bg-teal-100 text-teal-700 px-3 py-2 rounded-xl text-sm transition">
                      <FontAwesomeIcon icon={faGamepad} />
                      {a.titulo} (+{a.puntos} pts)
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Prof/Admin actions */}
            {(isAdmin() || isProfesor()) && (
              <div className="pt-5 border-t border-frost-200 space-y-2">
                <Link to={`/lecturas/${id}/quiz/manage`}
                  className="flex items-center gap-2 w-full bg-void-50 hover:bg-void-100 text-void-700 py-2.5 px-3 rounded-xl text-sm font-medium transition">
                  <FontAwesomeIcon icon={faQuestionCircle} /> Gestionar Quiz
                </Link>
                <button onClick={() => setShowActForm(!showActForm)}
                  className="flex items-center gap-2 w-full bg-teal-50 hover:bg-teal-100 text-teal-700 py-2.5 px-3 rounded-xl text-sm font-medium transition">
                  <FontAwesomeIcon icon={faPlus} /> {showActForm ? 'Cancelar' : 'Agregar Actividad'}
                </button>
                {showActForm && (
                  <form onSubmit={handleCreateActivity} className="space-y-2 p-3 bg-frost-50 rounded-xl text-sm">
                    <input type="text" placeholder="Título" value={actForm.titulo} onChange={e => actUpdate('titulo', e.target.value)} required
                      className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white" />
                    <select value={actForm.tipo} onChange={e => actUpdate('tipo', e.target.value)}
                      className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white">
                      <option value="seleccionar">Seleccionar</option>
                      <option value="completar">Completar</option>
                      <option value="sopa">Sopa de Letras</option>
                    </select>
                    {actForm.tipo === 'sopa' ? (
                      <input type="text" placeholder="Palabras separadas por coma (ej: SOL,LUNA,MAR)" value={actForm.contenido} onChange={e => actUpdate('contenido', e.target.value)} required
                        className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white" />
                    ) : (
                      <>
                        <textarea placeholder="Contenido de la actividad" value={actForm.contenido} onChange={e => actUpdate('contenido', e.target.value)} required rows={3}
                          className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white" />
                        <input type="text" placeholder="Solución" value={actForm.solucion} onChange={e => actUpdate('solucion', e.target.value)} required
                          className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white" />
                      </>
                    )}
                    <div className="flex items-center gap-2">
                      <input type="number" placeholder="Puntos" value={actForm.puntos} onChange={e => actUpdate('puntos', parseInt(e.target.value))} min={1}
                        className="w-20 px-3 py-2 border border-frost-200 rounded-xl bg-white" />
                      <button type="submit" disabled={creandoAct}
                        className="flex-1 bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-2 rounded-xl font-medium transition">
                        {creandoAct ? 'Creando...' : 'Crear Actividad'}
                      </button>
                    </div>
                  </form>
                )}
                {isAdmin() && (
                  <button onClick={handleDelete}
                    className="flex items-center gap-2 w-full bg-red-50 hover:bg-red-100 text-red-600 py-2.5 px-3 rounded-xl text-sm font-medium transition">
                    <FontAwesomeIcon icon={faTrash} /> Eliminar Lectura
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      {!isAdmin() && !isProfesor() && lectura?.id && <StudentAIChatWidget lecturaId={lectura.id} />}
    </div>
  );
}

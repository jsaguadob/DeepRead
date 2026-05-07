import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { quizzes, ai } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faBrain, faCheckCircle, faTimesCircle, faRobot } from '@fortawesome/free-solid-svg-icons';

export default function Quiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAdmin, isProfesor } = useAuth();
  const [preguntas, setPreguntas] = useState([]);
  const [respuestas, setRespuestas] = useState({});
  const [resultado, setResultado] = useState(null);
  const [detalles, setDetalles] = useState([]);
  const [explicaciones, setExplicaciones] = useState([]);
  const [enviando, setEnviando] = useState(false);
  const [bloqueado, setBloqueado] = useState(false);
  const [cargando, setCargando] = useState(true);
  const [quizInfo, setQuizInfo] = useState({});
  const [explicacionesIA, setExplicacionesIA] = useState({});
  const [explicando, setExplicando] = useState(null);

  useEffect(() => {
    quizzes.getQuestions(id)
      .then(res => {
        if (res.data.bloqueado) {
          setBloqueado(true);
          setQuizInfo({ aprobado: res.data.quiz_aprobado, usados: res.data.intentos_usados, max: res.data.intentos_max });
        } else {
          setPreguntas(res.data.preguntas);
        }
        setCargando(false);
      })
      .catch(() => {
        toast({ type: 'error', mesteal: 'Error al cargar preguntas' });
        navigate(`/lecturas/${id}`);
      });
  }, [id, navigate]);

  useEffect(() => {
    if (isAdmin() || isProfesor()) {
      navigate(`/lecturas/${id}/quiz/manage`);
    }
  }, []);

  useEffect(() => {
    if (bloqueado && !cargando) {
      const msg = quizInfo.aprobado
        ? 'Quiz ya aprobado'
        : `Sin intentos disponibles (${quizInfo.usados}/${quizInfo.max})`;
      toast({ type: 'error', mesteal: msg });
      navigate(`/lecturas/${id}`);
    }
  }, [bloqueado, cargando]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (Object.keys(respuestas).length < preguntas.length) {
      toast({ type: 'error', mesteal: 'Responde todas las preguntas' });
      return;
    }
    setEnviando(true);
    try {
      const res = await quizzes.submitQuiz(id, { respuestas });
      setResultado(res.data.resultado);
      setDetalles(res.data.detalles || []);
      setExplicaciones(res.data.explicaciones || []);
      if (res.data.resultado.aprobado) {
        toast({ mesteal: `¡Aprobado! ${res.data.resultado.porcentaje.toFixed(0)}%` });
      } else {
        toast({ type: 'error', mesteal: `Necesitas 80%. Obtuviste ${res.data.resultado.porcentaje.toFixed(0)}%` });
      }
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al enviar' });
    } finally {
      setEnviando(false);
    }
  };

  if (cargando) {
    return <div className="p-8 text-center text-void-400">Cargando...</div>;
  }

  if (resultado) {
    const d = Object.fromEntries((detalles || []).map(x => [x.pregunta_id, x]));
    const e = Object.fromEntries((explicaciones || []).map(x => [x.id, x]));
    return (
      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl shadow-sm p-8 border border-frost-200 text-center mb-8">
          <div className={`text-6xl mb-4 ${resultado.aprobado ? 'text-teal-500' : 'text-iris-500'}`}>
            <FontAwesomeIcon icon={resultado.aprobado ? faCheckCircle : faTimesCircle} />
          </div>
          <h2 className="text-2xl font-heading font-bold text-void-800 mb-2">
            {resultado.aprobado ? '¡Quiz Aprobado!' : 'Quiz No Aprobado'}
          </h2>
          <p className="text-void-400 mb-4">
            {resultado.correctas} de {resultado.total} correctas — {resultado.porcentaje.toFixed(0)}%
          </p>
          <div className="w-full bg-frost-200 rounded-full h-3 mb-4 max-w-md mx-auto">
            <div className={`h-full rounded-full transition-all ${resultado.aprobado ? 'bg-teal-500' : 'bg-iris-500'}`}
              style={{ width: `${resultado.porcentaje}%` }} />
          </div>
          <p className="text-sm text-void-400">
            +{resultado.puntos} pts | {resultado.intentos_restantes} intentos restantes
          </p>
        </div>

        {!resultado.mostrar_feedback && resultado.intentos_restantes > 0 && (
          <div className="bg-void-50 rounded-2xl p-5 border border-void-200 text-center mb-6">
            <p className="text-void-600 text-sm">
              Tienes <strong>{resultado.intentos_restantes}</strong> intento(s) restante(s).
              Las respuestas correctas se mostrarán cuando se agoten los intentos.
            </p>
          </div>
        )}

        {resultado.mostrar_feedback && detalles.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-lg font-heading font-semibold text-void-800">Detalle por pregunta</h3>
            {preguntas.map((p, i) => {
              const det = d[p.id];
              const exp = e[p.id];
              if (!det) return null;
              return (
                <div key={p.id} className={`rounded-2xl shadow-sm p-5 border ${
                  det.correcta ? 'border-teal-200 bg-teal-50' : 'border-red-200 bg-red-50'
                }`}>
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 text-lg ${det.correcta ? 'text-teal-600' : 'text-red-500'}`}>
                      <FontAwesomeIcon icon={det.correcta ? faCheckCircle : faTimesCircle} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-semibold text-void-800 mb-2">{i + 1}. {p.pregunta}</p>
                      <p className="text-sm text-void-500 mb-1">
                        <span className="font-medium">Tu respuesta:</span> {det.respondida || '(sin respuesta)'}
                      </p>
                      {!det.correcta && (
                        <p className="text-sm text-teal-700 font-medium mb-1">
                          Respuesta correcta: {det.respuesta_correcta}
                        </p>
                      )}
                      {exp?.explicacion && (
                        <p className="text-sm text-void-400 mt-2 italic">{exp.explicacion}</p>
                      )}
                      {!det.correcta && user?.tipo_usuario === 'institucional' && (
                        <div className="mt-2">
                          {explicando === p.id ? (
                            <div className="text-sm text-void-500 animate-pulse">Generando explicación...</div>
                          ) : explicacionesIA[p.id] ? (
                            <div className="mt-1 p-3 bg-white rounded-xl border border-teal-200 text-sm text-void-700">
                              {explicacionesIA[p.id]}
                            </div>
                          ) : (
                            <button onClick={async () => {
                              setExplicando(p.id);
                              try {
                                const res = await ai.explicarPregunta({ pregunta_id: p.id });
                                setExplicacionesIA(prev => ({ ...prev, [p.id]: res.data.respuesta || 'Sin respuesta' }));
                              } catch {
                                setExplicacionesIA(prev => ({ ...prev, [p.id]: 'Error al obtener explicación' }));
                              } finally {
                                setExplicando(null);
                              }
                            }}
                              className="text-xs text-teal-600 hover:text-teal-700 font-medium underline flex items-center gap-1">
                              <FontAwesomeIcon icon={faRobot} /> Explicar con IA
                            </button>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

          {resultado.puede_completar_sin_quiz && (
            <div className="bg-void-50 rounded-2xl p-4 border border-void-200 mb-4">
              <p className="text-sm text-void-600">
                Agotaste todos los intentos. Aún puedes marcar la lectura como completada,
                pero <strong>no recibirás los puntos completos</strong> por no haber aprobado el quiz.
              </p>
              <Link to={`/lecturas/${id}`}
                className="inline-block mt-2 text-sm text-iris-600 hover:text-iris-700 font-medium underline">
                Ir a la lectura para completarla
              </Link>
            </div>
          )}

          <div className="flex gap-3 justify-center mt-4">
          {!resultado.aprobado && resultado.intentos_restantes > 0 && (
            <button onClick={() => { setResultado(null); setDetalles([]); setExplicaciones([]); }}
              className="bg-iris-500 hover:bg-iris-600 text-white px-6 py-2.5 rounded-xl font-medium transition">
              Intentar de nuevo
            </button>
          )}
          <Link to={`/lecturas/${id}`}
            className="bg-void-100 hover:bg-void-200 text-void-700 px-6 py-2.5 rounded-xl font-medium transition">
            Volver a la lectura
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link to={`/lecturas/${id}`} className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver
      </Link>

      <div className="flex items-center gap-3 mb-8">
        <FontAwesomeIcon icon={faBrain} className="text-2xl text-iris-400" />
        <div>
          <h1 className="text-2xl font-heading font-bold text-void-800">Quiz de Comprensión</h1>
          <p className="text-sm text-void-400">{preguntas.length} preguntas — 80% para aprobar</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {preguntas.map((p, i) => (
          <div key={p.id} className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
            <h3 className="font-semibold text-void-800 mb-4">{i + 1}. {p.pregunta}</h3>
            <div className="space-y-2">
              {['a', 'b', 'c', 'd'].map(letra => (
                <label key={letra}
                  className={`flex items-center gap-3 p-3 rounded-xl border-2 cursor-pointer transition ${
                    respuestas[`pregunta_${p.id}`] === letra
                      ? 'border-iris-400 bg-iris-50'
                      : 'border-frost-200 hover:border-void-200'
                  }`}>
                  <input type="radio" name={`pregunta_${p.id}`} value={letra}
                    checked={respuestas[`pregunta_${p.id}`] === letra}
                    onChange={e => setRespuestas(r => ({ ...r, [`pregunta_${p.id}`]: e.target.value }))}
                    className="accent-iris-500" />
                  <span className="font-medium text-void-600">{letra.toUpperCase()}.</span>
                  <span>{p[`opcion_${letra}`]}</span>
                </label>
              ))}
            </div>
          </div>
        ))}

        <button type="submit" disabled={enviando || preguntas.length === 0}
          className="w-full bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold text-lg transition shadow-lg shadow-iris-500/25">
          {enviando ? 'Enviando...' : 'Enviar Respuestas'}
        </button>
      </form>
    </div>
  );
}

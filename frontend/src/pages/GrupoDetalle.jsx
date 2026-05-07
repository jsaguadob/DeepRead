import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { groups, readings } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faUsers, faBook, faGraduationCap, faPlus, faTimes, faLink, faChartBar, faQuestionCircle, faLock, faLockOpen } from '@fortawesome/free-solid-svg-icons';

export default function GrupoDetalle() {
  const { id } = useParams();
  const { user, isAdmin } = useAuth();
  const [grupo, setGrupo] = useState(null);
  const [miembros, setMiembros] = useState([]);
  const [lecturas, setLecturas] = useState([]);
  const [esDueno, setEsDueno] = useState(false);
  const [showCreateLectura, setShowCreateLectura] = useState(false);
  const [form, setForm] = useState({ titulo: '', contenido: '', nivel: 1, tiempo_estimado_minutos: 10, puntos_recompensa: 100, categoria: '', intentos_maximos: 3, fecha_cierre: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    groups.get(id)
      .then(res => {
        setGrupo(res.data.grupo);
        setMiembros(res.data.miembros);
        setLecturas(res.data.lecturas);
        setEsDueno(res.data.es_dueno);
      })
      .catch(() => {
        toast({ type: 'error', mesteal: 'Grupo no encontrado' });
      });
  }, [id]);

  const handleCreateLectura = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Create reading via API with grupo_id = current group
      const payload = { ...form, grupo_id: parseInt(id), es_publica: false };
      if (!payload.fecha_cierre) delete payload.fecha_cierre;
      await readings.create(payload);
      toast({ mesteal: 'Lectura creada en el grupo' });
      setShowCreateLectura(false);
      setForm({ titulo: '', contenido: '', nivel: 1, tiempo_estimado_minutos: 10, puntos_recompensa: 100, categoria: '', intentos_maximos: 3, fecha_cierre: '' });
      groups.get(id).then(r => setLecturas(r.data.lecturas));
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al crear' });
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMiris = async (userId) => {
    if (!confirm('¿Eliminar este miembro?')) return;
    try {
      await groups.removeMiris(id, userId);
      toast({ mesteal: 'Miembro eliminado' });
      groups.get(id).then(r => setMiembros(r.data.miembros));
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al eliminar' });
    }
  };

  const handleToggleCierre = async (lecturaId, accion) => {
    try {
      const res = await groups.toggleLecture(id, lecturaId, { accion });
      toast({ mesteal: res.data.message });
      groups.get(id).then(r => setLecturas(r.data.lecturas));
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al cambiar estado' });
    }
  };

  if (!grupo) return <div className="p-8 text-center text-void-400">Cargando...</div>;

  const update = (f, v) => setForm(p => ({ ...p, [f]: v }));

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <Link to="/grupos" className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver a Grupos
      </Link>

      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <FontAwesomeIcon icon={faUsers} className="text-3xl text-iris-400" />
          <div>
            <h1 className="text-3xl font-heading font-bold text-void-800">{grupo.nombre}</h1>
            <p className="text-void-400">{grupo.descripcion || ''}</p>
          </div>
        </div>
        <div className="bg-frost-100 p-3 rounded-xl text-center">
          <p className="text-xs text-void-400">Código</p>
          <p className="text-xl font-bold text-iris-500">{grupo.codigo_unico}</p>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Lecturas */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-heading font-semibold text-void-800 flex items-center gap-2">
                <FontAwesomeIcon icon={faBook} className="text-teal-500" /> Lecturas ({lecturas.length})
              </h2>
              {esDueno && (
                <button onClick={() => setShowCreateLectura(!showCreateLectura)}
                  className="text-sm bg-iris-500 hover:bg-iris-600 text-white px-3 py-1.5 rounded-lg transition flex items-center gap-1">
                  <FontAwesomeIcon icon={faPlus} /> {showCreateLectura ? 'Cancelar' : 'Nueva'}
                </button>
              )}
            </div>

            {showCreateLectura && (
              <form onSubmit={handleCreateLectura} className="mb-6 p-4 bg-frost-50 rounded-xl space-y-3">
                <input type="text" placeholder="Título" value={form.titulo} onChange={e => update('titulo', e.target.value)} required
                  className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm" />
                <textarea placeholder="Contenido" value={form.contenido} onChange={e => update('contenido', e.target.value)} required rows={4}
                  className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm" />
                <div className="grid grid-cols-4 gap-2">
                  <select value={form.nivel} onChange={e => update('nivel', parseInt(e.target.value))}
                    className="px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm">
                    {[1,2,3].map(n => <option key={n} value={n}>Nv.{n}</option>)}
                  </select>
                  <input type="number" placeholder="Min" value={form.tiempo_estimado_minutos} onChange={e => update('tiempo_estimado_minutos', parseInt(e.target.value))}
                    className="px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm" />
                  <input type="number" placeholder="Pts" value={form.puntos_recompensa} onChange={e => update('puntos_recompensa', parseInt(e.target.value))}
                    className="px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm" />
                  <input type="datetime-local" value={form.fecha_cierre} onChange={e => update('fecha_cierre', e.target.value)}
                    className="px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm" />
                  <select value={form.categoria} onChange={e => update('categoria', e.target.value)}
                    className="px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm">
                    <option value="">Cat.</option>
                    <option value="ciencia">Ciencia</option>
                    <option value="historia">Historia</option>
                    <option value="literatura">Literatura</option>
                  </select>
                </div>
                <button type="submit" disabled={loading}
                  className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-4 py-2 rounded-xl text-sm font-medium transition">
                  {loading ? 'Creando...' : 'Crear Lectura'}
                </button>
              </form>
            )}

            {lecturas.length === 0 ? (
              <p className="text-void-400 text-sm">No hay lecturas en este grupo</p>
            ) : (
              <div className="space-y-3">
                {lecturas.map(l => (
                  <div key={l.id} className="flex items-center justify-between p-3 bg-frost-50 rounded-xl">
                    <Link to={`/lecturas/${l.id}`} className="flex-1 hover:text-iris-500 transition">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-void-800">{l.titulo}</p>
                        {l.cerrada && (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-red-100 text-red-600">
                            <FontAwesomeIcon icon={faLock} className="mr-0.5" />Cerrada
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-void-400">
                        Nv.{l.nivel} · {l.tiempo_estimado_minutos} min · +{l.puntos_recompensa} pts
                        {l.fecha_cierre && ` · Cierra: ${new Date(l.fecha_cierre).toLocaleDateString()}`}
                      </p>
                    </Link>
                    <div className="flex gap-1">
                      {esDueno && (
                        <>
                          <button onClick={() => handleToggleCierre(l.id, l.cerrada ? 'reabrir' : 'cerrar')}
                            className={`p-1.5 rounded-lg transition ${l.cerrada ? 'text-teal-500 hover:bg-teal-50' : 'text-red-400 hover:bg-red-50'}`}
                            title={l.cerrada ? 'Reabrir' : 'Cerrar'}>
                            <FontAwesomeIcon icon={l.cerrada ? faLockOpen : faLock} />
                          </button>
                          <Link to={`/lecturas/${l.id}/quiz/manage`}
                            className="text-void-400 hover:text-void-600 p-1.5 hover:bg-frost-200 rounded-lg transition"
                            title="Gestionar Quiz">
                            <FontAwesomeIcon icon={faQuestionCircle} />
                          </Link>
                        </>
                      )}
                      <Link to={`/grupos/${id}/calificaciones`}
                        className="text-void-400 hover:text-void-600 p-1.5 hover:bg-frost-200 rounded-lg transition"
                        title="Ver calificaciones">
                        <FontAwesomeIcon icon={faChartBar} />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {esDueno && (
            <Link to={`/grupos/${id}/calificaciones`}
              className="block bg-white rounded-2xl shadow-sm p-6 border border-frost-200 card-hover">
              <div className="flex items-center gap-3">
                <FontAwesomeIcon icon={faGraduationCap} className="text-2xl text-teal-500" />
                <div>
                  <h3 className="font-heading font-semibold text-void-800">Calificaciones</h3>
                  <p className="text-sm text-void-400">Ver ranking y progreso de estudiantes</p>
                </div>
              </div>
            </Link>
          )}
        </div>

        {/* Miembros */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 sticky top-4">
            <h2 className="text-xl font-heading font-semibold text-void-800 mb-4 flex items-center gap-2">
              <FontAwesomeIcon icon={faUsers} className="text-iris-400" /> Miembros ({miembros.length})
            </h2>
            <div className="space-y-3">
              {miembros.map(m => (
                <div key={m.id} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-void-700 text-sm">{m.username}</p>
                    <p className="text-xs text-void-400">{m.email}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      m.rol === 'profesor' ? 'bg-void-50 text-void-600' : 'bg-teal-50 text-teal-600'
                    }`}>{m.rol}</span>
                    {esDueno && m.rol !== 'profesor' && (
                      <button onClick={() => handleRemoveMiris(m.id)}
                        className="text-red-400 hover:text-red-600 text-xs p-1 hover:bg-red-50 rounded transition">
                        <FontAwesomeIcon icon={faTimes} />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-frost-200">
              <p className="text-xs text-void-400 flex items-center gap-1">
                <FontAwesomeIcon icon={faLink} /> Código: <strong className="text-iris-500">{grupo.codigo_unico}</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

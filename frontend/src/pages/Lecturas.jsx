import { useState, useEffect, useCallback } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { readings, groups } from '../services/api';
import { toast } from '../components/Toast';
import FileImportModal from '../components/FileImportModal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook, faClock, faStar, faFilter, faPlus, faSearch, faCheckCircle, faFileUpload } from '@fortawesome/free-solid-svg-icons';

export default function Lecturas() {
  const { user, isAdmin, isProfesor } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [lecturas, setLecturas] = useState([]);
  const [showImport, setShowImport] = useState(false);
  const [categorias, setCategorias] = useState([]);
  const [filtroNivel, setFiltroNivel] = useState('');
  const [filtroCat, setFiltroCat] = useState('');
  const [showCreate, setShowCreate] = useState(searchParams.get('crear') === 'true');
  const [form, setForm] = useState({ titulo: '', contenido: '', nivel: 1, tiempo_estimado_minutos: 10, puntos_recompensa: 100, categoria: '', intentos_maximos: 3, grupo_id: '' });
  const [loading, setLoading] = useState(false);
  const [creando, setCreando] = useState(false);
  const [misGrupos, setMisGrupos] = useState([]);

  const load = useCallback(() => {
    setLoading(true);
    readings.list({ nivel: filtroNivel || undefined, categoria: filtroCat || undefined })
      .then(res => {
        setLecturas(res.data.lecturas);
        setCategorias(res.data.categorias);
      })
      .catch(() => toast({ type: 'error', mesteal: 'Error al cargar lecturas' }))
      .finally(() => setLoading(false));
  }, [filtroNivel, filtroCat]);

  useEffect(() => { load(); }, [load]);

  useEffect(() => {
    if (isProfesor() && !isAdmin()) {
      groups.list().then(res => setMisGrupos(res.data.grupos || [])).catch(() => {});
    }
  }, [isProfesor, isAdmin]);

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreando(true);
    try {
      const payload = { ...form, grupo_id: form.grupo_id ? parseInt(form.grupo_id) : undefined };
      await readings.create(payload);
      toast({ mesteal: 'Lectura creada exitosamente' });
      setShowCreate(false);
      load();
      setForm({ titulo: '', contenido: '', nivel: 1, tiempo_estimado_minutos: 10, puntos_recompensa: 100, categoria: '', intentos_maximos: 3, grupo_id: '' });
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al crear' });
    } finally {
      setCreando(false);
    }
  };

  const update = (f, v) => setForm(p => ({ ...p, [f]: v }));

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">Lecturas</h1>
          <p className="text-void-400 mt-1">Explora y mejora tu comprensión lectora</p>
        </div>
        {(isAdmin() || isProfesor()) && (
          <div className="flex gap-2">
            <button onClick={() => setShowImport(true)}
              className="bg-teal-500 hover:bg-teal-600 text-white px-5 py-2.5 rounded-xl font-medium transition shadow-lg shadow-teal-500/25 flex items-center gap-2">
              <FontAwesomeIcon icon={faFileUpload} /> Importar Archivo
            </button>
            <button onClick={() => setShowCreate(!showCreate)}
              className="bg-iris-500 hover:bg-iris-600 text-white px-5 py-2.5 rounded-xl font-medium transition shadow-lg shadow-iris-500/25 flex items-center gap-2">
              <FontAwesomeIcon icon={faPlus} /> {showCreate ? 'Cancelar' : 'Nueva Lectura'}
            </button>
          </div>
        )}
      </div>

      {/* Create form */}
      {showCreate && (
        <div className="bg-white rounded-2xl shadow-sm p-6 mb-8 border border-frost-200">
          <h2 className="text-lg font-heading font-semibold text-void-800 mb-4">Crear Nueva Lectura</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Título</label>
                <input type="text" value={form.titulo} onChange={e => update('titulo', e.target.value)} required
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
              </div>
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Categoría</label>
                <select value={form.categoria} onChange={e => update('categoria', e.target.value)}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50">
                  <option value="">Seleccionar</option>
                  <option value="ciencia">Ciencia</option>
                  <option value="historia">Historia</option>
                  <option value="literatura">Literatura</option>
                  <option value="tecnologia">Tecnología</option>
                  <option value="arte">Arte</option>
                  <option value="filosofia">Filosofía</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-void-600 mb-1">Contenido</label>
              <textarea value={form.contenido} onChange={e => update('contenido', e.target.value)} required rows={6}
                className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
            </div>
            {isProfesor() && !isAdmin() && (
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Grupo <span className="text-red-500">*</span></label>
                <select value={form.grupo_id} onChange={e => update('grupo_id', parseInt(e.target.value) || '')} required
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50">
                  <option value="">Seleccionar grupo</option>
                  {misGrupos.filter(g => g.es_dueno).map(g => (
                    <option key={g.id} value={g.id}>{g.nombre}</option>
                  ))}
                </select>
              </div>
            )}
            <div className="grid sm:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Nivel</label>
                <select value={form.nivel} onChange={e => update('nivel', parseInt(e.target.value))}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50">
                  {[1,2,3].map(n => <option key={n} value={n}>Nivel {n}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Tiempo (min)</label>
                <input type="number" value={form.tiempo_estimado_minutos} onChange={e => update('tiempo_estimado_minutos', parseInt(e.target.value))} required min={1}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
              </div>
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Puntos</label>
                <input type="number" value={form.puntos_recompensa} onChange={e => update('puntos_recompensa', parseInt(e.target.value))} required min={0}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
              </div>
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Intentos Quiz</label>
                <input type="number" value={form.intentos_maximos} onChange={e => update('intentos_maximos', parseInt(e.target.value))} required min={1} max={10}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
              </div>
            </div>
            <button type="submit" disabled={creando}
              className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-medium transition">
              {creando ? 'Creando...' : 'Crear Lectura'}
            </button>
          </form>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <select value={filtroNivel} onChange={e => setFiltroNivel(e.target.value)}
          className="px-4 py-2 border border-frost-200 rounded-xl bg-white text-void-600 text-sm focus:outline-none focus:ring-2 focus:ring-iris-400/50">
          <option value="">Todos los niveles</option>
          <option value="1">Nivel 1</option>
          <option value="2">Nivel 2</option>
          <option value="3">Nivel 3</option>
        </select>
        <select value={filtroCat} onChange={e => setFiltroCat(e.target.value)}
          className="px-4 py-2 border border-frost-200 rounded-xl bg-white text-void-600 text-sm focus:outline-none focus:ring-2 focus:ring-iris-400/50">
          <option value="">Todas las categorías</option>
          {categorias.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <button onClick={() => { setFiltroNivel(''); setFiltroCat(''); }}
          className="px-4 py-2 text-void-400 hover:text-void-600 text-sm transition">
          <FontAwesomeIcon icon={faFilter} /> Limpiar
        </button>
      </div>

      {/* Cards */}
      {loading ? (
        <p className="text-center text-void-400 py-12">Cargando lecturas...</p>
      ) : lecturas.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-2xl border border-frost-200">
          <FontAwesomeIcon icon={faBook} className="text-4xl text-void-300 mb-3" />
          <p className="text-void-400">No hay lecturas disponibles</p>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {lecturas.map(l => (
            <Link key={l.id} to={`/lecturas/${l.id}`}
              className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 card-hover block">
              <div className="flex items-start justify-between mb-3">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                  l.nivel === 1 ? 'bg-teal-50 text-teal-600' :
                  l.nivel === 2 ? 'bg-flare-50 text-flare-600' :
                  'bg-iris-50 text-iris-600'
                }`}>
                  Nivel {l.nivel}
                </span>
                <div className="flex items-center gap-1">
                  {l.cerrada && <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-100 text-red-600 font-medium"><FontAwesomeIcon icon={faLock} /> Cerrada</span>}
                  {l.completada && <FontAwesomeIcon icon={faCheckCircle} className="text-teal-500" />}
                </div>
              </div>
              <h3 className="text-lg font-heading font-semibold text-void-800 mb-2">{l.titulo}</h3>
              {l.categoria && (
                <span className="text-xs text-void-400 bg-frost-100 px-2 py-0.5 rounded-full">{l.categoria}</span>
              )}
              <div className="flex items-center gap-4 mt-4 text-sm text-void-400">
                <span className="flex items-center gap-1"><FontAwesomeIcon icon={faClock} /> {l.tiempo_estimado_minutos} min</span>
                <span className="flex items-center gap-1"><FontAwesomeIcon icon={faStar} className="text-flare-500" /> +{l.puntos_recompensa} pts</span>
              </div>
            </Link>
          ))}
        </div>
      )}
      {showImport && (
        <FileImportModal
          onClose={() => setShowImport(false)}
          onCreated={(lectura) => navigate(`/lecturas/${lectura.id}`)}
          misGrupos={misGrupos}
        />
      )}
    </div>
  );
}

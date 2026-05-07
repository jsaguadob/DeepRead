import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { groups } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUsers, faPlus, faLink, faArrowRight, faUserPlus } from '@fortawesome/free-solid-svg-icons';

export default function Grupos() {
  const { user, isAdmin, isProfesor } = useAuth();
  const [grupos, setGrupos] = useState([]);
  const [gruposCreados, setGruposCreados] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [showJoin, setShowJoin] = useState(false);
  const [form, setForm] = useState({ nombre: '', descripcion: '' });
  const [codigo, setCodigo] = useState('');
  const [loading, setLoading] = useState(false);

  const load = () => {
    groups.list()
      .then(res => {
        setGrupos(res.data.grupos);
        setGruposCreados(res.data.grupos_creados);
      })
      .catch(() => {});
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await groups.create(form);
      toast({ mesteal: `Grupo creado! Código: ${res.data.codigo}` });
      setShowCreate(false);
      setForm({ nombre: '', descripcion: '' });
      load();
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al crear' });
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async (e) => {
    e.preventDefault();
    if (!codigo.trim()) return;
    setLoading(true);
    try {
      const res = await groups.join(codigo.trim());
      toast({ mesteal: res.data.mesteal });
      setShowJoin(false);
      setCodigo('');
      load();
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Código inválido' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <FontAwesomeIcon icon={faUsers} className="text-3xl text-iris-400" />
          <div>
            <h1 className="text-3xl font-heading font-bold text-void-800">Mis Grupos</h1>
            <p className="text-void-400">Aprende en equipo</p>
          </div>
        </div>
        <div className="flex gap-3">
          <button onClick={() => setShowJoin(!showJoin)}
            className="bg-white border-2 border-frost-200 hover:border-void-200 text-void-600 px-4 py-2.5 rounded-xl font-medium transition flex items-center gap-2">
            <FontAwesomeIcon icon={faLink} /> Unirse
          </button>
          {(isAdmin() || isProfesor()) && (
            <button onClick={() => setShowCreate(!showCreate)}
              className="bg-iris-500 hover:bg-iris-600 text-white px-4 py-2.5 rounded-xl font-medium transition flex items-center gap-2">
              <FontAwesomeIcon icon={faPlus} /> Crear Grupo
            </button>
          )}
        </div>
      </div>

      {showCreate && (
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mb-6">
          <h2 className="font-heading font-semibold text-void-800 mb-4">Crear Nuevo Grupo</h2>
          <form onSubmit={handleCreate} className="space-y-4 max-w-md">
            <input type="text" placeholder="Nombre del grupo" value={form.nombre}
              onChange={e => setForm(p => ({ ...p, nombre: e.target.value }))} required
              className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
            <textarea placeholder="Descripción (opcional)" value={form.descripcion}
              onChange={e => setForm(p => ({ ...p, descripcion: e.target.value }))} rows={2}
              className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
            <button type="submit" disabled={loading}
              className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-medium transition">
              {loading ? 'Creando...' : 'Crear Grupo'}
            </button>
          </form>
        </div>
      )}

      {showJoin && (
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mb-6">
          <h2 className="font-heading font-semibold text-void-800 mb-4">Unirse a un Grupo</h2>
          <form onSubmit={handleJoin} className="flex gap-3 max-w-md">
            <input type="text" placeholder="Código del grupo" value={codigo}
              onChange={e => setCodigo(e.target.value.toUpperCase())} required
              className="flex-1 px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50 uppercase" />
            <button type="submit" disabled={loading}
              className="bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-medium transition">
              <FontAwesomeIcon icon={faUserPlus} />
            </button>
          </form>
        </div>
      )}

      {gruposCreados.length > 0 && (
        <>
          <h2 className="text-xl font-heading font-semibold text-void-800 mb-4">Grupos que creé</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {gruposCreados.map(g => (
              <div key={g.id} className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
                <h3 className="text-lg font-heading font-semibold text-void-800">{g.nombre}</h3>
                <p className="text-sm text-void-400 mb-2">{g.descripcion || 'Sin descripción'}</p>
                <div className="bg-frost-100 p-2 rounded-xl mb-3">
                  <p className="text-xs text-void-400">Código:</p>
                  <p className="text-lg font-bold text-iris-500">{g.codigo_unico}</p>
                </div>
                <Link to={`/grupos/${g.id}`}
                  className="block w-full bg-void-600 hover:bg-void-700 text-white text-center py-2 rounded-xl text-sm font-medium transition">
                  Entrar al Grupo
                </Link>
              </div>
            ))}
          </div>
        </>
      )}

      {grupos.length > 0 && (
        <>
          <h2 className="text-xl font-heading font-semibold text-void-800 mb-4">Grupos a los que pertenezco</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {grupos.map(g => (
              <div key={g.id} className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="text-lg font-heading font-semibold text-void-800">{g.nombre}</h3>
                    <p className="text-sm text-void-400">{g.descripcion || 'Sin descripción'}</p>
                  </div>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    g.rol === 'profesor' ? 'bg-void-50 text-void-600' : 'bg-teal-50 text-teal-600'
                  }`}>{g.rol}</span>
                </div>
                <Link to={`/grupos/${g.id}`}
                  className="block w-full bg-iris-500/10 hover:bg-iris-500/20 text-iris-600 text-center py-2 rounded-xl text-sm font-medium transition">
                  Entrar al Grupo <FontAwesomeIcon icon={faArrowRight} className="ml-1" />
                </Link>
              </div>
            ))}
          </div>
        </>
      )}

      {grupos.length === 0 && gruposCreados.length === 0 && (
        <div className="text-center py-12 bg-white rounded-2xl border border-frost-200">
          <FontAwesomeIcon icon={faUsers} className="text-4xl text-void-300 mb-3" />
          <p className="text-void-400 mb-4">No perteneces a ningún grupo</p>
          <button onClick={() => setShowJoin(true)}
            className="text-iris-500 hover:text-iris-600 font-medium">
            Unirse a un grupo
          </button>
        </div>
      )}
    </div>
  );
}

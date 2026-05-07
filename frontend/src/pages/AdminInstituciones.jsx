import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { institutions } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faBuilding, faPlus, faToggleOn, faToggleOff, faTrash } from '@fortawesome/free-solid-svg-icons';

export default function AdminInstituciones() {
  const [lista, setLista] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [nombre, setNombre] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    institutions.list()
      .then(res => setLista(res.data.instituciones))
      .catch(() => toast({ type: 'error', mesteal: 'Error al cargar' }));
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!nombre.trim()) return;
    setLoading(true);
    try {
      const res = await institutions.create({ nombre: nombre.trim() });
      toast({ mesteal: `Institución creada. Código: ${res.data.institucion.codigo}` });
      setNombre('');
      setShowCreate(false);
      institutions.list().then(r => setLista(r.data.instituciones));
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al crear' });
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (inst) => {
    try {
      await institutions.update(inst.id, { activa: !inst.activa });
      toast({ mesteal: inst.activa ? 'Institución desactivada' : 'Institución activada' });
      institutions.list().then(r => setLista(r.data.instituciones));
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al actualizar' });
    }
  };

  const handleDelete = async (id, nombre) => {
    if (!confirm(`¿Desactivar "${nombre}"?`)) return;
    try {
      await institutions.delete(id);
      toast({ mesteal: 'Institución desactivada' });
      institutions.list().then(r => setLista(r.data.instituciones));
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error' });
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <Link to="/admin" className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver al Panel
      </Link>

      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <FontAwesomeIcon icon={faBuilding} className="text-3xl text-iris-400" />
          <div>
            <h1 className="text-3xl font-heading font-bold text-void-800">Instituciones</h1>
            <p className="text-void-400">Gestiona las instituciones educativas registradas</p>
          </div>
        </div>
        <button onClick={() => setShowCreate(!showCreate)}
          className="bg-iris-500 hover:bg-iris-600 text-white px-4 py-2.5 rounded-xl font-medium transition flex items-center gap-2">
          <FontAwesomeIcon icon={faPlus} /> {showCreate ? 'Cancelar' : 'Nueva'}
        </button>
      </div>

      {showCreate && (
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mb-6">
          <form onSubmit={handleCreate} className="flex gap-3 max-w-md">
            <input type="text" placeholder="Nombre de la institución" value={nombre}
              onChange={e => setNombre(e.target.value)} required
              className="flex-1 px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
            <button type="submit" disabled={loading}
              className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-medium transition">
              {loading ? 'Creando...' : 'Crear'}
            </button>
          </form>
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-sm border border-frost-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-frost-50">
              <tr>
                <th className="p-3 text-left text-sm font-medium text-void-600">Nombre</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Código</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Estado</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Creada</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {lista.map(i => (
                <tr key={i.id} className="border-t border-frost-100 hover:bg-frost-50 transition">
                  <td className="p-3 font-medium text-void-700">{i.nombre}</td>
                  <td className="p-3 text-center font-mono text-sm text-iris-500 font-bold">{i.codigo}</td>
                  <td className="p-3 text-center">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      i.activa ? 'bg-teal-50 text-teal-600' : 'bg-red-50 text-red-500'
                    }`}>{i.activa ? 'Activa' : 'Inactiva'}</span>
                  </td>
                  <td className="p-3 text-center text-sm text-void-400">
                    {i.fecha_creacion ? new Date(i.fecha_creacion).toLocaleDateString() : '-'}
                  </td>
                  <td className="p-3 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <button onClick={() => handleToggle(i)}
                        className={`p-1.5 rounded-lg transition ${i.activa ? 'text-teal-500 hover:bg-teal-50' : 'text-void-300 hover:bg-frost-100'}`}
                        title={i.activa ? 'Desactivar' : 'Activar'}>
                        <FontAwesomeIcon icon={i.activa ? faToggleOn : faToggleOff} />
                      </button>
                      <button onClick={() => handleDelete(i.id, i.nombre)}
                        className="text-red-400 hover:text-red-600 p-1.5 hover:bg-red-50 rounded-lg transition"
                        title="Desactivar">
                        <FontAwesomeIcon icon={faTrash} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {lista.length === 0 && (
          <div className="text-center py-12">
            <FontAwesomeIcon icon={faBuilding} className="text-3xl text-void-300 mb-2" />
            <p className="text-void-400">No hay instituciones registradas</p>
          </div>
        )}
      </div>
    </div>
  );
}

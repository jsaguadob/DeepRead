import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { users } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCrown, faUsers, faGraduationCap, faBook, faChartLine, faBuilding, faSave, faTrash } from '@fortawesome/free-solid-svg-icons';

export default function AdminPanel() {
  const [usuarios, setUsuarios] = useState([]);
  const [stats, setStats] = useState({});
  const [editando, setEditando] = useState(null);
  const [rolForm, setRolForm] = useState({ rol: '', tipo_usuario: '' });

  useEffect(() => {
    users.list()
      .then(res => {
        setUsuarios(res.data.usuarios);
        setStats(res.data.stats);
      })
      .catch(() => toast({ type: 'error', mesteal: 'Error al cargar usuarios' }));
  }, []);

  const handleUpdate = async (userId) => {
    try {
      await users.update(userId, rolForm);
      toast({ mesteal: 'Usuario actualizado' });
      setEditando(null);
      users.list().then(res => setUsuarios(res.data.usuarios));
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al actualizar' });
    }
  };

  const handleDelete = async (userId, username) => {
    if (!confirm(`¿Eliminar a "${username}" permanentemente?`)) return;
    try {
      await users.delete(userId);
      toast({ mesteal: 'Usuario eliminado' });
      users.list().then(res => setUsuarios(res.data.usuarios));
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al eliminar' });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center gap-3 mb-8">
        <FontAwesomeIcon icon={faCrown} className="text-3xl text-flare-500" />
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">Panel de Administración</h1>
          <p className="text-void-400">Gestión de usuarios y sistema</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid sm:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-void-800">{stats.total_estudiantes || 0}</p>
          <p className="text-sm text-void-400"><FontAwesomeIcon icon={faUsers} /> Estudiantes</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-void-800">{stats.total_profesores || 0}</p>
          <p className="text-sm text-void-400"><FontAwesomeIcon icon={faGraduationCap} /> Profesores</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-teal-500">{stats.usuarios_activos || 0}</p>
          <p className="text-sm text-void-400">Activos</p>
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 text-center">
          <p className="text-2xl font-heading font-bold text-flare-500">{stats.lecturas_completadas || 0}</p>
          <p className="text-sm text-void-400"><FontAwesomeIcon icon={faBook} /> Completadas</p>
        </div>
      </div>

      {/* Quick links */}
      <div className="grid sm:grid-cols-2 gap-4 mb-8">
        <Link to="/admin/instituciones"
          className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 card-hover flex items-center gap-3">
          <FontAwesomeIcon icon={faBuilding} className="text-2xl text-iris-400" />
          <div>
            <h3 className="font-heading font-semibold text-void-800">Instituciones</h3>
            <p className="text-sm text-void-400">Gestionar instituciones educativas</p>
          </div>
        </Link>
        <Link to="/admin/estadisticas"
          className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200 card-hover flex items-center gap-3">
          <FontAwesomeIcon icon={faChartLine} className="text-2xl text-teal-500" />
          <div>
            <h3 className="font-heading font-semibold text-void-800">Estadísticas</h3>
            <p className="text-sm text-void-400">Métricas del sistema</p>
          </div>
        </Link>
      </div>

      {/* Users table */}
      <div className="bg-white rounded-2xl shadow-sm border border-frost-200 overflow-hidden">
        <div className="p-5 border-b border-frost-200">
          <h2 className="text-xl font-heading font-semibold text-void-800">Usuarios ({usuarios.length})</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-frost-50">
              <tr>
                <th className="p-3 text-left text-sm font-medium text-void-600">Usuario</th>
                <th className="p-3 text-left text-sm font-medium text-void-600">Email</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Rol</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Tipo</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Puntos</th>
                <th className="p-3 text-center text-sm font-medium text-void-600">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map(u => (
                <tr key={u.id} className="border-t border-frost-100 hover:bg-frost-50 transition">
                  <td className="p-3 font-medium text-void-700">{u.username}</td>
                  <td className="p-3 text-sm text-void-400">{u.email}</td>
                  <td className="p-3 text-center">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      u.rol === 'admin' ? 'bg-iris-50 text-iris-600' :
                      u.rol === 'profesor' ? 'bg-void-50 text-void-600' :
                      'bg-teal-50 text-teal-600'
                    }`}>{u.rol}</span>
                  </td>
                  <td className="p-3 text-center">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      u.tipo_usuario === 'institucional' ? 'bg-flare-50 text-flare-600' : 'bg-frost-100 text-void-500'
                    }`}>{u.tipo_usuario}</span>
                  </td>
                  <td className="p-3 text-center text-sm text-void-600">{u.puntos_totales}</td>
                  <td className="p-3 text-center">
                    {editando === u.id ? (
                      <div className="flex items-center gap-1 justify-center">
                        <select value={rolForm.rol} onChange={e => setRolForm(p => ({ ...p, rol: e.target.value }))}
                          className="text-xs border border-frost-200 rounded-lg px-2 py-1 bg-white">
                          <option value="estudiante">Estudiante</option>
                          <option value="profesor">Profesor</option>
                          <option value="admin">Admin</option>
                        </select>
                        <select value={rolForm.tipo_usuario} onChange={e => setRolForm(p => ({ ...p, tipo_usuario: e.target.value }))}
                          className="text-xs border border-frost-200 rounded-lg px-2 py-1 bg-white">
                          <option value="gratuito">Gratuito</option>
                          <option value="institucional">Institucional</option>
                        </select>
                        <button onClick={() => handleUpdate(u.id)}
                          className="text-teal-500 hover:text-teal-600 p-1">
                          <FontAwesomeIcon icon={faSave} />
                        </button>
                        <button onClick={() => setEditando(null)}
                          className="text-void-300 hover:text-void-500 p-1">✕</button>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center gap-1">
                        <button onClick={() => {
                          setEditando(u.id);
                          setRolForm({ rol: u.rol, tipo_usuario: u.tipo_usuario });
                        }}
                          className="text-void-400 hover:text-void-600 px-2 py-1 text-xs hover:bg-frost-100 rounded-lg transition">
                          Editar
                        </button>
                        {u.id !== usuarios.find(x => x.rol === 'admin')?.id && (
                          <button onClick={() => handleDelete(u.id, u.username)}
                            className="text-red-400 hover:text-red-600 px-2 py-1 text-xs hover:bg-red-50 rounded-lg transition">
                            <FontAwesomeIcon icon={faTrash} />
                          </button>
                        )}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

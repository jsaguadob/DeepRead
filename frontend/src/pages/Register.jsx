import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook, faUser, faEnvelope, faLock, faEye, faEyeSlash, faGraduationCap, faChalkboardTeacher, faUserGraduate } from '@fortawesome/free-solid-svg-icons';

export default function Register() {
  const [form, setForm] = useState({ username: '', email: '', password: '', tipo_usuario: 'gratuito', rol: 'estudiante' });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const update = (field, value) => setForm(f => ({ ...f, [field]: value }));

  const handleTipoChange = (tipo) => {
    setForm(f => ({
      ...f,
      tipo_usuario: tipo,
      rol: tipo === 'gratuito' ? 'estudiante' : f.rol
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(form);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Error al registrarse');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-sm p-8 border border-frost-200">
          <div className="text-center mb-8">
            <FontAwesomeIcon icon={faBook} className="text-3xl text-iris-400 mb-3" />
            <h1 className="text-2xl font-heading font-bold text-void-800">Crear Cuenta</h1>
            <p className="text-void-400 mt-1">Únete a DeepRead</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Nombre de Usuario</label>
              <div className="relative">
                <FontAwesomeIcon icon={faUser} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-void-300 text-sm" />
                <input type="text" value={form.username} onChange={e => update('username', e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 focus:border-iris-400 bg-frost-50 transition"
                  placeholder="usuario123" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Email</label>
              <div className="relative">
                <FontAwesomeIcon icon={faEnvelope} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-void-300 text-sm" />
                <input type="email" value={form.email} onChange={e => update('email', e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 focus:border-iris-400 bg-frost-50 transition"
                  placeholder="tu@email.com" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Tipo de Cuenta</label>
              <div className="grid grid-cols-2 gap-2">
                <button type="button" onClick={() => handleTipoChange('gratuito')}
                  className={`py-3 px-4 rounded-xl border-2 transition font-medium text-sm ${
                    form.tipo_usuario === 'gratuito'
                      ? 'border-teal-500 bg-teal-50 text-teal-700'
                      : 'border-frost-200 bg-frost-50 text-void-400'
                  }`}>
                  Gratuito
                </button>
                <button type="button" onClick={() => handleTipoChange('institucional')}
                  className={`py-3 px-4 rounded-xl border-2 transition font-medium text-sm ${
                    form.tipo_usuario === 'institucional'
                      ? 'border-iris-400 bg-iris-50 text-iris-700'
                      : 'border-frost-200 bg-frost-50 text-void-400'
                  }`}>
                  <FontAwesomeIcon icon={faGraduationCap} className="mr-1.5" />
                  Institucional
                </button>
              </div>
              {form.tipo_usuario === 'institucional' && (
                <p className="text-xs text-void-400 mt-1">Requiere email .edu (ej: usuario@uni.edu.mx)</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Rol</label>
              <div className="grid grid-cols-2 gap-2">
                <button type="button" onClick={() => update('rol', 'estudiante')}
                  className={`py-3 px-4 rounded-xl border-2 transition font-medium text-sm ${
                    form.rol === 'estudiante'
                      ? 'border-teal-500 bg-teal-50 text-teal-700'
                      : 'border-frost-200 bg-frost-50 text-void-400'
                  }`}>
                  <FontAwesomeIcon icon={faUserGraduate} className="mr-1.5" />
                  Estudiante
                </button>
                <button type="button" onClick={() => update('rol', 'profesor')}
                  className={`py-3 px-4 rounded-xl border-2 transition font-medium text-sm ${
                    form.rol === 'profesor'
                      ? 'border-flare-500 bg-flare-50 text-flare-700'
                      : 'border-frost-200 bg-frost-50 text-void-400'
                  }`}>
                  <FontAwesomeIcon icon={faChalkboardTeacher} className="mr-1.5" />
                  Profesor
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Contraseña</label>
              <div className="relative">
                <FontAwesomeIcon icon={faLock} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-void-300 text-sm" />
                <input type={showPassword ? 'text' : 'password'} value={form.password} onChange={e => update('password', e.target.value)}
                  required minLength={6}
                  className="w-full pl-10 pr-12 py-3 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 focus:border-iris-400 bg-frost-50 transition" />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-void-300 hover:text-void-500">
                  <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading}
              className="w-full bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition shadow-lg shadow-iris-500/25">
              {loading ? 'Creando cuenta...' : 'Crear Cuenta'}
            </button>
          </form>

          <p className="text-center mt-6 text-sm text-void-400">
            ¿Ya tienes cuenta?{' '}
            <Link to="/login" className="text-iris-500 hover:text-iris-600 font-medium">
              Inicia Sesión
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

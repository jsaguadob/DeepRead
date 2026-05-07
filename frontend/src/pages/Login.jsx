import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook, faEnvelope, faLock, faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

export default function Login() {
  const [loginInput, setLoginInput] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(loginInput, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Error al iniciar sesión');
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
            <h1 className="text-2xl font-heading font-bold text-void-800">Iniciar Sesión</h1>
            <p className="text-void-400 mt-1">Accede a tu cuenta de DeepRead</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Email o Usuario</label>
              <div className="relative">
                <FontAwesomeIcon icon={faEnvelope} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-void-300 text-sm" />
                <input type="text" value={loginInput} onChange={e => setLoginInput(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 focus:border-iris-400 bg-frost-50 transition"
                  placeholder="email@ejemplo.com o usuario" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-void-600 mb-1.5">Contraseña</label>
              <div className="relative">
                <FontAwesomeIcon icon={faLock} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-void-300 text-sm" />
                <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => setPassword(e.target.value)}
                  required
                  className="w-full pl-10 pr-12 py-3 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 focus:border-iris-400 bg-frost-50 transition" />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-void-300 hover:text-void-500">
                  <FontAwesomeIcon icon={showPassword ? faEyeSlash : faEye} />
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading}
              className="w-full bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition shadow-lg shadow-iris-500/25">
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </button>
          </form>

          <p className="text-center mt-6 text-sm text-void-400">
            ¿No tienes cuenta?{' '}
            <Link to="/register" className="text-iris-500 hover:text-iris-600 font-medium">
              Regístrate
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

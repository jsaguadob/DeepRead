import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook, faStar, faUsers, faBrain, faArrowRight } from '@fortawesome/free-solid-svg-icons';

export default function Landing() {
  const { user } = useAuth();

  if (user) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <FontAwesomeIcon icon={faBook} className="text-6xl text-iris-400 mb-4" />
        <h1 className="text-4xl font-heading font-bold text-void-800 mb-4">
          Bienvenido de nuevo, {user.username}
        </h1>
        <p className="text-lg text-void-400 mb-8">
          Continúa mejorando tu lectura crítica
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/dashboard"
            className="bg-iris-500 hover:bg-iris-600 text-white px-8 py-3 rounded-xl font-medium transition shadow-lg shadow-iris-500/25">
            Ir al Dashboard
          </Link>
          <Link to="/lecturas"
            className="bg-white border-2 border-void-200 hover:border-void-300 text-void-700 px-8 py-3 rounded-xl font-medium transition">
            Explorar Lecturas
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-void-800 via-void-700 to-void-900" />
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: 'radial-gradient(circle at 25% 50%, rgba(232,99,60,0.3) 0%, transparent 50%), radial-gradient(circle at 75% 50%, rgba(245,158,11,0.2) 0%, transparent 50%)'
        }} />
        <div className="relative max-w-7xl mx-auto px-4 py-24 sm:py-32">
          <div className="text-center max-w-3xl mx-auto">
            <div className="flex items-center justify-center gap-3 mb-6">
              <FontAwesomeIcon icon={faBook} className="text-5xl text-iris-400" />
            </div>
            <h1 className="text-5xl sm:text-6xl font-heading font-bold text-white mb-6 leading-tight">
              Mejora tu{' '}
              <span className="bg-gradient-to-r from-iris-400 to-flare-400 bg-clip-text text-transparent">
                lectura crítica
              </span>
            </h1>
            <p className="text-xl text-white/70 mb-10 max-w-2xl mx-auto">
              DeepRead te ayuda a desarrollar habilidades de comprensión lectora con lecturas por niveles,
              quizzes interactivos y actividades dinámicas.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link to="/register"
                className="bg-iris-500 hover:bg-iris-600 text-white px-8 py-3.5 rounded-xl font-semibold text-lg transition shadow-xl shadow-iris-500/30 flex items-center gap-2">
                Comienza Gratis <FontAwesomeIcon icon={faArrowRight} />
              </Link>
              <Link to="/login"
                className="bg-white/10 hover:bg-white/20 text-white border border-white/20 px-8 py-3.5 rounded-xl font-medium text-lg transition">
                Iniciar Sesión
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-heading font-bold text-center text-void-800 mb-12">
            ¿Por qué DeepRead?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={faBook}
              title="Lecturas por Niveles"
              description="Contenido adaptado a tu nivel de lectura, desde básico hasta avanzado."
              color="text-iris-400"
            />
            <FeatureCard
              icon={faBrain}
              title="Quizzes Interactivos"
              description="Pon a prueba tu comprensión con preguntas de opción múltiple y retroalimentación."
              color="text-teal-500"
            />
            <FeatureCard
              icon={faUsers}
              title="Grupos y Clases"
              description="Crea grupos, comparte lecturas y sigue el progreso de tus estudiantes."
              color="text-flare-500"
            />
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 bg-frost relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="bg-white rounded-2xl shadow-sm p-8 card-hover">
              <p className="text-4xl font-heading font-bold text-iris-500 mb-2">+50</p>
              <p className="text-void-400 font-medium">Lecturas disponibles</p>
            </div>
            <div className="bg-white rounded-2xl shadow-sm p-8 card-hover">
              <p className="text-4xl font-heading font-bold text-teal-500 mb-2">3</p>
              <p className="text-void-400 font-medium">Niveles de dificultad</p>
            </div>
            <div className="bg-white rounded-2xl shadow-sm p-8 card-hover">
              <p className="text-4xl font-heading font-bold text-flare-500 mb-2">Gratis</p>
              <p className="text-void-400 font-medium">Para estudiantes y profesores</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description, color }) {
  return (
    <div className="bg-frost-50 rounded-2xl p-8 card-hover border border-frost-200">
      <div className={`text-4xl mb-4 ${color}`}>
        <FontAwesomeIcon icon={icon} />
      </div>
      <h3 className="text-xl font-heading font-semibold text-void-800 mb-3">{title}</h3>
      <p className="text-void-400 leading-relaxed">{description}</p>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { activities } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGamepad, faPuzzlePiece, faClock, faStar, faSpellCheck, faListCheck } from '@fortawesome/free-solid-svg-icons';

const tipoIcon = {
  sopa: faPuzzlePiece, completar: faSpellCheck, seleccionar: faListCheck
};
const tipoColor = {
  sopa: 'bg-flare-50 text-flare-600',
  completar: 'bg-teal-50 text-teal-600',
  seleccionar: 'bg-iris-50 text-iris-600'
};

export default function Actividades() {
  const [actividades, setActividades] = useState([]);

  useEffect(() => {
    activities.list()
      .then(res => setActividades(res.data.actividades))
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center gap-3 mb-8">
        <FontAwesomeIcon icon={faGamepad} className="text-3xl text-iris-400" />
        <div>
          <h1 className="text-3xl font-heading font-bold text-void-800">Actividades</h1>
          <p className="text-void-400">Refuerza tu aprendizaje con actividades interactivas</p>
        </div>
      </div>

      {actividades.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-2xl border border-frost-200">
          <FontAwesomeIcon icon={faGamepad} className="text-4xl text-void-300 mb-3" />
          <p className="text-void-400">No hay actividades disponibles</p>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {actividades.map(a => (
            <Link key={a.id} to={`/actividades/${a.id}`}
              className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 card-hover block">
              <div className="flex items-center gap-2 mb-3">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${tipoColor[a.tipo] || 'bg-gray-100 text-gray-600'}`}>
                  <FontAwesomeIcon icon={tipoIcon[a.tipo] || faGamepad} className="mr-1" />
                  {a.tipo === 'sopa' ? 'Sopa de Letras' : a.tipo === 'completar' ? 'Completar' : 'Seleccionar'}
                </span>
                <span className="text-xs text-void-400">Nv.{a.nivel}</span>
              </div>
              <h3 className="text-lg font-heading font-semibold text-void-800 mb-1">{a.titulo}</h3>
              {a.lectura_titulo && (
                <p className="text-xs text-void-400 mb-3">Lectura: {a.lectura_titulo}</p>
              )}
              <div className="flex items-center gap-4 text-sm text-void-400 mt-4">
                <span className="flex items-center gap-1"><FontAwesomeIcon icon={faClock} /> {a.tiempo_estimado} min</span>
                <span className="flex items-center gap-1"><FontAwesomeIcon icon={faStar} className="text-flare-500" /> +{a.puntos} pts</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

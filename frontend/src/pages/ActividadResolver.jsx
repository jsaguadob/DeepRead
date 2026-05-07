import { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { activities } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faGamepad, faPuzzlePiece, faCheckCircle, faTimes } from '@fortawesome/free-solid-svg-icons';

export default function ActividadResolver() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [actividad, setActividad] = useState(null);
  const [respuesta, setRespuesta] = useState('');
  const [completado, setCompletado] = useState(false);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    activities.get(id)
      .then(res => {
        setActividad(res.data.actividad);
        setCompletado(res.data.completado);
      })
      .catch(() => {
        toast({ type: 'error', mesteal: 'Actividad no encontrada' });
        navigate('/actividades');
      });
  }, [id, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (actividad.tipo === 'seleccionar' || actividad.tipo === 'completar') {
      if (!respuesta.trim()) {
        toast({ type: 'error', mesteal: 'Ingresa una respuesta' });
        return;
      }
    }
    setEnviando(true);
    try {
      const res = await activities.submit(id, { respuesta: respuesta.trim() });
      if (res.data.completado) {
        setCompletado(true);
        toast({ mesteal: res.data.mesteal });
      } else {
        toast({ type: 'error', mesteal: res.data.mesteal });
      }
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al enviar' });
    } finally {
      setEnviando(false);
    }
  };

  if (!actividad) return <div className="p-8 text-center text-void-400">Cargando...</div>;

  if (completado) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center">
        <div className="bg-white rounded-2xl shadow-sm p-8 border border-frost-200">
          <FontAwesomeIcon icon={faCheckCircle} className="text-5xl text-teal-500 mb-4" />
          <h2 className="text-xl font-heading font-bold text-void-800 mb-2">¡Actividad Completada!</h2>
          <p className="text-void-400 mb-6">Ya realizaste esta actividad.</p>
          <Link to={`/lecturas/${actividad.lectura_id}`}
            className="inline-block bg-iris-500 hover:bg-iris-600 text-white px-6 py-2.5 rounded-xl font-medium transition">
            Volver a la lectura
          </Link>
        </div>
      </div>
    );
  }

  if (actividad.tipo === 'sopa') {
    return <WordSearch actividad={actividad} />;
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <Link to={`/lecturas/${actividad.lectura_id}`} className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver
      </Link>

      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200">
        <div className="flex items-center gap-2 mb-1">
          <FontAwesomeIcon icon={faGamepad} className="text-iris-400" />
          <span className="text-sm font-medium text-void-500">{actividad.tipo === 'completar' ? 'Completar' : 'Seleccionar'}</span>
        </div>
        <h1 className="text-2xl font-heading font-bold text-void-800 mb-2">{actividad.titulo}</h1>
        <p className="text-flare-500 font-semibold mb-4">+{actividad.puntos} pts</p>
        <p className="text-void-700 mb-6 leading-relaxed">{actividad.contenido}</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-void-600 mb-1.5">
              {actividad.tipo === 'seleccionar' ? 'Tu respuesta' : 'Escribe la palabra correcta'}
            </label>
            <input type="text" value={respuesta} onChange={e => setRespuesta(e.target.value)}
              className="w-full px-4 py-3 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50"
              placeholder="Escribe aquí..." />
          </div>
          <button type="submit" disabled={enviando}
            className="w-full bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition shadow-lg shadow-iris-500/25">
            {enviando ? 'Enviando...' : 'Verificar Respuesta'}
          </button>
        </form>
      </div>
    </div>
  );
}

function WordSearch({ actividad }) {
  const [grid, setGrid] = useState([]);
  const [selectedCells, setSelectedCells] = useState([]);
  const [foundWords, setFoundWords] = useState([]);
  const [enviando, setEnviando] = useState(false);
  const [completado, setCompletado] = useState(false);
  const palabras = actividad.contenido.split(',').map(p => p.trim().toUpperCase());
  const size = 10;

  const initGrid = useCallback(() => {
    const newGrid = Array(size).fill(null).map(() => Array(size).fill(''));
    const positions = {};

    for (const word of palabras) {
      let placed = false;
      let tries = 0;
      while (!placed && tries < 100) {
        const r = Math.floor(Math.random() * size);
        const c = Math.floor(Math.random() * size);
        const dir = Math.random() > 0.5 ? 'H' : 'V';
        if (dir === 'H' && c + word.length <= size) {
          let fit = true;
          for (let i = 0; i < word.length; i++) {
            if (newGrid[r][c + i] && newGrid[r][c + i] !== word[i]) fit = false;
          }
          if (fit) {
            for (let i = 0; i < word.length; i++) newGrid[r][c + i] = word[i];
            placed = true;
          }
        } else if (dir === 'V' && r + word.length <= size) {
          let fit = true;
          for (let i = 0; i < word.length; i++) {
            if (newGrid[r + i]?.[c] && newGrid[r + i][c] !== word[i]) fit = false;
          }
          if (fit) {
            for (let i = 0; i < word.length; i++) newGrid[r + i][c] = word[i];
            placed = true;
          }
        }
        tries++;
      }
    }

    const ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        if (!newGrid[r][c]) newGrid[r][c] = ABC[Math.floor(Math.random() * ABC.length)];
      }
    }
    setGrid(newGrid);
  }, [actividad]);

  useEffect(() => { initGrid(); }, [initGrid]);

  const toggleCell = (r, c) => {
    const key = `${r}-${c}`;
    setSelectedCells(prev =>
      prev.includes(key) ? prev.filter(k => k !== key) : [...prev, key]
    );
  };

  const checkWord = () => {
    const sortedSel = [...selectedCells].sort().join(',');
    for (const word of palabras) {
      if (foundWords.includes(word)) continue;
      const positions = [];
      for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
          if (grid[r][c] === word[0]) {
            let found = true;
            for (let i = 0; i < word.length; i++) {
              const row = r, col = c + i;
              if (col >= size || grid[row]?.[col] !== word[i]) {
                found = false;
                break;
              }
            }
            if (found) {
              for (let i = 0; i < word.length; i++) positions.push(`${r}-${c + i}`);
              break;
            }
            found = true;
            for (let i = 0; i < word.length; i++) {
              const row = r + i, col = c;
              if (row >= size || grid[row]?.[col] !== word[i]) {
                found = false;
                break;
              }
            }
            if (found) {
              for (let i = 0; i < word.length; i++) positions.push(`${r + i}-${c}`);
              break;
            }
          }
        }
        if (positions.length > 0) break;
      }
      if (positions.length > 0 && sortedSel === [...positions].sort().join(',')) {
        setFoundWords(prev => [...prev, word]);
        setSelectedCells([]);
        return;
      }
    }
    toast({ type: 'error', mesteal: 'Esa selección no es correcta' });
  };

  const handleSubmitSopa = async () => {
    setEnviando(true);
    try {
      const res = await activities.submit(actividad.id, { encontradas: foundWords.join(',') });
      if (res.data.completado) {
        setCompletado(true);
        toast({ mesteal: res.data.mesteal });
      } else {
        toast({ mesteal: `Encontradas ${foundWords.length} de ${palabras.length}` });
      }
    } catch {
      toast({ type: 'error', mesteal: 'Error al enviar' });
    } finally {
      setEnviando(false);
    }
  };

  if (completado) {
    return (
      <div className="max-w-lg mx-auto px-4 py-12 text-center">
        <div className="bg-white rounded-2xl shadow-sm p-8 border border-frost-200">
          <FontAwesomeIcon icon={faCheckCircle} className="text-5xl text-teal-500 mb-4" />
          <h2 className="text-xl font-heading font-bold text-void-800 mb-2">¡Sopa Completa!</h2>
          <p className="text-void-400 mb-6">Has encontrado todas las palabras.</p>
          <Link to={`/lecturas/${actividad.lectura_id}`}
            className="inline-block bg-iris-500 hover:bg-iris-600 text-white px-6 py-2.5 rounded-xl font-medium transition">
            Volver a la lectura
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <Link to={`/lecturas/${actividad.lectura_id}`} className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-4 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver
      </Link>

      <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 text-center">
        <FontAwesomeIcon icon={faPuzzlePiece} className="text-2xl text-flare-500 mb-2" />
        <h1 className="text-2xl font-heading font-bold text-void-800">{actividad.titulo}</h1>
        <p className="text-sm text-void-400 mb-4">Haz clic en las letras para seleccionar palabras</p>

        <div className="mb-4">
          <p className="text-sm font-medium text-void-600 mb-2">Palabras a encontrar:</p>
          <div className="flex flex-wrap justify-center gap-2">
            {palabras.map((p, i) => (
              <span key={i}
                className={`px-3 py-1 rounded-lg text-sm border transition ${
                  foundWords.includes(p) ? 'bg-teal-500 text-white border-teal-600 line-through' : 'bg-frost-50 text-void-600 border-frost-200'
                }`}>
                {p}
              </span>
            ))}
          </div>
        </div>

        <div className="inline-grid gap-1 mb-4" style={{ gridTemplateColumns: `repeat(${size}, 1fr)` }}>
          {grid.map((row, r) =>
            row.map((cell, c) => {
              const key = `${r}-${c}`;
              const isSelected = selectedCells.includes(key);
              const isFound = foundWords.some(w => {
                let found = false;
                for (let i = 0; i < w.length; i++) {
                  const rowR = r, colC = c;
                  // Check horizontal
                  if (colC + w.length <= size) {
                    let ok = true;
                    for (let j = 0; j < w.length; j++) if (grid[rowR]?.[colC + j] !== w[j]) ok = false;
                    if (ok) { found = true; break; }
                  }
                  // Check vertical
                  if (rowR + w.length <= size) {
                    let ok = true;
                    for (let j = 0; j < w.length; j++) if (grid[rowR + j]?.[colC] !== w[j]) ok = false;
                    if (ok) { found = true; break; }
                  }
                }
                return found;
              });
              return (
                <button key={key} onClick={() => !isFound && toggleCell(r, c)}
                  className={`w-9 h-9 sm:w-10 sm:h-10 font-bold text-sm rounded transition ${
                    isFound ? 'bg-teal-500 text-white cursor-default' :
                    isSelected ? 'bg-iris-400 text-white' :
                    'bg-frost-100 hover:bg-frost-200 text-void-700 cursor-pointer'
                  }`}>
                  {cell}
                </button>
              );
            })
          )}
        </div>

        <div className="flex justify-center gap-3 mb-4">
          <button onClick={() => setSelectedCells([])}
            className="bg-void-100 hover:bg-void-200 text-void-600 px-4 py-2 rounded-xl text-sm font-medium transition">
            Limpiar
          </button>
          <button onClick={checkWord}
            disabled={selectedCells.length === 0}
            className="bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-white px-4 py-2 rounded-xl text-sm font-medium transition">
            Marcar Palabra
          </button>
        </div>

        <p className="text-sm text-void-400 mb-4">
          Encontradas: {foundWords.length} / {palabras.length}
        </p>

        <button onClick={handleSubmitSopa} disabled={enviando}
          className="w-full bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition shadow-lg shadow-iris-500/25">
          {enviando ? 'Enviando...' : 'TERMINAR Y VERIFICAR'}
        </button>
      </div>
    </div>
  );
}

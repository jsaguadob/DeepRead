import { useState, useRef } from 'react';
import { readings } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { toast } from './Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileUpload, faTimes, faFilePdf, faFileWord, faFileAlt, faCheckCircle, faSpinner } from '@fortawesome/free-solid-svg-icons';

const EXTENSIONS = ['.pdf', '.docx', '.txt'];

export default function FileImportModal({ onClose, onCreated, misGrupos }) {
  const { isAdmin, isProfesor } = useAuth();
  const inputRef = useRef(null);
  const [archivo, setArchivo] = useState(null);
  const [categoria, setCategoria] = useState('');
  const [grupoId, setGrupoId] = useState(
    misGrupos?.length === 1 ? String(misGrupos[0].id) : ''
  );
  const [cantidadPreguntas, setCantidadPreguntas] = useState(5);
  const [generarQuiz, setGenerarQuiz] = useState(true);
  const [procesando, setProcesando] = useState(false);
  const [etapa, setEtapa] = useState('');
  const [completado, setCompletado] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext))) {
      setArchivo(file);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) setArchivo(file);
  };

  const iconoArchivo = () => {
    if (!archivo) return faFileUpload;
    const name = archivo.name.toLowerCase();
    if (name.endsWith('.pdf')) return faFilePdf;
    if (name.endsWith('.docx')) return faFileWord;
    return faFileAlt;
  };

  const handleSubmit = async () => {
    if (!archivo) return;
    setProcesando(true);
    setCompletado(false);
    try {
      setEtapa('Extrayendo texto del archivo...');
      await new Promise(r => setTimeout(r, 500));

      const formData = new FormData();
      formData.append('archivo', archivo);
      formData.append('cantidad_preguntas', String(generarQuiz ? cantidadPreguntas : 0));
      formData.append('categoria', categoria);
      if (grupoId) formData.append('grupo_id', grupoId);

      if (generarQuiz && cantidadPreguntas > 0) {
        setEtapa('Analizando contenido con IA...');
        await new Promise(r => setTimeout(r, 800));
        setEtapa('Generando preguntas...');
      }

      const res = await readings.importarArchivo(formData);
      setEtapa('');
      setCompletado(true);
      toast({ mesteal: `Lectura importada: ${res.data.lectura.titulo} (${res.data.total_preguntas} preguntas)` });
      setTimeout(() => {
        onCreated(res.data.lectura);
        onClose();
      }, 1500);
    } catch (err) {
      setEtapa('');
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al importar' });
    } finally {
      setProcesando(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" onClick={e => e.target === e.currentTarget && !procesando && onClose()}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6">
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-lg font-heading font-bold text-void-800">Importar Archivo</h2>
          {!procesando && (
            <button onClick={onClose} className="text-void-400 hover:text-void-600"><FontAwesomeIcon icon={faTimes} /></button>
          )}
        </div>

        {completado ? (
          <div className="text-center py-8">
            <FontAwesomeIcon icon={faCheckCircle} className="text-5xl text-teal-500 mb-3" />
            <p className="text-void-700 font-semibold">Lectura importada exitosamente</p>
          </div>
        ) : procesando ? (
          <div className="text-center py-8">
            <FontAwesomeIcon icon={faSpinner} className="text-4xl text-iris-500 mb-4 animate-spin" />
            <p className="text-void-600">{etapa}</p>
          </div>
        ) : (
          <>
            {/* Drop zone */}
            <div
              onDragOver={e => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => inputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition mb-5 ${
                archivo ? 'border-teal-400 bg-teal-50' : 'border-frost-300 hover:border-iris-400 bg-frost-50'
              }`}>
              <input ref={inputRef} type="file" accept=".pdf,.docx,.txt" onChange={handleFileSelect} className="hidden" />
              <FontAwesomeIcon icon={iconoArchivo()} className={`text-4xl mb-2 ${archivo ? 'text-teal-500' : 'text-void-400'}`} />
              {archivo ? (
                <p className="font-medium text-void-700">{archivo.name}</p>
              ) : (
                <>
                  <p className="font-medium text-void-500 mb-1">Arrastra un archivo o haz clic</p>
                  <p className="text-xs text-void-400">PDF, DOCX o TXT</p>
                </>
              )}
            </div>

            {/* Fields */}
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-void-500 mb-1">Categoría</label>
                <select value={categoria} onChange={e => setCategoria(e.target.value)}
                  className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-frost-50 text-sm focus:outline-none focus:ring-2 focus:ring-iris-400/50">
                  <option value="">Sin categoría</option>
                  <option value="ciencia">Ciencia</option>
                  <option value="historia">Historia</option>
                  <option value="literatura">Literatura</option>
                  <option value="tecnologia">Tecnología</option>
                  <option value="arte">Arte</option>
                  <option value="filosofia">Filosofía</option>
                </select>
              </div>

              {(isProfesor() && !isAdmin()) && misGrupos?.length > 0 && (
                <div>
                  <label className="block text-xs font-medium text-void-500 mb-1">Grupo *</label>
                  <select value={grupoId} onChange={e => setGrupoId(e.target.value)}
                    className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-frost-50 text-sm focus:outline-none focus:ring-2 focus:ring-iris-400/50">
                    <option value="">Seleccionar grupo</option>
                    {misGrupos.map(g => <option key={g.id} value={g.id}>{g.nombre}</option>)}
                  </select>
                </div>
              )}

              <div className="flex items-center gap-3">
                <input type="checkbox" id="genQuiz" checked={generarQuiz} onChange={e => setGenerarQuiz(e.target.checked)}
                  className="accent-iris-500" />
                <label htmlFor="genQuiz" className="text-sm text-void-700">Generar preguntas automáticamente</label>
              </div>

              {generarQuiz && (
                <div>
                  <label className="block text-xs font-medium text-void-500 mb-1">Cantidad de preguntas</label>
                  <input type="number" min={1} max={20} value={cantidadPreguntas} onChange={e => setCantidadPreguntas(parseInt(e.target.value) || 5)}
                    className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-frost-50 text-sm focus:outline-none focus:ring-2 focus:ring-iris-400/50" />
                </div>
              )}
            </div>

            <button onClick={handleSubmit} disabled={!archivo || (isProfesor() && !isAdmin() && !grupoId)}
              className="w-full mt-5 bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white py-2.5 rounded-xl font-medium transition">
              <FontAwesomeIcon icon={faFileUpload} className="mr-2" />Importar y Procesar
            </button>
          </>
        )}
      </div>
    </div>
  );
}
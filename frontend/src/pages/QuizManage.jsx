import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { quizzes, readings, ai } from '../services/api';
import { toast } from '../components/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faPlus, faTrash, faPencilAlt, faSave, faTimes, faCopy, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons';

export default function QuizManage() {
  const { id } = useParams();
  const [lectura, setLectura] = useState(null);
  const [preguntas, setPreguntas] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showBatch, setShowBatch] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ pregunta: '', opcion_a: '', opcion_b: '', opcion_c: '', opcion_d: '', respuesta_correcta: 'a', explicacion: '' });
  const [batchForm, setBatchForm] = useState([{ pregunta: '', opcion_a: '', opcion_b: '', opcion_c: '', opcion_d: '', respuesta_correcta: 'a', explicacion: '' }]);
  const [loading, setLoading] = useState(false);
  const [generandoIA, setGenerandoIA] = useState(false);
  const [aiCantidad, setAiCantidad] = useState(5);

  useEffect(() => {
    readings.get(id).then(r => setLectura(r.data.lectura));
    loadQuestions();
  }, [id]);

  const loadQuestions = () => {
    quizzes.getQuestions(id).then(res => setPreguntas(res.data.preguntas));
  };

  const update = (f, v) => setForm(p => ({ ...p, [f]: v }));

  const resetForm = () => {
    setForm({ pregunta: '', opcion_a: '', opcion_b: '', opcion_c: '', opcion_d: '', respuesta_correcta: 'a', explicacion: '' });
    setEditId(null);
    setShowForm(false);
  };

  const handleEdit = (p) => {
    setForm({
      pregunta: p.pregunta, opcion_a: p.opcion_a, opcion_b: p.opcion_b,
      opcion_c: p.opcion_c, opcion_d: p.opcion_d, respuesta_correcta: p.respuesta_correcta, explicacion: p.explicacion || ''
    });
    setEditId(p.id);
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (editId) {
        await quizzes.updateQuestion(editId, form);
        toast({ mesteal: 'Pregunta actualizada' });
      } else {
        await quizzes.createQuestion(id, form);
        toast({ mesteal: 'Pregunta agregada' });
      }
      resetForm();
      loadQuestions();
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error' });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (preguntaId) => {
    if (!confirm('¿Eliminar esta pregunta?')) return;
    try {
      await quizzes.deleteQuestion(preguntaId);
      toast({ mesteal: 'Pregunta eliminada' });
      loadQuestions();
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al eliminar' });
    }
  };

  const handleBatchSubmit = async () => {
    const validas = batchForm.filter(q => q.pregunta && q.opcion_a);
    if (validas.length === 0) {
      toast({ type: 'error', mesteal: 'Agrega al menos una pregunta' });
      return;
    }
    setLoading(true);
    try {
      const res = await quizzes.batchCreate(id, { preguntas: validas });
      toast({ mesteal: res.data.mesteal });
      setBatchForm([{ pregunta: '', opcion_a: '', opcion_b: '', opcion_c: '', opcion_d: '', respuesta_correcta: 'a', explicacion: '' }]);
      setShowBatch(false);
      loadQuestions();
    } catch (err) {
      toast({ type: 'error', mesteal: 'Error al crear preguntas' });
    } finally {
      setLoading(false);
    }
  };

  const addBatchRow = () => {
    setBatchForm(prev => [...prev, { pregunta: '', opcion_a: '', opcion_b: '', opcion_c: '', opcion_d: '', respuesta_correcta: 'a', explicacion: '' }]);
  };

  const updateBatch = (i, field, value) => {
    setBatchForm(prev => prev.map((q, idx) => idx === i ? { ...q, [field]: value } : q));
  };

  const removeBatchRow = (i) => {
    setBatchForm(prev => prev.filter((_, idx) => idx !== i));
  };

  const handleGenerarIA = async () => {
    setGenerandoIA(true);
    try {
      const res = await ai.generarQuiz({ lectura_id: parseInt(id), cantidad: aiCantidad });
      if (res.data.error) {
        toast({ type: 'error', mesteal: res.data.error });
        return;
      }
      if (res.data.preguntas) {
        setBatchForm(res.data.preguntas);
        setShowBatch(true);
        setShowForm(false);
        toast({ mesteal: `${res.data.preguntas.length} preguntas generadas por IA` });
      }
    } catch (err) {
      toast({ type: 'error', mesteal: err.response?.data?.error || 'Error al conectar con la IA' });
    } finally {
      setGenerandoIA(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <Link to={`/lecturas/${id}`} className="inline-flex items-center gap-2 text-void-400 hover:text-void-600 mb-6 transition">
        <FontAwesomeIcon icon={faArrowLeft} /> Volver a la lectura
      </Link>

      <h1 className="text-2xl font-heading font-bold text-void-800 mb-2">Gestionar Quiz</h1>
      <p className="text-void-400 mb-6">
        {lectura?.titulo} — {preguntas.length} pregunta{preguntas.length !== 1 ? 's' : ''}
      </p>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-3 mb-8">
        <button onClick={() => { setShowForm(true); setShowBatch(false); }}
          className="bg-iris-500 hover:bg-iris-600 text-white px-4 py-2 rounded-xl font-medium transition flex items-center gap-2">
          <FontAwesomeIcon icon={faPlus} /> Agregar Pregunta
        </button>
        <button onClick={() => { setShowBatch(!showBatch); setShowForm(false); }}
          className="bg-teal-500 hover:bg-teal-600 text-white px-4 py-2 rounded-xl font-medium transition flex items-center gap-2">
          <FontAwesomeIcon icon={faCopy} /> Creación Múltiple
        </button>
        <div className="flex items-center gap-2 ml-auto">
          <select value={aiCantidad} onChange={e => setAiCantidad(parseInt(e.target.value))}
            className="px-3 py-2 border border-frost-200 rounded-xl bg-white text-sm">
            {[3,5,8,10].map(n => <option key={n} value={n}>{n} preg.</option>)}
          </select>
          <button onClick={handleGenerarIA} disabled={generandoIA}
            className="bg-gradient-to-r from-iris-500 to-violet-600 hover:from-iris-600 hover:to-violet-700 disabled:opacity-50 text-white px-4 py-2 rounded-xl font-medium transition flex items-center gap-2 shadow-lg shadow-iris-500/30">
            <FontAwesomeIcon icon={faWandMagicSparkles} className={generandoIA ? 'animate-spin' : ''} />
            {generandoIA ? 'Generando...' : 'Generar con IA'}
          </button>
        </div>
      </div>

      {/* Single question form */}
      {showForm && (
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mb-8">
          <h2 className="font-heading font-semibold text-void-800 mb-4">
            {editId ? 'Editar Pregunta' : 'Nueva Pregunta'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-void-600 mb-1">Pregunta</label>
              <textarea value={form.pregunta} onChange={e => update('pregunta', e.target.value)} required rows={2}
                className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              {['a', 'b', 'c', 'd'].map(letra => (
                <div key={letra}>
                  <label className="block text-sm font-medium text-void-600 mb-1">Opción {letra.toUpperCase()}</label>
                  <input type="text" value={form[`opcion_${letra}`]} onChange={e => update(`opcion_${letra}`, e.target.value)} required
                    className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
                </div>
              ))}
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Respuesta Correcta</label>
                <select value={form.respuesta_correcta} onChange={e => update('respuesta_correcta', e.target.value)}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50">
                  {['a', 'b', 'c', 'd'].map(l => <option key={l} value={l}>{l.toUpperCase()}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-void-600 mb-1">Explicación</label>
                <input type="text" value={form.explicacion} onChange={e => update('explicacion', e.target.value)}
                  className="w-full px-4 py-2.5 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50" />
              </div>
            </div>
            <div className="flex gap-3">
              <button type="submit" disabled={loading}
                className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-medium transition">
                {loading ? 'Guardando...' : editId ? 'Actualizar' : 'Agregar Pregunta'}
              </button>
              <button type="button" onClick={resetForm}
                className="bg-void-100 hover:bg-void-200 text-void-600 px-6 py-2.5 rounded-xl font-medium transition">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Batch form */}
      {showBatch && (
        <div className="bg-white rounded-2xl shadow-sm p-6 border border-frost-200 mb-8">
          <h2 className="font-heading font-semibold text-void-800 mb-4">Creación Múltiple de Preguntas</h2>
          {batchForm.map((q, i) => (
            <div key={i} className="border border-frost-200 rounded-xl p-4 mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-void-600">Pregunta #{i + 1}</span>
                {batchForm.length > 1 && (
                  <button type="button" onClick={() => removeBatchRow(i)} className="text-red-400 hover:text-red-600">
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                )}
              </div>
              <div className="space-y-3">
                <textarea placeholder="Pregunta" value={q.pregunta} onChange={e => updateBatch(i, 'pregunta', e.target.value)} rows={1}
                  className="w-full px-4 py-2 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50 text-sm" />
                <div className="grid grid-cols-2 gap-2">
                  {['a', 'b', 'c', 'd'].map(letra => (
                    <input key={letra} type="text" placeholder={`Opción ${letra.toUpperCase()}`}
                      value={q[`opcion_${letra}`]} onChange={e => updateBatch(i, `opcion_${letra}`, e.target.value)}
                      className="px-3 py-2 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50 text-sm" />
                  ))}
                </div>
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="text-xs text-void-400">Correcta</label>
                    <select value={q.respuesta_correcta} onChange={e => updateBatch(i, 'respuesta_correcta', e.target.value)}
                      className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-frost-50 text-sm">
                      {['a', 'b', 'c', 'd'].map(l => <option key={l} value={l}>{l.toUpperCase()}</option>)}
                    </select>
                  </div>
                  <div className="flex-[2]">
                    <label className="text-xs text-void-400">Explicación</label>
                    <input type="text" placeholder="Opcional" value={q.explicacion} onChange={e => updateBatch(i, 'explicacion', e.target.value)}
                      className="w-full px-3 py-2 border border-frost-200 rounded-xl bg-frost-50 text-sm" />
                  </div>
                </div>
              </div>
            </div>
          ))}
          <div className="flex gap-3">
            <button onClick={addBatchRow}
              className="bg-void-100 hover:bg-void-200 text-void-600 px-4 py-2 rounded-xl font-medium transition flex items-center gap-2">
              <FontAwesomeIcon icon={faPlus} /> Agregar otra
            </button>
            <button onClick={handleBatchSubmit} disabled={loading}
              className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-6 py-2 rounded-xl font-medium transition">
              {loading ? 'Guardando...' : `Guardar ${batchForm.length} pregunta${batchForm.length > 1 ? 's' : ''}`}
            </button>
          </div>
        </div>
      )}

      {/* Questions list */}
      <div className="space-y-4">
        {preguntas.map((p, i) => (
          <div key={p.id} className="bg-white rounded-2xl shadow-sm p-5 border border-frost-200">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="font-semibold text-void-800 mb-2">{i + 1}. {p.pregunta}</h3>
                <div className="grid grid-cols-2 gap-2 ml-4">
                  {['a', 'b', 'c', 'd'].map(letra => (
                    <div key={letra}
                      className={`px-3 py-1.5 rounded-lg text-sm ${
                        p.respuesta_correcta === letra ? 'bg-teal-50 text-teal-700 border border-teal-300' : 'bg-frost-50 text-void-500'
                      }`}>
                      {letra.toUpperCase()}) {p[`opcion_${letra}`]}
                    </div>
                  ))}
                </div>
                {p.explicacion && (
                  <p className="mt-2 text-sm text-void-400"><strong>Explicación:</strong> {p.explicacion}</p>
                )}
              </div>
              <div className="flex gap-2 ml-4">
                <button onClick={() => handleEdit(p)}
                  className="text-void-400 hover:text-void-600 p-2 hover:bg-frost-100 rounded-lg transition">
                  <FontAwesomeIcon icon={faPencilAlt} />
                </button>
                <button onClick={() => handleDelete(p.id)}
                  className="text-red-400 hover:text-red-600 p-2 hover:bg-red-50 rounded-lg transition">
                  <FontAwesomeIcon icon={faTrash} />
                </button>
              </div>
            </div>
          </div>
        ))}
        {preguntas.length === 0 && (
          <div className="text-center py-12 bg-white rounded-2xl border border-frost-200">
            <p className="text-void-400 mb-4">No hay preguntas todavía</p>
            <button onClick={() => setShowForm(true)}
              className="text-iris-500 hover:text-iris-600 font-medium">
              Crear primera pregunta
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

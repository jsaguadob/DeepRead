import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ai } from '../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRobot, faTimes, faPaperPlane, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons';

export default function AIChatWidget() {
  const [open, setOpen] = useState(false);
  const [mensajes, setMensajes] = useState([]);
  const [input, setInput] = useState('');
  const [enviando, setEnviando] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    if (open && mensajes.length === 0) {
      setMensajes([{ role: 'ai', text: '¡Hola! Soy tu asistente de análisis. Pregúntame sobre estadísticas, rendimiento de estudiantes, quizzes, etc.' }]);
    }
  }, [open]);

  useEffect(() => {
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes]);

  const enviar = async () => {
    if (!input.trim() || enviando) return;
    const msg = input.trim();
    setInput('');
    setMensajes(prev => [...prev, { role: 'user', text: msg }]);
    setEnviando(true);
    try {
      const res = await ai.chat({ mensaje: msg });
      setMensajes(prev => [...prev, { role: 'ai', text: res.data.respuesta || res.data.error || 'Sin respuesta' }]);
    } catch {
      setMensajes(prev => [...prev, { role: 'ai', text: 'Error al conectar con la IA' }]);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <>
      {!open && (
        <button onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 bg-gradient-to-r from-iris-500 to-violet-600 text-white w-14 h-14 rounded-full shadow-xl flex items-center justify-center hover:scale-105 transition z-50">
          <FontAwesomeIcon icon={faWandMagicSparkles} className="text-xl" />
        </button>
      )}
      {open && (
        <div className="fixed bottom-6 right-6 w-96 max-w-[calc(100vw-2rem)] bg-white rounded-2xl shadow-2xl border border-frost-200 flex flex-col z-50" style={{ height: '500px', maxHeight: 'calc(100vh - 4rem)' }}>
          <div className="flex items-center justify-between p-4 border-b border-frost-200 bg-gradient-to-r from-iris-500 to-violet-600 text-white rounded-t-2xl">
            <div className="flex items-center gap-2">
              <FontAwesomeIcon icon={faRobot} />
              <span className="font-semibold text-sm">Asistente IA</span>
            </div>
            <button onClick={() => setOpen(false)} className="text-white/80 hover:text-white">
              <FontAwesomeIcon icon={faTimes} />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {mensajes.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-iris-500 text-white rounded-br-md'
                    : 'bg-frost-100 text-void-700 rounded-bl-md'
                }`}>
                  {m.role === 'user' ? m.text : (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}
                      components={{
                        strong: ({ children }) => <span className="font-bold text-iris-600">{children}</span>,
                        ul: ({ children }) => <ul className="list-disc pl-4 space-y-0.5 my-1">{children}</ul>,
                        ol: ({ children }) => <ol className="list-decimal pl-4 space-y-0.5 my-1">{children}</ol>,
                        p: ({ children }) => <p className="mb-1 last:mb-0">{children}</p>,
                        code: ({ children }) => <code className="bg-void-100/30 px-1 rounded text-xs">{children}</code>,
                      }}
                    >
                      {m.text}
                    </ReactMarkdown>
                  )}
                </div>
              </div>
            ))}
            {enviando && (
              <div className="flex justify-start">
                <div className="bg-frost-100 px-4 py-2.5 rounded-2xl text-sm text-void-400 rounded-bl-md">
                  <FontAwesomeIcon icon={faRobot} className="mr-2 animate-pulse" />Pensando...
                </div>
              </div>
            )}
            <div ref={ref} />
          </div>
          <div className="p-3 border-t border-frost-200">
            <div className="flex gap-2">
              <input type="text" value={input} onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && enviar()}
                placeholder="Pregunta sobre estadísticas..."
                className="flex-1 px-4 py-2 border border-frost-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-iris-400/50 bg-frost-50 text-sm" />
              <button onClick={enviar} disabled={enviando || !input.trim()}
                className="bg-iris-500 hover:bg-iris-600 disabled:opacity-50 text-white px-4 py-2 rounded-xl transition">
                <FontAwesomeIcon icon={faPaperPlane} />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

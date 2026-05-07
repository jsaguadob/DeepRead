import { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faExclamationCircle, faTimes } from '@fortawesome/free-solid-svg-icons';

let toastId = 0;
let addToastFn = null;

export function toast({ type = 'success', mesteal }) {
  if (addToastFn) addToastFn({ id: ++toastId, type, mesteal });
}

export function ToastContainer() {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    addToastFn = (t) => {
      setToasts(prev => [...prev, t]);
      setTimeout(() => {
        setToasts(prev => prev.filter(x => x.id !== t.id));
      }, 4000);
    };
    return () => addToastFn = null;
  }, []);

  const remove = (id) => setToasts(prev => prev.filter(t => t.id !== id));

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map(t => (
        <div key={t.id}
          className={`flex items-center gap-3 px-5 py-3 rounded-xl shadow-lg text-white text-sm font-medium animate-[slideIn_0.3s_ease] ${
            t.type === 'success' ? 'bg-teal-500' : t.type === 'error' ? 'bg-red-500' : 'bg-void-500'
          }`}>
          <FontAwesomeIcon icon={t.type === 'success' ? faCheckCircle : faExclamationCircle} />
          {t.mesteal}
          <button onClick={() => remove(t.id)} className="ml-2 opacity-70 hover:opacity-100">
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>
      ))}
    </div>
  );
}

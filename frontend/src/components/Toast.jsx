import React, { useEffect } from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

export default function Toast({ toast, onClose }) {
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => {
      onClose();
    }, 3500);
    return () => clearTimeout(timer);
  }, [toast, onClose]);

  if (!toast) return null;

  const { type = 'success', message } = toast;

  const getStyle = () => {
    switch (type) {
      case 'error':
        return {
          bg: 'bg-red-900/90 border-red-500/50 text-white',
          icon: <AlertCircle className="w-4 h-4 text-red-300 shrink-0" />,
        };
      case 'info':
        return {
          bg: 'bg-slate-900/90 border-slate-700 text-white',
          icon: <Info className="w-4 h-4 text-blue-400 shrink-0" />,
        };
      default:
        return {
          bg: 'bg-slate-950/95 border-emerald-500/40 text-white',
          icon: <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />,
        };
    }
  };

  const style = getStyle();

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-fade-in max-w-sm">
      <div className={`flex items-center gap-3 px-4 py-3 rounded-2xl shadow-xl backdrop-blur-md border ${style.bg} text-xs font-medium`}>
        {style.icon}
        <span className="flex-1 leading-snug">{message}</span>
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-white transition-colors p-1"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}

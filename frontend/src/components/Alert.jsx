import { X, AlertCircle } from 'lucide-react';

export function Alert({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="fixed top-6 right-6 z-50 animate-in fade-in slide-in-from-top-4 duration-300">
      <div className="bg-red-500/10 border border-red-500 text-red-500 p-4 rounded-xl shadow-2xl backdrop-blur-md flex items-center gap-3 min-w-[300px]">
        <AlertCircle size={20} className="shrink-0" />
        <p className="text-sm font-medium flex-1">{message}</p>
        <button onClick={onClose} className="hover:bg-red-500/20 p-1 rounded-lg transition-colors">
          <X size={18} />
        </button>
      </div>
    </div>
  );
}
import { useState, useEffect } from 'react';
import { api } from '../api/axios';
import { Plus, Trash2, Users, Clock, MapPin } from 'lucide-react';

export function Bookings() {
  const [bookings, setBookings] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [formData, setFormData] = useState({ title: '', roomId: '', startAt: '', endAt: '', participants: '' });

  useEffect(() => { 
    api.get('/rooms/').then(res => setRooms(res.data.items || []));
    fetchBookings(); 
  }, []);

  const fetchBookings = async () => {
    const res = await api.get('/bookings/');
    setBookings(res.data.items || []);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
        const payload = {
            ...formData,
            roomId: parseInt(formData.roomId),
            participants: formData.participants.split(',').map(i => i.trim())
          };
          await api.post('/bookings/', payload);
          setFormData({ title: '', roomId: '', startAt: '', endAt: '', participants: '' });
          fetchBookings();
    } catch (err) { alert("Erro ao criar reserva"); }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">Gerenciar Reservas</h1>
        <p className="text-slate-400">Agende reuniões e gerencie horários das salas.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Formulário */}
        <div className="lg:col-span-5">
          <form onSubmit={handleCreate} className="bg-slate-800 border border-slate-700 p-6 rounded-2xl space-y-4 sticky top-8">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-2">
              <Plus size={20} className="text-blue-500" /> Nova Reserva
            </h2>
            
            <input 
              placeholder="Título da Reunião" 
              className="w-full bg-slate-900 border border-slate-700 p-3 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
              onChange={e => setFormData({...formData, title: e.target.value})} 
              value={formData.title} required 
            />

            <select 
              className="w-full bg-slate-900 border border-slate-700 p-3 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
              onChange={e => setFormData({...formData, roomId: e.target.value})} 
              value={formData.roomId} required
            >
              <option value="">Selecione a Sala</option>
              {rooms.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>

            <div className="grid grid-cols-2 gap-3">
              <input type="datetime-local" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-xs" 
                onChange={e => setFormData({...formData, startAt: e.target.value})} value={formData.startAt} required />
              <input type="datetime-local" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-xs" 
                onChange={e => setFormData({...formData, endAt: e.target.value})} value={formData.endAt} required />
            </div>

            <textarea 
              placeholder="Participantes (e-mail, e-mail...)" 
              className="w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-sm min-h-[100px]" 
              onChange={e => setFormData({...formData, participants: e.target.value})} 
              value={formData.participants} required 
            />

            <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-600/20">
              Confirmar Reserva
            </button>
          </form>
        </div>

        {/* Listagem */}
        <div className="lg:col-span-7 space-y-4">
          {bookings.length === 0 && <div className="text-center py-20 border-2 border-dashed border-slate-800 rounded-2xl text-slate-500">Nenhuma reserva encontrada</div>}
          
          {bookings.map(b => (
            <div key={b.id} className="bg-slate-800/50 border border-slate-700 p-5 rounded-2xl hover:bg-slate-800 transition-all group">
              <div className="flex justify-between items-start">
                <div className="space-y-2">
                  <span className={`text-[10px] font-bold uppercase px-2 py-1 rounded ${b.status === 'ACTIVE' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-red-500/10 text-red-500'}`}>
                    {b.status === 'ACTIVE' ? 'Ativa' : 'Cancelada'}
                  </span>
                  <h3 className="text-xl font-bold text-white">{b.title}</h3>
                  
                  <div className="flex flex-wrap gap-4 text-sm text-slate-400">
                    <div className="flex items-center gap-1.5"><MapPin size={14}/> {b.roomName || 'Sala ' + b.roomId}</div>
                    <div className="flex items-center gap-1.5"><Clock size={14}/> {new Date(b.startAt).toLocaleString('pt-BR')}</div>
                  </div>
                </div>

                {b.status === 'ACTIVE' && (
                  <button onClick={() => handleCancel(b.id)} className="p-2 text-slate-500 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all opacity-0 group-hover:opacity-100">
                    <Trash2 size={20} />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
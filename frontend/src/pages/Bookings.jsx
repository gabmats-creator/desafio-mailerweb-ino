import { useState, useEffect } from 'react';
import { api } from '../api/axios';
import { Plus, Trash2, Users, Clock, MapPin, Edit2, X } from 'lucide-react';
import { Alert } from '../components/Alert';

export function Bookings() {
    const [bookings, setBookings] = useState([]);
    const [rooms, setRooms] = useState([]);

    const [editingId, setEditingId] = useState(null);

    const [formData, setFormData] = useState({ title: '', roomId: '', startAt: '', endAt: '', participants: '' });
    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {
        api.get('/rooms/').then(res => setRooms(res.data.items || []));
        fetchBookings();
    }, []);

    const fetchBookings = async () => {
        const res = await api.get('/bookings/');
        setBookings(res.data.items || []);
    };

    const resetForm = () => {
        setFormData({ title: '', roomId: '', startAt: '', endAt: '', participants: '' });
        setEditingId(null);
        setErrorMessage(null);
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setErrorMessage(null);
        try {
            const payload = {
                ...formData,
                roomId: parseInt(formData.roomId),
                // Tratamento para garantir que participants vire array tanto na criação quanto na edição
                participants: typeof formData.participants === 'string'
                    ? formData.participants.split(',').map(i => i.trim()).filter(i => i !== '')
                    : formData.participants
            };

            // <-- Se tiver editingId, faz PUT. Se não, faz POST.
            if (editingId) {
                await api.put(`/bookings/${editingId}`, payload);
            } else {
                await api.post('/bookings/', payload);
            }

            resetForm();
            fetchBookings();
        } catch (err) {
            const detail = err.response?.data?.detail;
            let message = "Erro inesperado ao processar reserva.";

            if (typeof detail === 'string') {
                message = detail;
            } else if (Array.isArray(detail)) {
                message = detail[0]?.msg || "Erro de validação nos dados enviados.";
            }

            setErrorMessage(message);
            setTimeout(() => setErrorMessage(null), 5000);
        }
    };

    // <-- Função que joga os dados da reserva pro formulário
    const handleEdit = (booking) => {
        setEditingId(booking.id);
        setFormData({
            title: booking.title,
            roomId: booking.roomId,
            startAt: new Date(booking.startAt).toISOString().slice(0, 16),
            endAt: new Date(booking.endAt).toISOString().slice(0, 16),
            participants: booking.participants.join(', ')
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleCancel = async (id) => {
        if (!window.confirm("Deseja cancelar esta reserva?")) return;
        setErrorMessage(null);
        try {
            await api.patch(`/bookings/${id}/cancel`);
            fetchBookings();
        } catch (err) {
            const detail = err.response?.data?.detail;
            let message = "Erro inesperado ao cancelar reserva.";
            if (typeof detail === 'string') message = detail;
            else if (Array.isArray(detail)) message = detail[0]?.msg || "Erro de validação.";

            setErrorMessage(message);
            setTimeout(() => setErrorMessage(null), 5000);
        }
    };

    return (
        <div className="max-w-5xl mx-auto">
            <Alert message={errorMessage} onClose={() => setErrorMessage(null)} />

            <header className="mb-8">
                <h1 className="text-3xl font-bold">Gerenciar Reservas</h1>
                <p className="text-black">Agende reuniões e gerencie horários das salas.</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Formulário */}
                <div className="lg:col-span-5">
                    <form onSubmit={handleCreate} className="bg-slate-800 border border-slate-700 p-6 rounded-2xl space-y-4 sticky top-8">

                        {/* <-- Cabeçalho do formulário dinâmico (Nova vs Editar) */}
                        <div className="flex justify-between items-center mb-2">
                            <h2 className="text-lg font-semibold flex items-center gap-2">
                                {editingId ? (
                                    <><Edit2 size={20} className="text-amber-500" /> Editar Reserva</>
                                ) : (
                                    <><Plus size={20} className="text-blue-500" /> Nova Reserva</>
                                )}
                            </h2>
                            {editingId && (
                                <button type="button" onClick={resetForm} className="text-slate-400 hover:text-white transition-colors">
                                    <X size={20} />
                                </button>
                            )}
                        </div>

                        <input
                            placeholder="Título da Reunião"
                            className="w-full bg-slate-900 border border-slate-700 p-3 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all text-white"
                            onChange={e => setFormData({ ...formData, title: e.target.value })}
                            value={formData.title} required
                        />

                        <select
                            className="w-full bg-slate-900 border border-slate-700 p-3 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none text-white"
                            onChange={e => setFormData({ ...formData, roomId: e.target.value })}
                            value={formData.roomId} required
                        >
                            <option value="">Selecione a Sala</option>
                            {rooms.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
                        </select>

                        <div className="grid grid-cols-2 gap-3">
                            <input type="datetime-local" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-xs text-white"
                                onChange={e => setFormData({ ...formData, startAt: e.target.value })} value={formData.startAt} required />
                            <input type="datetime-local" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-xs text-white"
                                onChange={e => setFormData({ ...formData, endAt: e.target.value })} value={formData.endAt} required />
                        </div>

                        <textarea
                            placeholder="Participantes (e-mail, e-mail...)"
                            className="w-full bg-slate-900 border border-slate-700 p-3 rounded-xl text-sm min-h-[100px] text-white"
                            onChange={e => setFormData({ ...formData, participants: e.target.value })}
                            value={formData.participants} required
                        />

                        {/* <-- Botão dinâmico */}
                        <button className={`w-full font-bold py-3 rounded-xl transition-all shadow-lg text-white ${editingId
                                ? 'bg-amber-600 hover:bg-amber-500 shadow-amber-600/20'
                                : 'bg-blue-600 hover:bg-blue-500 shadow-blue-600/20'
                            }`}>
                            {editingId ? 'Salvar Alterações' : 'Confirmar Reserva'}
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
                                    <span className={`text-[10px] font-bold uppercase px-2 py-1 rounded ${b.status === 'Ativa' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-red-500/10 text-red-500'}`}>
                                        {b.status === 'Ativa' ? 'Ativa' : 'Cancelada'}
                                    </span>
                                    <h3 className="text-xl font-bold text-white">{b.title}</h3>

                                    <div className="flex flex-wrap gap-4 text-sm text-white">
                                        <div className="flex items-center gap-1.5"><MapPin size={14} /> {b.roomName || 'Sala ' + b.roomId}</div>
                                        <div className="flex items-center gap-1.5"><Clock size={14} /> {new Date(b.startAt).toLocaleString('pt-BR')}</div>
                                    </div>
                                    <div className="pt-2 flex flex-wrap gap-1.5 opacity-0 max-h-0 group-hover:opacity-100 group-hover:max-h-20 transition-all duration-300 ease-in-out">
                                        <div className="flex items-center gap-1 text-slate-500 mr-1">
                                            <Users size={12} />
                                            <span className="text-[10px] font-bold uppercase">Participantes:</span>
                                        </div>
                                        {b.participants?.map((email, idx) => (
                                            <span key={idx} className="text-[11px] bg-slate-700 text-slate-300 px-2 py-0.5 rounded-full border border-slate-600">
                                                {email}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                {/* <-- Adicionado o botão de Editar junto com o de Cancelar */}
                                {b.status === 'Ativa' && (
                                    <div className="flex gap-2">
                                        <button onClick={() => handleEdit(b)} title="Editar" className="p-2 text-slate-500 hover:text-amber-500 hover:bg-amber-500/10 rounded-lg transition-all opacity-0 group-hover:opacity-100">
                                            <Edit2 size={20} />
                                        </button>
                                        <button onClick={() => handleCancel(b.id)} title="Cancelar" className="p-2 text-slate-500 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all opacity-0 group-hover:opacity-100">
                                            <Trash2 size={20} />
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
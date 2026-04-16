import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/axios';

export function Dashboard() {
  const navigate = useNavigate();
  
  // Estados para armazenar dados da API
  const [rooms, setRooms] = useState([]);
  const [bookings, setBookings] = useState([]);
  
  // Estados de UX (Loading, Erros e Sucesso)
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [feedback, setFeedback] = useState({ type: '', message: '' });

  // Estado do Formulário de Reserva
  const [formData, setFormData] = useState({
    title: '',
    room_id: '',
    start_at: '',
    end_at: '',
    participants: ''
  });

  // Busca inicial dos dados
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fazemos as duas requisições ao mesmo tempo para ser mais rápido
      const [roomsRes, bookingsRes] = await Promise.all([
        api.get('/rooms/'),
        api.get('/bookings/')
      ]);
      
      // O fastapi-pagination devolve os dados dentro de "items"
      setRooms(roomsRes.data.items || []);
      setBookings(bookingsRes.data.items || []);
    } catch (error) {
      showFeedback('error', 'Erro ao carregar os dados. Verifique sua conexão.');
    } finally {
      setLoading(false);
    }
  };

  const showFeedback = (type, message) => {
    setFeedback({ type, message });
    // Limpa a mensagem após 5 segundos
    setTimeout(() => setFeedback({ type: '', message: '' }), 5000);
  };

  const handleLogout = () => {
    localStorage.removeItem('@MailerWeb:token');
    navigate('/');
  };

  const handleCreateBooking = async (e) => {
    e.preventDefault();
    setActionLoading(true);
    
    try {
      // Converte os emails digitados com vírgula para um Array limpo
      const participantsArray = formData.participants
        .split(',')
        .map(email => email.trim())
        .filter(email => email !== '');

      const payload = {
        ...formData,
        room_id: parseInt(formData.room_id), // Backend exige Int
        participants: participantsArray
      };

      await api.post('/bookings/', payload);
      showFeedback('success', 'Reserva criada com sucesso!');
      
      // Limpa o formulário e recarrega a lista
      setFormData({ title: '', room_id: '', start_at: '', end_at: '', participants: '' });
      fetchData();
    } catch (error) {
      showFeedback('error', error.response?.data?.detail || 'Erro ao criar reserva.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Tem certeza que deseja cancelar esta reserva?')) return;
    
    try {
      await api.patch(`/bookings/${bookingId}/cancel`);
      showFeedback('success', 'Reserva cancelada com sucesso!');
      fetchData(); // Recarrega a lista para mostrar o novo status
    } catch (error) {
      showFeedback('error', error.response?.data?.detail || 'Erro ao cancelar reserva.');
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Carregando dados...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      {/* Navbar Simplificada */}
      <div className="flex justify-between items-center bg-white p-4 rounded-lg shadow mb-6">
        <h1 className="text-xl font-bold text-gray-800">MailerWeb - Dashboard</h1>
        <button onClick={handleLogout} className="text-red-600 font-medium hover:text-red-800">Sair</button>
      </div>

      {/* Alertas de Feedback */}
      {feedback.message && (
        <div className={`p-4 rounded-lg mb-6 text-sm font-medium ${
          feedback.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {feedback.message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* COLUNA DIREITA: Lista de Reservas */}
        <div className="lg:col-span-2">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-black text-lg font-bold mb-4">Minhas Reservas</h2>
            
            {bookings.length === 0 ? (
              <p className="text-gray-500 text-sm">Você ainda não possui reservas cadastradas.</p>
            ) : (
              <div className="space-y-4">
                {bookings.map(booking => {
                  const isActive = booking.status === 'Ativa';
                  return (
                    <div key={booking.id} className={`p-4 border rounded-lg flex justify-between items-center ${isActive ? 'bg-gray-50' : 'bg-red-50 border-red-200'}`}>
                      <div>
                        <h3 className="font-bold text-gray-800">
                          {booking.title} 
                          {!isActive && <span className="ml-2 text-xs text-red-600 bg-red-100 px-2 py-1 rounded">Cancelada</span>}
                        </h3>
                        <p className="text-sm text-gray-600">Sala: {booking.room_name}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {new Date(booking.startAt).toLocaleString()} até {new Date(booking.endAt).toLocaleString()}
                        </p>
                      </div>
                      
                      {isActive && (
                        <div className="flex gap-2">
                          <button 
                            onClick={() => handleCancelBooking(booking.id)}
                            className="text-xs text-red-600 hover:text-red-800 border border-red-600 px-3 py-1 rounded">
                            Cancelar
                          </button>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
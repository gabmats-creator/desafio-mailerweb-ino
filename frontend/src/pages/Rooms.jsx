import { useState, useEffect } from 'react';
import { api } from '../api/axios';
import { Alert } from '../components/Alert'; // 1. Importando o componente de Alerta

export function Rooms() {
  const [rooms, setRooms] = useState([]);
  const [newRoom, setNewRoom] = useState({ name: '', capacity: 0 });
  const [errorMessage, setErrorMessage] = useState(null); // 2. Criando o estado do erro

  useEffect(() => { fetchRooms(); }, []);

  const fetchRooms = async () => {
    try {
      const res = await api.get('/rooms/');
      setRooms(res.data.items || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setErrorMessage(null); // Limpa qualquer erro anterior antes de tentar de novo

    try {
      await api.post('/rooms/', { name: newRoom.name, capacity: parseInt(newRoom.capacity) });
      setNewRoom({ name: '', capacity: 0 });
      fetchRooms();
    } catch (err) {
      // 3. Tratamento blindado contra tela preta
      const detail = err.response?.data?.detail;
      let message = "Erro inesperado ao criar sala.";

      if (typeof detail === 'string') {
        // Se for erro normal (Ex: "Já existe uma sala com este nome")
        message = detail;
      } else if (Array.isArray(detail)) {
        // Se for erro 422 do FastAPI, ele pega a mensagem de dentro do Array
        message = detail[0]?.msg || "Erro de validação nos dados enviados.";
      }

      setErrorMessage(message);
      setTimeout(() => setErrorMessage(null), 5000); // Some depois de 5 segundos
    }
  };

  return (
    <div>
      {/* 4. Inserindo o Alerta no topo */}
      <Alert message={errorMessage} onClose={() => setErrorMessage(null)} />

      <h1 className="text-2xl font-bold mb-6">Gerenciar Salas</h1>
      
      <form onSubmit={handleCreate} className="bg-white p-4 rounded shadow mb-8 flex gap-4 items-end">
        <div>
          <label className="block text-sm text-black">Nome da Sala</label>
          <input className="border p-2 rounded w-64 text-black" value={newRoom.name} 
            onChange={e => setNewRoom({...newRoom, name: e.target.value})} required />
        </div>
        <div>
          <label className="block text-sm text-black">Capacidade</label>
          <input type="number" className="border p-2 rounded w-32 text-black" value={newRoom.capacity} 
            onChange={e => setNewRoom({...newRoom, capacity: e.target.value})} required />
        </div>
        <button className="bg-green-600 text-white px-6 py-2 rounded">Criar Sala</button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {rooms.map(room => (
          <div key={room.id} className="bg-white p-6 rounded shadow border-l-4 border-blue-500">
            <h3 className="font-bold text-lg mb-2 text-blue-500">{room.name}</h3>
            <p className="text-gray-600">Capacidade: {room.capacity} pessoas</p>
            <p className="text-xs text-gray-400 mt-2">ID: {room.id}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
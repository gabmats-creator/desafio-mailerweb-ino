import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/axios';

export function Login() {
  // Controle para alternar entre Login e Cadastro
  const [isLoginMode, setIsLoginMode] = useState(true);
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // Estados de UX
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      if (isLoginMode) {
        // --- FLUXO DE LOGIN (Exige Form Data pelo FastAPI) ---
        const formData = new URLSearchParams();
        formData.append('username', email); 
        formData.append('password', password);

        // O endpoint será resolvido como: http://localhost:8080/mailerweb/v1/users/login
        const response = await api.post('/users/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        localStorage.setItem('@MailerWeb:token', response.data.accessToken);
        navigate('/dashboard');
        
      } else {
        // --- FLUXO DE CADASTRO (Exige JSON padrão) ---
        // Assumindo que a sua rota de criação de usuário é POST /users/
        await api.post('/users/', {
          email: email,
          password: password
        });

        setSuccess('Conta criada com sucesso! Você já pode fazer login.');
        setIsLoginMode(true); // Volta a tela para o modo de Login
        setPassword(''); // Limpa a senha por segurança
      }
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao processar requisição.');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLoginMode(!isLoginMode);
    setError(null);
    setSuccess(null);
    setPassword(''); // Limpa a senha ao trocar de tela
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        
        <h1 className="text-2xl font-bold text-center mb-2 text-gray-800">
          MailerWeb
        </h1>
        <p className="text-center text-sm text-gray-500 mb-6">
          {isLoginMode ? 'Entre com sua conta para continuar' : 'Crie sua conta gratuitamente'}
        </p>
        
        {/* Alertas de Feedback */}
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}
        {success && <div className="bg-green-100 text-green-700 p-3 rounded mb-4 text-sm">{success}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">E-mail</label>
            <input 
              type="email" 
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Senha</label>
            <input 
              type="password" 
              required
              minLength={isLoginMode ? 1 : 6} // No cadastro, exige senha maior
              className="mt-1 text-black block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className={`w-full text-white p-2 rounded-md transition-colors disabled:opacity-50 ${
              isLoginMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            {loading ? 'Processando...' : (isLoginMode ? 'Entrar' : 'Criar Conta')}
          </button>
        </form>

        {/* Botão para alternar entre Login e Cadastro */}
        <div className="mt-6 text-center">
          <button 
            onClick={toggleMode}
            type="button"
            className="text-sm text-blue-600 hover:underline"
          >
            {isLoginMode 
              ? 'Não tem uma conta? Cadastre-se' 
              : 'Já tem uma conta? Faça login'}
          </button>
        </div>

      </div>
    </div>
  );
}
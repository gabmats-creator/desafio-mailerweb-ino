import { useNavigate, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, DoorOpen, CalendarDays, LogOut } from 'lucide-react';

export function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('@MailerWeb:token');
    navigate('/');
  };

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Salas', path: '/rooms', icon: <DoorOpen size={20} /> },
    { name: 'Reservas', path: '/bookings', icon: <CalendarDays size={20} /> },
  ];

  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col h-screen sticky top-0">
      <div className="p-8">
        <h1 className="text-xl font-black tracking-tighter text-blue-500 italic">MAILER<span className="text-white">WEB</span></h1>
      </div>
      
      <nav className="flex-1 px-4 space-y-2">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all ${
              location.pathname === item.path 
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' 
              : 'text-slate-400 hover:bg-slate-900 hover:text-white'
            }`}
          >
            {item.icon}
            {item.name}
          </Link>
        ))}
      </nav>

      <button 
        onClick={handleLogout} 
        className="m-4 flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all border border-transparent hover:border-red-400/20"
      >
        <LogOut size={20} />
        Sair
      </button>
    </aside>
  );
}
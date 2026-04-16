import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Rooms } from './pages/Rooms';
import { Bookings } from './pages/Bookings';
import { Sidebar } from './components/Sidebar';

function Layout({ children }) {
  const isAuthenticated = !!localStorage.getItem('@MailerWeb:token');
  if (!isAuthenticated) return <Navigate to="/" />;

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/rooms" element={<Layout><Rooms /></Layout>} />
        <Route path="/bookings" element={<Layout><Bookings /></Layout>} />
      </Routes>
    </BrowserRouter>
  );
}
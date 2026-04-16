import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { Login } from './Login';
import { api } from '../api/axios';

vi.mock('../api/axios');

const mockedNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockedNavigate,
  };
});

describe('Testes da Tela de Login', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  test('Deve realizar o fluxo básico de login com sucesso', async () => {
    api.post.mockResolvedValueOnce({
      data: { accessToken: 'fake-jwt-token' }
    });

    // Usamos o container para fazer queries brutas no HTML
    const { container } = render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    // Selecionamos os inputs pelo tipo
    const emailInput = container.querySelector('input[type="email"]');
    const passwordInput = container.querySelector('input[type="password"]');

    fireEvent.change(emailInput, { target: { value: 'teste@teste.com' } });
    fireEvent.change(passwordInput, { target: { value: '123456' } });
    
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalled();
      expect(localStorage.getItem('@MailerWeb:token')).toBe('fake-jwt-token');
      expect(mockedNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });
});
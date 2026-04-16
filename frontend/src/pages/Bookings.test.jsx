import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { Bookings } from './Bookings';
import { api } from '../api/axios';

vi.mock('../api/axios');

describe('Testes da Tela de Reservas', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    
    api.get.mockImplementation((url) => {
      if (url === '/rooms/') return Promise.resolve({ data: { items: [{ id: 1, name: 'Sala 1', capacity: 10 }] } });
      if (url === '/bookings/') return Promise.resolve({ data: { items: [] } });
      return Promise.resolve({ data: { items: [] } });
    });
  });

  test('Deve criar uma reserva com sucesso (Integração de Criação)', async () => {
    api.post.mockResolvedValueOnce({ status: 201 });

    const { container } = render(<Bookings />);

    await waitFor(() => expect(screen.getByText('Sala 1')).toBeInTheDocument());

    fireEvent.change(screen.getByPlaceholderText(/Título da Reunião/i), { target: { value: 'Reunião Importante' } });
    
    const selects = screen.getAllByRole('combobox');
    fireEvent.change(selects[0], { target: { value: '1' } }); 

    // === CORREÇÃO: Preenchendo as datas para passar no "required" do HTML ===
    const dateInputs = container.querySelectorAll('input[type="datetime-local"]');
    fireEvent.change(dateInputs[0], { target: { value: '2026-04-16T10:00' } });
    fireEvent.change(dateInputs[1], { target: { value: '2026-04-16T11:00' } });
    // =======================================================================

    fireEvent.change(screen.getByPlaceholderText(/Participantes/i), { target: { value: 'joao@teste.com' } });
    
    fireEvent.click(screen.getByRole('button', { name: /Confirmar Reserva/i }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalled();
    });
  });

  test('Deve exibir erro de conflito se a sala já estiver ocupada', async () => {
    api.post.mockRejectedValueOnce({
      response: { data: { detail: 'Já existe uma reserva neste horário para esta sala.' } }
    });

    const { container } = render(<Bookings />);

    await waitFor(() => expect(screen.getByText('Sala 1')).toBeInTheDocument());

    fireEvent.change(screen.getByPlaceholderText(/Título da Reunião/i), { target: { value: 'Reunião Duplicada' } });
    
    const selects = screen.getAllByRole('combobox');
    fireEvent.change(selects[0], { target: { value: '1' } });

    // === CORREÇÃO: Preenchendo as datas aqui também ===
    const dateInputs = container.querySelectorAll('input[type="datetime-local"]');
    fireEvent.change(dateInputs[0], { target: { value: '2026-04-16T14:00' } });
    fireEvent.change(dateInputs[1], { target: { value: '2026-04-16T15:00' } });
    
    fireEvent.change(screen.getByPlaceholderText(/Participantes/i), { target: { value: 'maria@teste.com' } });

    fireEvent.click(screen.getByRole('button', { name: /Confirmar Reserva/i }));

    await waitFor(() => {
      expect(screen.getByText('Já existe uma reserva neste horário para esta sala.')).toBeInTheDocument();
    });
  });
});
# 🏢 Meeting Room Booking + Async Notification System

Uma aplicação Fullstack completa para gerenciamento de reservas de salas, desenvolvida como solução para o desafio técnico. O sistema conta com validações rigorosas de conflitos de horário e um motor de mensageria assíncrono blindado contra falhas, utilizando o Padrão Outbox.

## 🚀 Tecnologias Utilizadas

**Backend:**
- Python 3.10+
- FastAPI (Alta performance e tipagem assíncrona)
- SQLAlchemy 2.0 (ORM Assíncrono)
- PostgreSQL (Banco de Dados)
- Pytest (Testes Automatizados com AsyncMock)

**Frontend:**
- React (Vite)
- Tailwind CSS (Estilização responsiva)
- Lucide React (Ícones)
- Vitest + React Testing Library (Testes Automatizados)

**Infraestrutura:**
- Docker & Docker Compose

---

## 🧠 Decisões Técnicas e Arquitetura

Para atender aos requisitos de alta concorrência e resiliência, as seguintes decisões arquiteturais foram tomadas:

### 1. Prevenção de Conflitos e Overbooking (Concorrência)
Para garantir que duas reservas não ocupem o mesmo espaço, a verificação de *overlap* foi delegada ao banco de dados utilizando consultas por intervalo (`new_start < existing_end AND new_end > existing_start`). Associado ao nível de isolamento de transações do banco, isso previne condições de corrida (*race conditions*) durante requisições simultâneas.

### 2. Padrão Outbox + Transação Atômica (Mensageria Segura)
Para evitar o problema clássico de "A reserva foi salva, mas a notificação falhou" (ou vice-versa), foi implementado o **Padrão Outbox**. 
* Utilizando o *Repository Pattern*, a inserção da `Reserva` e a inserção do `OutboxEvent` ocorrem na mesma transação atômica (`commit` único). 
* Se o banco de dados cair milissegundos antes da notificação ser registrada, o *Rollback* cancela a reserva, garantindo consistência absoluta dos dados.

### 3. Worker Idempotente
O envio de e-mails é processado de forma assíncrona por um Worker isolado. Ele busca apenas eventos com status `PENDING` e os atualiza para `PROCESSED` na mesma operação. Essa **idempotência** garante que, mesmo que o worker sofra reinicializações forçadas ou realize *retries*, um participante jamais receberá o mesmo e-mail duas vezes.

### 4. Tratamento Universal de Timezones
Para eliminar bugs de fuso horário entre o navegador do usuário (BRT) e o servidor em contêiner (UTC), o Frontend foi programado para injetar explicitamente o sufixo ISO 8601 (`Z` - *Zulu Time*) no payload. O backend salva estritamente em UTC e o React renderiza na hora local, eliminando o clássico erro de "reserva pulando 3 horas".

---

## ⚙️ Variáveis de Ambiente

Localmente, o arquivo settings.py tem todas as variáveis necessárias para que uma execução teste
seja realizada

---

## 🛠️ Como Executar o Projeto

A aplicação inteira está orquestrada via Docker. Você não precisa instalar nada além do **Docker** e do **Docker Compose** na sua máquina.

### 1. Subindo a Aplicação
Na raiz do projeto, execute o comando abaixo para construir as imagens e subir os contêineres:

```bash
docker-compose up --build -d
```

Este comando iniciará simultaneamente:
- O Banco de Dados (PostgreSQL) na porta `5432`
- O Backend (API) na porta `8080`
- O Frontend (React) na porta `5173`
- O Worker de E-mails (Processo em background)

### 2. Acessando os Serviços
- **Frontend:** Abra `http://localhost:5173` no seu navegador.
- **Backend (Swagger UI):** Acesse `http://localhost:8080/mailerweb/v1/docs` para interagir com a documentação interativa da API.
- **Banco de dados PostgreSQL:** Acesse um SGBD(Datagrip, PGAdmin, DBeaver...), informando host=localhost, port=5433, user=mailer_user, password=mailer_pass e database=mailerweb_db, será possível visualizar as tabelas criadas e suas respectivas colunas e registros

## 🧪 Como Rodar os Testes

Os testes garantem o funcionamento rigoroso das regras de negócio (Backend) e a fluidez da experiência do usuário (Frontend).

**Para rodar os testes do Backend (Pytest):**
Garante validação de datas, proteção de rotas, transações atômicas e idempotência do worker.
```bash
docker-compose exec api pytest -v
```

**Para rodar os testes do Frontend (Vitest):**
Valida os fluxos de renderização de interface, formulários, alertas e chamadas da API (`axios` mockado).
```bash
docker-compose exec frontend npm run test
```
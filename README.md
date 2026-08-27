# DRF Schedule Manager

**DRF Schedule Manager** é uma aplicação desenvolvida para automatizar e simplificar o gerenciamento de consultas clínicas. 

A plataforma permite o cadastro de especialistas e a definição de suas grades de trabalho (dias, horários e quantidade de vagas).

Os pacientes interagem com uma interface, onde podem visualizar a disponibilidade e agendar consultas. O sistema conta com autenticação JWT e validações para garantir a integridade dos dados, impedindo sobreposição de agendas e bloqueando reservas duplicadas no mesmo horário.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Django, Django REST Framework
- **Frontend:** Vue.js
- **Banco de Dados:** PostgreSQL
- **Infraestrutura:** Docker, Docker Compose, Makefile

---

## ⚙️ Pré-requisitos
Para rodar o projeto, você precisará ter instalado em sua máquina:
- **Docker** e **Docker Compose**
- **Make** *(Opcional, mas recomendado para o uso dos atalhos)*

Para verificar se o `make` já está instalado, rode no terminal:
```bash
make --version
```
Caso não esteja instalado (distribuições baseadas em Debian/Ubuntu), instale rapidamente com:
```bash
sudo apt update && sudo apt install make -y
```
---

## 🚀 Como Executar o Projeto

**1. Clone o repositório e acesse a pasta:**
```bash
git clone <url-do-repositorio>
cd drf-schedule-manager
```

**2. Suba a infraestrutura completa:**

Este comando constrói as imagens e sobe os containers em segundo plano. As migrações do banco de dados são executadas automaticamente na inicialização.

Usando **Make**:
```bash
make up
```

Ou usando o comando nativo do **Docker**:
```bash
docker compose up --build -d
```

**3. Popule o banco de dados**

Este passo cria dados iniciais de teste (especialistas, pacientes e superusuario) e exibe no terminal todos os links e senhas de acesso.

Usando **Make**:
```bash
make setup
```

Ou usando o comando nativo do **Docker**:
```bash
docker compose exec web python manage.py setup_teste
```

**4. Acompanhe os logs da aplicação (Opcional):**

Este comando conecta o terminal à saída dos containers, permitindo visualizar as requisições da aplicação tempo real.

Usando **Make**:
```bash
make logs
```

Ou usando o comando nativo do **Docker**:
```bash
docker compose logs -f
```
> 💡 **Nota:** Para sair da visualização dos logs e liberar o terminal, basta pressionar `Ctrl + C`.

**5. Execute os testes automatizados (Opcional):**

Este comando roda a suíte de testes unitários do backend para validar as regras de negócio e os bloqueios da API.

Usando **Make**:
```bash
make test
```

Ou usando o comando nativo do **Docker**:
```bash
docker compose exec web python manage.py test
```

---

## 💻 Comandos Adicionais

Além dos passos principais do fluxo de execução, o projeto conta com comandos auxiliares no `Makefile`. Abaixo está a tabela de equivalência com os comandos nativos do Docker:

| Ação | Comando via `make` | Comando nativo (Docker) |
| :--- | :--- | :--- |
| **Exibir ajuda dos comandos** | `make help` | *N/A* |
| **Parar e limpar containers/volumes** | `make down` | `docker compose down -v` |
| **Ver logs específicos da API (Django)** | `make logs-web` | `docker compose logs -f web` |
| **Ver logs específicos do Banco de Dados**| `make logs-db` | `docker compose logs -f db` |
| **Ver logs específicos do Front-End** | `make logs-frontend`| `docker compose logs -f frontend` |
| **Aplicar migrações do Django** | `make migrate` | `docker compose exec web python manage.py migrate` |
| **Criar superusuário manualmente** | `make superuser` | `docker compose exec web python manage.py createsuperuser` |

## 🔑 Credenciais e Acessos

Utilize as informações abaixo para fazer os testes manuais após subir a aplicação na sua máquina:

### 🌐 Links Rápidos
- **Front-End (Vue):** [http://localhost:5173](http://localhost:5173)
- **API Base URL:** [http://localhost:8000/api/](http://localhost:8000/api/)
- **API Docs (Swagger):** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Admin Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 👤 Login

**Administrador (Pode acessar o Admin Django, criar especialistas e agendas):**
- **Login:** `admin`
- **Senha:** `admin123`

**Pacientes (Podem acessar a interface e reservar consultas):**
- **Logins:** `paciente1`, `paciente2` ou `paciente3`
- **Senha:** `senha123`

## ✒️ Autor
Desenvolvido por **Thalysson Delano**.
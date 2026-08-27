help:
	@echo "Comandos disponíveis:"
	@echo "  make up            - Sobe a aplicação completa (Docker build e up)"
	@echo "  make down          - Para a aplicação e remove os containers e volumes"
	@echo "  make setup         - Popula o banco de dados com alguns dados iniciais para teste"
	@echo "  make logs          - Mostra os logs de TODOS os serviços juntos"
	@echo "  make logs-web      - Mostra apenas os logs do Backend (Django)"
	@echo "  make logs-db       - Mostra apenas os logs do Banco de Dados (Postgres)"
	@echo "  make logs-frontend - Mostra apenas os logs do Front-End"
	@echo "  make migrate       - Roda as migrações do Django"
	@echo "  make superuser     - Cria um superusuário"
	@echo "  make test          - Executa os testes automatizados"

.PHONY: up down setup logs logs-web logs-db logs-frontend superuser migrate test help

up:
	docker compose up --build -d

down:
	docker compose down -v

setup:
	docker compose exec web python manage.py setup_teste

logs:
	docker compose logs -f

logs-web:
	docker compose logs -f web

logs-db:
	docker compose logs -f db

logs-frontend:
	docker compose logs -f frontend

migrate:
	docker compose exec web python manage.py migrate

superuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web python manage.py test
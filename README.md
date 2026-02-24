# Modular ERP System

> **Architecture:** FastAPI Microservices  
> **Database:** PostgreSQL 16  
> **Queue:** RabbitMQ  
> **Cache:** Redis

## Quick Start

```bash
# 1. Clone and enter
git clone <repo-url> && cd erp-system

# 2. Copy environment
cp .env.example .env

# 3. Start infrastructure + services
docker compose up -d

# 4. Verify
docker compose ps
```

## Services

| Service | Port | Description |
|---|---|---|
| **Gateway** | 8000 | API Gateway — routing, JWT validation, CORS |
| **Auth** | 8001 | Registration, login, JWT tokens |
| **RBAC** | 8002 | Roles, permissions, access control |
| **Quotation** | 8003 | Quotation management, PDF export |
| **Invoice** | 8004 | Invoice management, payments |
| **Inventory** | 8005 | Products, stock levels, movements |
| **HRIS** | 8006 | Employees, attendance, leave, payroll |
| **Notification** | 8007 | Event-driven notifications (in-app + email) |

## Infrastructure

| Service | Port | Credentials |
|---|---|---|
| PostgreSQL | 5432 | `erp_user` / `erp_password` |
| Redis | 6379 | — |
| RabbitMQ | 5672 (AMQP), 15672 (UI) | `guest` / `guest` |

## Makefile Commands

```bash
make up                    # Start all containers
make down                  # Stop all containers
make build                 # Rebuild images
make logs service=auth     # Tail service logs
make test service=auth     # Run service tests
make migrate service=auth  # Run Alembic migrations
make shell service=auth    # Open shell in container
make ps                    # List running containers
make clean                 # Stop + remove volumes
```

## Project Structure

```
erp-system/
├── docker-compose.yml
├── Makefile
├── .env / .env.example
├── backend/
│   ├── shared/            # Shared utilities (DB, auth, messaging)
│   ├── gateway/           # API Gateway (port 8000)
│   ├── auth/              # Auth Service (port 8001)
│   ├── rbac/              # RBAC Service (port 8002)
│   ├── quotation/         # Quotation Service (port 8003)
│   ├── invoice/           # Invoice Service (port 8004)
│   ├── inventory/         # Inventory Service (port 8005)
│   ├── hris/              # HRIS Service (port 8006)
│   └── notification/      # Notification Service (port 8007)
├── frontend/              # Next.js frontend (TBD)
└── docs/
```

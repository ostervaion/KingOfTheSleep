# Full-Stack Docker Project

| Service    | Technology      | Internal address     |
|------------|-----------------|----------------------|
| `db`       | PostgreSQL 16   | `db:5432`            |
| `backend`  | FastAPI         | `backend:8000`       |
| `frontend` | Vue 3 + Vite    | `frontend:5173`      |
| `server`   | Caddy 2         | `localhost:80`       |

Caddy is the single public entry point. All traffic arrives on port 80 (or 443 in production), and Caddy reverse-proxies:

- `/api/*` → FastAPI backend (strips the `/api` prefix)
- everything else → Vue frontend

---

## Quick start

```bash
# 1. Create your .env file
make env

# 2. Build and start everything
make up-build

# 3. Open http://localhost
```

---

## Common commands

| Command               | Description                                      |
|-----------------------|--------------------------------------------------|
| `make up`             | Start all services (detached)                    |
| `make up-build`       | Build images, then start                         |
| `make down`           | Stop and remove containers                       |
| `make down-volumes`   | Stop containers + delete volumes (data loss!)    |
| `make logs`           | Tail all logs                                    |
| `make logs-backend`   | Tail backend logs only                           |
| `make ps`             | Container status                                 |
| `make shell-backend`  | Bash shell in the backend container              |
| `make shell-db`       | psql session in the db container                 |
| `make db-dump`        | Dump DB to `db/backup.sql`                       |
| `make db-restore`     | Restore DB from `db/backup.sql`                  |
| `make build-no-cache` | Full rebuild without cache                       |
| `make clean`          | Remove containers + local images + build cache   |
| `make help`           | List all available targets                       |

---

## Project layout

```
.
├── Makefile
├── docker-compose.yml
├── .env.example
├── db/
│   ├── Dockerfile
│   └── init/
│       └── 01_schema.sql       # Runs on first boot
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── requirements.txt
│   └── routers/
│       └── items.py
├── frontend/
│   ├── Dockerfile              # Multi-stage: dev / build / production
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.js
│       └── App.vue
└── server/
    ├── Dockerfile
    └── Caddyfile
```

---

## Resources

These are real references and official documentation links for the technologies used in this project:

- Vue 3 documentation: https://vuejs.org/guide/introduction.html
- Vite documentation: https://vite.dev/guide/
- Pinia documentation: https://pinia.vuejs.org/
- Tailwind CSS documentation: https://tailwindcss.com/docs/installation
- Axios documentation: https://axios-http.com/docs/intro
- Phaser 3 documentation: https://phaser.io/docs/3.80.0/index
- FastAPI documentation: https://fastapi.tiangolo.com/
- SQLModel documentation: https://sqlmodel.tiangolo.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/
- PyJWT documentation: https://pyjwt.readthedocs.io/en/stable/
- Docker Compose documentation: https://docs.docker.com/compose/
- Caddy documentation: https://caddyserver.com/docs/
- MDN WebSockets API: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

---

## Production switch

1. In `.env` set `FRONTEND_BUILD_TARGET=production`.
2. In `server/Caddyfile` change `frontend:5173` → `frontend:80`.
3. Uncomment and configure the HTTPS block in `Caddyfile`.
4. Run `make up-build`.

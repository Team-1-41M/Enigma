# Enigma

- [Launching](#launching)
  - [Local](#local)
    - [Client](#client)
    - [Server](#server)
  - [Docker Compose](#docker-compose)

## Launching

### Local

Create .env file in project root:
```
DEBUG=True

NUXT_HOST=127.0.0.1
NUXT_PORT=3000
API_BASE_URL=127.0.0.1:8000

SERVER_HOST=127.0.0.1
SERVER_PORT=8000
SERVER_RELOAD=True

HTTPS=False
SECRET="fastapi-secure-q6&gtanz!$%5g%p8fthuwi#a3p))$+%+g-r6d(fb2h+a9ne414"

SUPERUSER_NAME=root
SUPERUSER_EMAIL=root@example.com
SUPERUSER_PASSWORD=Master#chew123_$

CACHE_TYPE=dict

DB_ENGINE=sqlite+aiosqlite
DB_NAME=enigma.sqlite3
```

#### Client
Install dependencies:
```bash
npm i
```

Launch:
```bash
npx nuxi dev --dotenv ../.env
```

After that you can visit ```http://NUXT_HOST:NUXT_PORT``` to see client app.

#### Server
You need to install Python (used 3.12).

Create virtual environment and activate it:
```bash
python -m venv ./server/.venv

source ./server/.venv/bin/activate # Linux

.\server\.venv\Scripts\activate # Windows
```

Install base (FastAPI, ORM, etc.) and local (SQLite) requirements:
```bash
pip install -r ./server/requirements/base.txt -r ./server/requirements/local.txt
```

Launch:
```bash
python ./server/run.py
```

After that you can visit ```http://SERVER_HOST:SERVER_PORT/docs``` in your browser to get the API specification.

### Docker Compose

Configure .env file in project root:
```
DEBUG=True

NUXT_HOST=0.0.0.0
NUXT_PORT=3000
API_BASE_URL=0.0.0.0:8000

SERVER_HOST=0.0.0.0
SERVER_PORT=8000
SERVER_RELOAD=True

HTTPS=False
SECRET="fastapi-secure-q6&gtanz!$%5g%p8fthuwi#a3p))$+%+g-r6d(fb2h+a9ne414"

SUPERUSER_NAME=root
SUPERUSER_EMAIL=root@example.com
SUPERUSER_PASSWORD=Master#chew123_$

CACHE_TYPE=redis
CACHE_HOST=cache
CACHE_PORT=6379
CACHE_DB=0

DB_ENGINE=postgresql+asyncpg
DB_NAME=enigma
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=database
DB_PORT=5432
```

Launch:
```bash
docker compose up --build
```
Docker will start a whole project, you can check it at localhost:some_port (for example, 8000 for the server and 3000 for the client).

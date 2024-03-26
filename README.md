# Enigma

## Launching

### Local

#### Server
You need to install Python (used 3.12).

In server directory, create virtual environment and activate it:
```
$ python -m venv .venv

$ source .venv/bin/activate # Linux

$ .venv\Scripts\activate # Windows
```

Install base (FastAPI, ORM, etc.) and local (SQLite) requirements:
```
$ pip install -r requirements/base.txt -r requirements/local.txt
```

Configure .env file in project root:
```
DEBUG=True

NUXT_HOST=127.0.0.1
NUXT_PORT=3000
API_BASE_URL=127.0.0.1:8000

SERVER_HOST=127.0.0.1
SERVER_PORT=8000
SERVER_RELOAD=True

HTTPS=False
CORS_ALLOWED_ORIGINS=127.0.0.1:3000

SUPERUSER_NAME=root
SUPERUSER_EMAIL=root@example.com
SUPERUSER_PASSWORD=Master#chew123_$

CACHE_TYPE=dict

DB_ENGINE=sqlite+aiosqlite
DB_NAME=enigma.sqlite3
```

Launch:
```
$ python run.py
```
After that you can visit server_address_in_dotenv/docs in your browser to get the API specification.

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
CORS_ALLOWED_ORIGINS=0.0.0.0:3000

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
```
$ docker compose up --build
```
Docker will start a whole project, you can check it at localhost:some_port (for example, 8000 for the server and 3000 for the client).

## Testing

### Server

Testing was done using pytest.

Install it (and some instruments for linting and formatting) in your activated venv:
```
$ pip install -r requirements/test.txt
```

Launch:
```
$ pytest
```
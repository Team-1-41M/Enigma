# Enigma
## Launching
### Server
You need to install Python (used 3.12).

Create virtual environment and activate it:
```
python -m venv server/.venv

# For Linux
server/.venv/bin/activate

# For Windows
server\.venv\Scripts\activate 
```

Install requirements:
```
pip install -r server/requirements.txt
```

Configure .env file in project root. For example:
```
HOST=127.0.0.1
PORT=8000
DEBUG=True
RELOAD=True
DB_URL=sqlite+aiosqlite:///enigma.sqlite3
```

Launch:
```
python server/run.py
```
After that you can visit 127.0.0.1:8000/docs 
in your browser to get the API specification.
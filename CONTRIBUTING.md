# Contributing

Each contributor works in his own fork in a branch with his own feature. At the end of the work, create a pull request to receive changes into the ```master``` branch of the main repository.

In each branch, run the linting tool and tests.

The ```master``` branch of the main repository builds Docker images of the client and server.

## Code style and quality

### Server

Follow [PEP-8](https://peps.python.org/pep-0008/).

To control your code quality you can install some instruments to your activated venv:
```bash
pip install -r ./server/requirements/test.txt
```

Run formatter:
```bash
ruff check --fix ./server
```

Test your code:
```bash
python -m pytest ./server
```
Don't forget configure .env in project root for tests.
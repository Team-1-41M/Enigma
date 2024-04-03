# Contributing

Each contributor works in his own fork in a branch with his own feature. At the end of the work, create a pull request to receive changes into the ```master``` branch of the main repository.

In each branch, run the linting tool and tests.

The ```master``` branch of the main repository builds Docker images of the client and server.

## Code style and quality

### Server

Follow PEP-8.

To control your code quality you can install some instruments to your activated venv:
```cmd
$ pip install -r ./server/requirements/test.txt
```

Run formatter:
```cmd
$ ruff check --fix ./server
```

Test your code:
```cmd
$ python -m pytest ./server
```
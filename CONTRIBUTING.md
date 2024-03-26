# Contributing

Each contributor works in his own fork in a branch with his own feature. At the end of the work, create a pull request to receive changes into the ```master``` branch of the main repository.

In each branch, run the linting tool and tests.

The ```master``` branch of the main repository builds Docker images of the client and server.

## Code style

### Server

Follow PEP-8.

Before you make a pull request, please, run:
```cmd
$ ruff check --fix .
```

Also test your code by pytest:
```cmd
$ pytest ./server/
```
All of these packages can be installed in your activated venv:
```cmd
$ pip install -r ./server/requirements/test.txt
```
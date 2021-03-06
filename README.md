# json api template

A general purpose json api template.

## Development Setup (required)

This project makes heavy use of docker, so the following tools are the only ones required for building the project in a basic fashion:

- docker
- docker-compose

## Development Setup (optional)

If you want to setup more complex development tooling (editor auto-complete, linters, debugging, etc) then you will also want to install any / all of the following:

- homebrew via https://brew.sh/, and the following homebrew installed tools via `brew install $tool`
  - postgres
  - python@3.8
- the above python install above comes with pip, and via pip you will also want to **globally** install the following via `pip install $tool`
  - pipenv
  - pylint
  - black
- finally, run `make dev` to initialize a **local** installation of all of the above dev tools

## Development Workflow

The most common commands are listed in the `Makefile`, and are run via `make test`, `make run`, etc etc.

More esoteric commands are listed in the `./scripts/` folder, you will generally not need to run these directly unless instructed to do so / you personally know that you need to do so. They are run like so: `./scripts/check_docker.sh`.

## Project Layout

```python
# [ database layer ]
#
# - connection.py
# - models.py
#
# [ migrations layer ]
#
# - env.py
# - versions/*.py
#
# [ server layer ]
#
# - app.py
#   - errors.py
#   - routes.py
#     - views.py
#       - schema.py
#   - controller.py
#
# [ tests layer ]
#
# - test_controller.py
#
```

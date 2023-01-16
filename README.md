# PET-project-backend

**Backend API for the PET-project to manage the data of User, Pet, and Walker entities.**


## Build the application

### Pre-requisites

- Python 3.8+
- Poetry - dependency management and packaging tool

**Steps**

- `poetry install`

## Run the application / special scripts

The pyproject.toml file contains  prepared script that can be run like: `poetry run <script-name>`.

Scripts:

- code_formatter - Format the source code according to python standards.
- linter - Run linter to reveal errors, bugs, stylist issues, suspicious constructs, etc.
- unittest - Run unit tests.
- server-dev - Start the server in development mode.
- server-debug - Start the server in development mode with debugging option.
- server-prod - Start the server in production mode.

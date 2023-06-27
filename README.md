# PET-project-backend

**Backend API for the PET-project to manage the data of User, Pet, and Walker entities.**

###### About the project
![](https://img.shields.io/badge/Python-3.8+-blue)
![](https://img.shields.io/badge/Flask-2.2.2-orange)
![](https://img.shields.io/badge/Flask--restx-1.1.0-orange)
![](https://img.shields.io/badge/Flask--sqlalchemy-3.0.2-orange)
![](https://img.shields.io/badge/Poetry-1.5.1-lightblue)
![](https://img.shields.io/badge/Docker-python:3.8--slim-success)

## Pre-requisites to run the Application

- **Python 3.8+**
  - check by get the current Python version: `python --version` or `python -V`<br>
  *Depending on your operating system and its version python might be installed as: py, python, python3 or some
    specific version python3.8, etc.*
  - if python is not installed, or you have an older version you need to install it:
    - for windows check the [**Python Releases for Windows**](https://www.python.org/downloads/windows/)
    - for linux run the following commands:
      ```
      [optional] sudo apt-get update && upgrade
      sudo apt-get install software-properties-common
      sudo add-apt-repository ppa:deadsnakes/ppa
      sudo apt-get update
      sudo apt-get install python3.8
      ```
 - for more information check the [**official website of Python**](https://www.python.org/downloads/)
- **Poetry** - dependency management and packaging tool
  - check the current poetry version: `poetry version`
  - if poetry is not installed you need install it:
    - for **Linux, macOS, Windows (WSL)**: `curl -sSL https://install.python-poetry.org | python3 -` (*replace python3
      with the name of your python*)
    - for **Windows (Powershell)**: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
    - for more information check the [**official website of Poetry**](https://python-poetry.org/docs/)

## Run the Application

Before you can run the application you need to install the dependencies.<br>

**Steps**
- Open a terminal/console window and navigate to the application folder
- Install the dependencies by running: `poetry install`
- Start the application: `poetry run server-dev`

The pyproject.toml file contains other prepared scripts that can be run like: `poetry run <script-name>`.

**Scripts**

- *code_formatter* - Format the source code according to python standards.
- *linter* - Run linters and static code analyzers to reveal errors, bugs, suspicious constructs, etc.
- *unittest* - Run unit tests.
- *local_check* - Run all 3 previous commands that check for styling and code standards, scan for lint issues and reveal potential bugs to ensure consistent, high-quality code.
- *build* - Build the project artifact used for deployment purposes.
- *dev-server* - Start the db server and the application server in development mode.
- *prod-server* - Start the server in production mode. (coming soon..)

## Useful commands

- **export dependencies** - `poetry export -f requirements.txt --output requirements.txt`

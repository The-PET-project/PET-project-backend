# PET-project-backend

**Backend API for the PET-project to manage the data of User, Pet, and Walker entities.**



## Pre-requisites to run the Application

- **Python 3.8+**
  - check by get the current Python version: `python --version` or `python -V`<br>
  *Depending on your operating system and its version python might be installed as: py, python, python3 or some 
    specific version python3.8, etc.*  
  - if python is not installed or you have an older version you need to install it:
    - for windows check the [Python Releases for Windows](https://www.python.org/downloads/windows/) 
    - for linux run the following commands:
      ```
      sudo apt-get update && upgrade
      sudo apt-get install software-properties-common
      sudo add-apt-repository ppa:deadsnakes/ppa
      sudo apt-get update
      sudo apt-get install python3.8
      ```
 - for more information check the [official website](https://www.python.org/downloads/)
- **Poetry** - dependency management and packaging tool
  - check the current poetry version: `poetry version`
  - if poetry is not installed you need install it:
    - for **Linux, macOS, Windows (WSL)**: `curl -sSL https://install.python-poetry.org | python3 -` (*replace python3 
      with the name of your python*)
    - for **Windows (Powershell)**: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
    - for more information check the [official website](https://python-poetry.org/docs/)

## Run the Application

Before you can run the application you need to install the dependencies.<br>

**Steps**
- Open a terminal/console window and navigate to the application folder
- Install the dependencies by runiing: `poetry install`
- Start the application: `poetry run server-dev`

The pyproject.toml file contains other prepared scripts that can be run like: `poetry run <script-name>`.

**Scripts**

- *code_formatter* - Format the source code according to python standards.
- *linter* - Run linter to reveal errors, bugs, stylist issues, suspicious constructs, etc.
- *unittest* - Run unit tests.
- *server-dev* - Start the server in development mode.
- *server-debug* - Start the server in development mode with debugging option.
- *server-prod* - Start the server in production mode.

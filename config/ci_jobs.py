import os
import logging
import shutil

SOURCE_FOLDER = 'pet_project_backend'
LOGGER = logging.getLogger(__name__)


def safe_run(command: str):
    """Helper function for running OS commands."""
    exit_code = os.system(command)
    if exit_code != 0:
        LOGGER.warning("Running the following system command has been failed. Command: %s" % command)
    return exit_code


def code_formatter():
    safe_run(f"python -m black {SOURCE_FOLDER}")


def linter():
    safe_run(f"python -m pylint {SOURCE_FOLDER}/ tests/")


def run_unittest():
    safe_run("python -m pytest tests/unit")


def build():
    shutil.rmtree('dist')
    safe_run("poetry build")


def start_dev_server():
    safe_run(f"docker-compose --env-file ./.env.dev up")


def start_prod_server():
    safe_run("echo WARNING: 'Production server is not ready to start!'")

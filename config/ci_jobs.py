import logging
import os
import shutil

SOURCE_FOLDER = "pet_project_backend"
LOGGER = logging.getLogger(__name__)


def safe_run(command: str):
    """Helper function for running OS commands."""
    exit_code = os.system(command)
    if exit_code != 0:
        LOGGER.warning("Running the following system command has been failed. Command: %s" % command)
    return exit_code


def code_formatter():
    safe_run("pre-commit run --hook-stage pre-commit --all-files")


def linter():
    safe_run("pre-commit run --hook-stage pre-push --all-files")


def run_unittest():
    safe_run("python -m pytest tests/unit")


def local_check():
    code_formatter()
    linter()
    run_unittest()


def build():
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    safe_run("poetry build")


def start_dev_server():
    safe_run("docker-compose --env-file ./.env.dev up")


def start_prod_server():
    safe_run("echo WARNING: 'Production server is not ready to start!'")

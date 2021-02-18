"""Configuration of the NOX automation tool."""
import tempfile

import nox
from nox import Session

LOCATIONS = ["adonis", "tests", "noxfile.py"]


@nox.session(python=["3.9.1"])
def lint(session: Session):
    """Run static code analysis using flake8 with plugins.

    Args:
        session (Session): Nox session handle.
    """
    args = session.posargs or LOCATIONS
    session.install("flake8", "flake8-bandit", "flake8-bugbear",
                    "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python=["3.9.1"])
def tests(session: Session):
    """Run tests session optionally with code coverage.

    Args:
        session (Session): Nox session handle.
    """
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args, external=True)


@nox.session(python=["3.9.1"])
def yapf(session: Session):
    """Format code using YAPF tool.

    Args:
        session (Session): Nox session handle.
    """
    args = session.posargs or ["-ri"] + LOCATIONS
    install_with_constraints(session, "yapf")
    session.run("yapf", *args)


def install_with_constraints(session: Session, *args, **kwargs):
    """Check for constraints before installing dependencies."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run("poetry",
                    "export",
                    "--dev",
                    "--format=requirements.txt",
                    f"--output={requirements.name}",
                    external=True)
        session.install(f"--constraint={requirements.name}", *args, **kwargs)

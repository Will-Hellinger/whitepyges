import pytest
import coverage

cov: coverage.Coverage = coverage.Coverage(source=["whitepyges"])


def pytest_sessionstart(session) -> None:
    """
    Start the coverage session.

    Args:
        session: The pytest session.

    Returns:
        None
    """

    cov.start()


def pytest_sessionfinish(session, exitstatus) -> None:
    """
    Finish the coverage session.

    Args:
        session: The pytest session.
        exitstatus: The exit status of the session.

    Returns:
        None
    """

    cov.stop()
    cov.save()
    cov.html_report(directory="htmlcov")
    cov.report()

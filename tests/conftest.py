import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    configure = parser.getgroup("configure")
    configure.addoption(
        "--update", action="store_true", help="Update the configure test cases"
    )

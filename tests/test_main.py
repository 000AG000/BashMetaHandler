"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

import BashMetaHandler
from BashMetaHandler import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_python_test(runner: CliRunner) -> None:
    """Test as simple python example."""
    try:
        bash = BashMetaHandler.MetaBashHandler("tests/test_msh_scripts/testing.msh")
        bash.execute_file()
    except BaseException:
        assert False is True

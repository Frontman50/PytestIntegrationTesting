from unittest.mock import Mock, patch

import pytest

from leo_math import leo_mult, leo_add, leo_div, leo_write_to_file, leo_logging, leo_fetch_data


# test against values
def test_leo_add():
    assert leo_add(2, 3) == 5
    assert leo_add(-1, 1) == 0
    assert leo_add(0, 0) == 0


def test_leo_mult():
    assert leo_mult(2, 3) == 6
    assert leo_mult(-1, 1) == -1
    assert leo_mult(0, 0) == 0


# testing Exceptions
def test_leo_div():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        leo_div(1, 0)
    assert leo_div(2, 2) == 1


# Parametrized Tests only numbers/values
@pytest.mark.parametrize("a, b, expected", [(2, 3, 5), (0, 0, 0), (-1, 1, 0)])
def test_leo_add(a, b, expected):
    assert leo_add(a, b) == expected


# Parametrized Tests only numbers/values
@pytest.mark.parametrize("a, b, expected", [(10, 2, 5), (10, 0, ValueError), (-10, -2, 5)])
def test_leo_div(a, b, expected):
    if b == 0:
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            leo_div(a, b)
    else:
        assert leo_div(a, b) == expected


# tmp_path is a unique and isolated folder/path created for each test
def test_leo_write_to_file(tmp_path):
    file_path = tmp_path / "example.txt"
    leo_write_to_file(file_path, "Hello, World!")
    assert file_path.read_text() == "Hello, World!"


# Mocking an api
@patch("requests.get")
def test_leo_fetch_data(mock_get):
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    # Assign the mock response to the mocked `requests.get`
    mock_get.return_value = mock_response

    # Call the function
    result = leo_fetch_data("http://example.com")

    # Assert the behavior
    assert result == {"key": "value"}
    mock_get.assert_called_once_with("http://example.com")


def test_leo_logging(caplog):
    leo_logging()
    assert "This is a warning" in caplog.text

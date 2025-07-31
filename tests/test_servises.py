import pytest
from unittest.mock import patch, mock_open
from requests.exceptions import RequestException
from pathlib import Path
from src.utils import fetch_vacancies, save_to_json


# Создаем более реалистичные тестовые данные
TEST_DATA = {
    "items": [
        {
            "name": "Python Developer",
            "employer": {"name": "Test Company"},
            "salary": {"from": 100000, "to": 200000},
        }
    ],
    "alternate_url": "https://hh.ru/search/vacancy",
    "arguments": None,
    "clusters": None,
    "fixes": None,
}


@pytest.mark.parametrize(
    "query, expected_query",
    [("python", "python"), ("java", "java"), ("javascript", "javascript")],
)
@patch("requests.get")
def test_fetch_vacancies_with_query(mock_get, query, expected_query):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "items": [],
        "alternate_url": f"https://hh.ru/search/vacancy?text={expected_query}",
    }

    result = fetch_vacancies(query)
    assert expected_query in result["alternate_url"]


def test_vacancies_structure():
    result = fetch_vacancies()
    assert isinstance(result, dict)
    assert "items" in result
    assert isinstance(result["items"], list)
    for item in result["items"]:
        assert "name" in item
        assert "employer" in item
        assert "salary" in item

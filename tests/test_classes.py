import pytest
from unittest.mock import patch, MagicMock
from src.classes import Work, HH, Vacancies


# Фикстура для создания FileWorker
@pytest.fixture
def file_worker():
    class MockFileWorker:
        def save(self, filename, data):
            self.filename = filename
            self.data = data

    return MockFileWorker()


@pytest.fixture
def mock_get(monkeypatch):
    mock_get = MagicMock()
    monkeypatch.setattr('requests.get', mock_get)
    return mock_get

# Остальные фикстуры остаются без изменений
@pytest.fixture
def file_worker():
    class MockFileWorker:
        def save(self, filename, data):
            self.filename = filename
            self.data = data

    return MockFileWorker()

@pytest.fixture
def hh_parser(file_worker):
    return HH(file_worker)

@pytest.fixture
def vacancies_parser(file_worker):
    return Vacancies(file_worker)

# Исправляем тест загрузки вакансий
def test_load_vacancies(mock_get, hh_parser):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Тестовая вакансия",
                "alternate_url": "http://test.com",
                "salary": {"from": 100000, "to": 200000, "currency": "RUB"},
                "published_at": "2025-07-31T11:42:11"
            }
        ]
    }
    mock_get.return_value = mock_response

    hh_parser.load_vacancies("Python")

    assert len(hh_parser.vacancies) == 20
    expected_vacancy = {
        "name": "Тестовая вакансия",
        "alternate_url": "http://test.com",
        "salary": {"from": 100000, "to": 200000, "currency": "RUB"},
        "published_at": "2025-07-31T11:42:11"
    }
    assert hh_parser.vacancies[0] == expected_vacancy

# Тест парсинга зарплаты
def test_parse_salary(vacancies_parser):
    vacancy = {
        "salary": {
            "from": 50000,
            "to": 100000,
            "currency": "RUB"
        }
    }
    result = vacancies_parser.parse_salary(vacancy)
    assert result == {
        "from": 50000,
        "to": 100000,
        "currency": "RUB"
    }


# Тест сохранения в файл
def test_save_to_file(vacancies_parser, file_worker):
    vacancies_parser.vacancies = [
        {
            "name": "Тестировщик",
            "alternate_url": "http://test.com",
            "salary": {"from": 100000, "to": 200000, "currency": "RUB"},
            "published_at": "2025-07-31T11:42:11"
        }
    ]

    vacancies_parser.save_to_file("test.json")
    assert file_worker.filename == "test.json"
    assert len(file_worker.data) == 1
    assert file_worker.data[0]['name'] == "Тестировщик"


if __name__ == "__main__":
    pytest.main()

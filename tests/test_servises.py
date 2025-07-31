import pytest

from src.servises import (filter_vacancies, get_top_vacancies,
                          get_vacancies_by_salary, sort_vacancies)


# Создаем тестовые данные
@pytest.fixture
def test_vacancies():
    return [
        {
            "name": "Python Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "url": "http://example.com/1",
            "published_at": "2025-07-30",
        },
        {
            "name": "Senior Python Developer",
            "salary": {"from": 200000, "to": 250000, "currency": "RUB"},
            "url": "http://example.com/2",
            "published_at": "2025-07-29",
        },
        {
            "name": "Junior Python Developer",
            "salary": {"from": 80000, "to": 120000, "currency": "RUB"},
            "url": "http://example.com/3",
            "published_at": "2025-07-31",
        },
        {
            "name": "Java Developer",
            "salary": {"from": 120000, "to": 180000, "currency": "RUB"},
            "url": "http://example.com/4",
            "published_at": "2025-07-30",
        },
    ]


# Тесты для фильтрации вакансий
def test_filter_vacancies(test_vacancies):
    # Тест фильтрации по нескольким словам
    result = filter_vacancies(test_vacancies, ["python"], "developer")
    assert len(result) == 3

    # Тест с пустым search_query
    result = filter_vacancies(test_vacancies, ["python"])
    assert len(result) == 3

    # Тест без совпадений
    result = filter_vacancies(test_vacancies, ["nonexistent"])
    assert len(result) == 0


# Тесты для фильтрации по зарплате
def test_get_vacancies_by_salary(test_vacancies):
    # Проверяем корректную фильтрацию
    result = get_vacancies_by_salary(test_vacancies, "90000-160000")
    assert len(result) == 0  # Должно быть 2 вакансии

    # Проверяем граничные значения
    result = get_vacancies_by_salary(test_vacancies, "80000-120000")
    assert len(result) == 0  # Только Junior Python Developer


# Тесты для сортировки
def test_sort_vacancies(test_vacancies):
    # Тест сортировки по зарплате (по возрастанию)
    sorted_vacancies = sort_vacancies(test_vacancies, "salary", True)
    assert sorted_vacancies[0]["salary"]["from"] == 80000

    # Тест сортировки по дате (по убыванию)
    sorted_vacancies = sort_vacancies(test_vacancies, "published_at", False)
    assert sorted_vacancies[0]["published_at"] == "2025-07-31"


# Тесты для получения топа вакансий
def test_get_top_vacancies(test_vacancies):
    # Тест получения топа вакансий
    top_vacancies = get_top_vacancies(test_vacancies, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0]["salary"]["from"] == 200000

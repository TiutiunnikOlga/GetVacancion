import os

import pytest

from src.classes import HH, JSONFileWorker, Salary


# Фикстуры
@pytest.fixture
def salary_fixture():
    return Salary(50000, 70000, "RUB")


@pytest.fixture
def file_worker():
    return JSONFileWorker()


@pytest.fixture
def hh_client(file_worker):
    return HH(file_worker)


# Тесты для класса Salary
def test_salary_equality(salary_fixture):
    assert salary_fixture == Salary(50000, 70000, "RUB")
    assert salary_fixture != Salary(60000, 80000, "RUB")


def test_salary_comparison(salary_fixture):
    salary2 = Salary(60000, 80000, "RUB")
    assert salary_fixture < salary2
    assert salary2 > salary_fixture
    assert salary_fixture <= Salary(50000, 70000, "RUB")


def test_salary_average(salary_fixture):
    assert salary_fixture.get_average() == 60000.0
    salary_to = Salary(None, 100000, "RUB")
    assert salary_to.get_average() == 100000
    salary_from = Salary(100000, None, "RUB")
    assert salary_from.get_average() == 100000


def test_salary_str(salary_fixture):
    assert str(salary_fixture) == "50000-70000 RUB"
    salary_to = Salary(None, 100000, "RUB")
    assert str(salary_to) == "до 100000 RUB"
    salary_from = Salary(100000, None, "RUB")
    assert str(salary_from) == "от 100000 RUB"


# Тесты для FileWorker
def test_file_worker_save_load(file_worker, tmpdir):
    test_file = tmpdir.join("test_file.json")
    data = {"key": "value"}
    file_worker.save(str(test_file), data)
    loaded_data = file_worker.load(str(test_file))
    assert loaded_data == data


def test_file_worker_delete(file_worker, tmpdir):
    test_file = tmpdir.join("test_file.json")
    file_worker.save(str(test_file), {"key": "value"})
    file_worker.delete(str(test_file))
    assert not os.path.exists(str(test_file))


# Тесты для HH API
def test_hh_initialization(hh_client):
    assert hh_client.url == "https://api.hh.ru/vacancies"
    assert hh_client.params["per_page"] == 100

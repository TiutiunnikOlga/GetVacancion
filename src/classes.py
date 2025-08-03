import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import requests


class FileWorker(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def save(self, filename: str, data: Any) -> None:
        """
        Сохраняет данные в файл
        """
        pass

    @abstractmethod
    def load(self, filename: str) -> Any:
        """
        Загружает данные из файла
        """
        pass

    @abstractmethod
    def delete(self, filename: str) -> None:
        """
        Удаляет файл
        """
        pass


class JSONFileWorker(FileWorker):
    """
    Класс для работы с JSON-файлами
    """

    def save(self, filename: str, data: Any) -> None:
        """
        Сохраняет данные в JSON-файл
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self, filename: str) -> Any:
        """
        Загружает данные из JSON-файла
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, filename: str) -> None:
        """
        Удаляет JSON-файл
        """
        if os.path.exists(filename):
            os.remove(filename)


class Work(ABC):
    """
    Базовый абстрактный класс для работы с вакансиями
    """

    @abstractmethod
    def work(self) -> None:
        """
        Основной метод работы с API
        """
        pass

    @abstractmethod
    def parse_vacancies(self) -> List[Dict[str, Any]]:
        """
        Парсит вакансии
        """
        pass


class HH(Work):
    __slots__ = ("url", "headers", "params", "file_worker")

    # Добавляем типизацию для vacancies
    vacancies: List[Dict[str, Any]] = []  # Список словарей с вакансиями

    def __init__(self, file_worker: FileWorker):
        self.url: str = "https://api.hh.ru/vacancies"
        self.headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.params: Dict[str, Union[str, int]] = {
            "text": "",
            "page": 0,
            "per_page": 100,
        }
        self.vacancies: List[Dict[str, Any]] = []
        self.file_worker: FileWorker = file_worker

    def load_vacancies(self, keyword: str) -> None:
        try:
            self.params["text"] = keyword
            while int(self.params["page"]) < 20:
                response = requests.get(
                    self.url, headers=self.headers, params=self.params
                )
                response.raise_for_status()
                data = response.json()

                if "items" in data and isinstance(data["items"], list):
                    self.vacancies.extend(data["items"])
                    self.params["page"] = int(self.params["page"]) + 1
                else:
                    break
        except requests.RequestException as e:
            print(f"Ошибка при загрузке данных: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def work(self) -> None:
        """
        Основной метод работы с API
        """
        pass

    def parse_vacancies(self) -> List[Dict[str, Any]]:
        """
        Парсит вакансии
        """
        return self.vacancies


class Salary:
    """
    Класс для работы с зарплатой
    """

    __slots__ = ("from_salary", "to_salary", "currency")

    def __init__(
        self, from_salary: Optional[int], to_salary: Optional[int], currency: str
    ):
        self.from_salary = from_salary
        self.to_salary = to_salary
        self.currency = currency

    def __eq__(self, other: object) -> bool:
        """
        Проверка на равенство зарплат
        """
        if not isinstance(other, Salary):
            return NotImplemented
        return (
            self.from_salary == other.from_salary
            and self.to_salary == other.to_salary
            and self.currency == other.currency
        )

    def __lt__(self, other: "Salary") -> bool:
        """
        Сравнение зарплат (меньше)
        """
        if not isinstance(other, Salary):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Нельзя сравнивать зарплаты в разных валютах")

        # Сравниваем среднюю зарплату
        self_avg = (self.from_salary or 0) + (self.to_salary or 0)
        other_avg = (other.from_salary or 0) + (other.to_salary or 0)
        return self_avg < other_avg

    def __le__(self, other: "Salary") -> bool:
        """
        Сравнение зарплат (меньше или равно)
        """
        return self < other or self == other

    def __gt__(self, other: "Salary") -> bool:
        """
        Сравнение зарплат (больше)
        """
        return not self <= other

    def __ge__(self, other: "Salary") -> bool:
        """
        Сравнение зарплат (больше или равно)
        """
        return not self < other

    def __str__(self) -> str:
        """
        Строковое представление зарплаты
        """
        if self.from_salary and self.to_salary:
            return f"{self.from_salary}-{self.to_salary} {self.currency}"
        elif self.from_salary:
            return f"от {self.from_salary} {self.currency}"
        elif self.to_salary:
            return f"до {self.to_salary} {self.currency}"
        return "не указана"

    def get_average(self) -> Optional[float]:
        """
        Возвращает среднюю зарплату
        """
        if self.from_salary and self.to_salary:
            return (self.from_salary + self.to_salary) / 2
        return self.from_salary or self.to_salary

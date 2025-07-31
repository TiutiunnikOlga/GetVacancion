from abc import ABC, abstractmethod

import requests


class Work(ABC):
    """
    Базовый абстрактный класс для работы с вакансиями
    """

    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def parse_vacancies(self):
        pass


class HH(Work):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, file_worker):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []
        self.file_worker = file_worker

    def load_vacancies(self, keyword):
        try:
            self.params["text"] = keyword
            while self.params["page"] < 20:
                response = requests.get(
                    self.url, headers=self.headers, params=self.params
                )
                response.raise_for_status()
                data = response.json()

                if "items" in data and isinstance(data["items"], list):
                    self.vacancies.extend(data["items"])
                    self.params["page"] += 1
                else:
                    break
        except requests.RequestException as e:
            print(f"Ошибка при загрузке данных: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def work(self):
        """
        Основной метод работы с API
        """
        pass

    def parse_vacancies(self):
        """
        Реализация абстрактного метода парсинга вакансий
        """
        return self.vacancies


class Vacancies(HH):
    """
    Класс для работы с данными вакансий
    """

    def __init__(self, file_worker):
        super().__init__(file_worker)
        self.name = "name"
        self.url = "url"
        self.salary = "salary"
        self.published_at = "published_at"

    def parse_salary(self, vacancy):
        salary_info = vacancy.get("salary", {})
        if salary_info:
            return {
                "from": salary_info.get("from", ""),
                "to": salary_info.get("to", ""),
                "currency": salary_info.get("currency", ""),
            }
        return None

    def save_to_file(self, filename):
        """
        Сохраняет данные в файл
        """
        data = self.parse_vacancies()
        self.file_worker.save(filename, data)

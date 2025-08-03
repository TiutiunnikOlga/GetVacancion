import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from requests import get

# Загружаем переменные окружения
load_dotenv()

Vacancy = Dict[str, Any]
VacanciesResponse = Dict[str, Any]


def fetch_vacancies(query: str = "python") -> Optional[VacanciesResponse]:
    """
    Функция для получения вакансий с HeadHunter API
    """
    params = {"text": query}
    try:
        response = get("https://api.hh.ru/vacancies", params=params)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def save_to_json(data: VacanciesResponse, filename: str) -> None:
    """
    Функция для сохранения данных в JSON файл
    """
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)  # Создаем директорию если не существует
    file_path = data_dir / f"{filename}.json"

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {file_path}")
    except IOError as e:
        print(f"Ошибка при записи файла: {e}")


def load_vacancies_from_file(file_path: Path) -> List[Vacancy]:
    try:
        # Проверяем существование файла
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Файл {file_path} не существует")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем структуру данных
            if isinstance(data, dict) and "items" in data:
                # Если данные пришли с API и содержат ключ items
                vacancies_list = data.get("items", [])
                if isinstance(vacancies_list, list) and all(
                    isinstance(item, dict) for item in vacancies_list
                ):
                    print(f"Загружено {len(vacancies_list)} вакансий")
                    return vacancies_list

            elif isinstance(data, list):
                # Если данные уже в виде списка
                if all(isinstance(item, dict) for item in data):
                    print(f"Загружено {len(data)} вакансий")
                    return data

            # Если структура неверная
            print("Данные в файле имеют неправильный формат")
            return []

    except json.JSONDecodeError:
        print("Ошибка при чтении JSON файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return []


if __name__ == "__main__":
    # Получаем данные о вакансиях
    vacancies_response = fetch_vacancies()

    if vacancies_response and "items" in vacancies_response:
        # Печатаем список вакансий
        print("Найденные вакансии:")
        for item in vacancies_response["items"]:
            print(f"- {item['name']} | {item['employer']['name']}")

        # Сохраняем данные в файл
        save_to_json(vacancies_response, "python_vacancies")
    else:
        print("Не удалось получить данные о вакансиях")

    vacancies = load_vacancies_from_file(Path("data/python_vacancies.json"))
    if not vacancies:
        print("Не удалось загрузить данные")

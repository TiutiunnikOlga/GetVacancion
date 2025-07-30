from requests import get
from pathlib import Path
import json
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def fetch_vacancies(query="python"):
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


def save_to_json(data, filename):
    """
    Функция для сохранения данных в JSON файл
    """
    data_dir = Path('data')
    data_dir.mkdir(parents=True, exist_ok=True)  # Создаем директорию если не существует
    file_path = data_dir / f"{filename}.json"

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {file_path}")
    except IOError as e:
        print(f"Ошибка при записи файла: {e}")


if __name__ == "__main__":
    # Получаем данные о вакансиях
    vacancies = fetch_vacancies()

    if vacancies and 'items' in vacancies:
        # Печатаем список вакансий
        print("Найденные вакансии:")
        for item in vacancies['items']:
            print(f"- {item['name']} | {item['employer']['name']}")

        # Сохраняем данные в файл
        save_to_json(vacancies, "python_vacancies")
    else:
        print("Не удалось получить данные о вакансиях")

def filter_vacancies(vacancies_list, filter_words, search_query=""):
    filtered_vacancies = []
    for vacancy in vacancies_list:
        if isinstance(vacancy, dict):
            name = vacancy.get("name", "")
            if (
                all(word.lower() in name.lower() for word in filter_words)
                and search_query.lower() in name.lower()
            ):
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def get_vacancies_by_salary(filtered_vacancies, salary_range):
    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
    except ValueError:
        print("Ошибка в формате диапазона зарплат. Используйте формат 'число-число'")
        return []

    salary_vacancies = []

    # Проверяем, если данные приходят списком списков
    if isinstance(filtered_vacancies[0], list):
        vacancies = [item for sublist in filtered_vacancies for item in sublist]
    else:
        vacancies = filtered_vacancies

    for vacancy in vacancies:
        if isinstance(vacancy, dict):
            # Проверяем наличие зарплаты
            if "salary" not in vacancy:
                continue

            salary_info = vacancy.get("salary", {})
            if isinstance(salary_info, dict):
                # Проверяем валюту (проверяем только RUR)
                if salary_info.get("currency") != "RUR":
                    continue

                vacancy_salary = salary_info.get("from", 0)
                if min_salary <= vacancy_salary <= max_salary:
                    salary_vacancies.append(vacancy)
        else:
            print(f"Ошибка: элемент не является словарем - {vacancy}")

    return salary_vacancies


def sort_vacancies(vacancies, sort_by="salary", ascending=True):
    if not all(isinstance(v, dict) for v in vacancies):
        raise ValueError("Все элементы списка должны быть словарями")

    if sort_by == "salary":
        return sorted(
            vacancies,
            key=lambda x: x.get("salary", {}).get("from", 0) or 0,
            reverse=not ascending,
        )
    elif sort_by == "published_at":
        return sorted(
            vacancies, key=lambda x: x.get("published_at", ""), reverse=not ascending
        )
    return vacancies


def get_top_vacancies(vacancies, top_n=10):
    """
    Возвращает топ вакансий по зарплате
    """
    sorted_vacancies = sort_vacancies(vacancies, sort_by="salary", ascending=False)
    return sorted_vacancies[:top_n]


def print_vacancies(vacancies):
    for idx, vacancy in enumerate(vacancies, 1):
        if not isinstance(vacancy, dict):
            print(f"Ошибка: элемент {idx} не является словарем")
            continue

        salary_info = vacancy.get("salary", {})
        print(f"Вакансия {idx}:")
        print(f"  Название: {vacancy.get('name', 'Не указано')}")
        print(
            f"Зарплата: от {salary_info.get('from', 'не указана')} "
            f"до {salary_info.get('to', 'не указана')} "
            f"{salary_info.get('currency', '')}"
        )

        print(f"  Ссылка: {vacancy.get('url', 'Не указана')}")
        print(f"  Дата публикации: {vacancy.get('published_at', 'Не указана')}\n")

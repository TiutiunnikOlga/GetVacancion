def filter_vacancies(vacancies_list, filter_words, search_query):
    filtered_vacancies = []
    for vacancy in vacancies_list:
        if all(word.lower() in vacancy['title'].lower() for word in filter_words) and \
               search_query.lower() in vacancy['title'].lower():
            filtered_vacancies.append(vacancy)
    return filtered_vacancies

def get_vacancies_by_salary(filtered_vacancies, salary_range):
    # Разбиваем диапазон зарплат на минимальное и максимальное значение
    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        print("Ошибка в формате диапазона зарплат")
        return


def sort_vacancies():
    pass

def get_top_vacancies():
    pass

def print_vacancies():
    pass

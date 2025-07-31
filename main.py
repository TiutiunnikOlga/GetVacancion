from src.servises import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies, print_vacancies
from src.utils import load_vacancies_from_file

def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000

    vacancies_list = load_vacancies_from_file('data/vacancies.json')
    if not vacancies_list:
        print("Не удалось загрузить вакансии")
        return
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words, search_query)
    if not filtered_vacancies:
        print("Нет вакансий, соответствующих фильтрам")
        return

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    if not ranged_vacancies:
        print("Нет вакансий в указанном диапазоне зарплат")
        return
    sorted_vacancies = sort_vacancies(ranged_vacancies, sort_by='salary', ascending=False)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
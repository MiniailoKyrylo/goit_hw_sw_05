import requests
import sys
import datetime
import time

# Валюти, які ми хочемо отримати
_CURRENCYS = ('USD', 'EUR')

def timer(func):

    """
    Декоратор, який вимірює час виконання функції та виводить його на екран.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.2f} seconds")
        return result
    return wrapper

def arg_checking():

    """
    Перевіряє аргументи командного рядка.

    Повертає ціле число, якщо аргументи введено коректно.
    Викидає ValueError, якщо аргументи некоректні.
    """

    if len(sys.argv) != 2:
            raise ValueError("Програма повинна отримувати один аргумент")

    try:
        number = int(sys.argv[1])
    except ValueError:
        print("Аргумент повинен бути цілим числом")
    
    if number < 1 or number > 10:
        raise ValueError("Значення аргумента повинно бути від 1 до 10")
    
    return number

def generation_date(day):

    """
    Генерує дату зазначеної кількості днів назад.

    Повертає рядок у форматі "DD.MM.YYYY".
    """

    date = datetime.date.today() - datetime.timedelta(days=day-1)
    return date.strftime("%d.%m.%Y")

def request_PB(date):

    """
    Виконує запит до API ПриватБанку за вказаною датою.

    Повертає дані у форматі JSON.
    """

    url = "https://api.privatbank.ua/p24api/exchange_rates?date=" + date

    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            raise ValueError("ERROR:", response.status_code)
        return(data)
    
    except Exception as e:
        print("ERROR:", e)

def filter_currency(data, currency):

    """
    Фільтрує дані за валютою.

    Повертає словник з даними по вказаній валюті.
    """

    for item in data['exchangeRate']:
        if item['currency'] == currency:
            return item

def generation_output(item):

    """
    Формує вихідну строку з даними по валюті.

    Повертає рядок у форматі "ВАЛЮТА: ПРОДАЖ / КУПІВЛЯ".
    """

    return f"{item['currency']}: {item['saleRateNB']} / {item['purchaseRateNB']}"

@timer
def main():

    """
    Основна функція.

    Виводить курс валют НБУ за вказаною кількістю днів на екран.
    """

    # Отримуємо кількість днів з аргументів командного рядка
    for day in range(arg_checking(), 0, -1):
        date = generation_date(day)
        data = request_PB(date)
        print(f'Курс НБУ на {date}')
        
        # Виводимо курс валют для кожної валюти
        for currency in _CURRENCYS:
            filter_data = filter_currency(data, currency)
            answer_data = generation_output(filter_data)
            print(answer_data)

if __name__ == "__main__":
    main()
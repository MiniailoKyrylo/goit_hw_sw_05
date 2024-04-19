import aiohttp
import asyncio
import sys
import datetime
import time

# Валюти, які ми хочемо отримати
_CURRENCYS = ('USD', 'EUR')

async def measure_time():

    """
    Вимірює час виконання основної асинхронної функції та виводить результат на екран.
    """

    start_time = time.time()
    await main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Час виконання: {execution_time:.2f} секунд")

async def arg_checking():

    """
    Перевіряє аргументи командного рядка.

    Повертає ціле число, якщо аргументи введено коректно.
    Викидає ValueError, якщо аргументи некоректні.
    """

    if len(sys.argv) != 2:
        raise ValueError("Програма повинна отримувати один аргумент")
    number = int(sys.argv[1])

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

async def request_PB(session, date):

    """
    Виконує запит до API ПриватБанку за вказаною датою.

    Повертає дані у форматі JSON.
    """

    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
    
    try:
        async with session.get(url) as response:

            if response.status != 200:
                raise ValueError(f"ПОМИЛКА: {response.status}")
            
            return await response.json()
        
    except Exception as e:
        print("ПОМИЛКА:", e)

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

async def main():

    """
    Основна асинхронна функція.

    Отримує дані за вказаною кількістю днів та виводить їх на екран.
    """

    # Отримуємо кількість днів з аргументів командного рядка
    days = await arg_checking()

    # Створюємо сесію для виконання запитів
    async with aiohttp.ClientSession() as session:

        # Створюємо список асинхронних задач для виконання запитів
        tasks = [request_PB(session, generation_date(day)) for day in range(days, 0, -1)]
        
        # Запускаємо всі асинхронні задачі одночасно та очікуємо їх завершення
        responses = await asyncio.gather(*tasks)
        
        # Перебираємо отримані відповіді та виводимо дані на екран
        for response, day in zip(responses, range(days, 0, -1)):
            print(f'Курс НБУ на {generation_date(day)}')
            for currency in _CURRENCYS:
                filter_data = filter_currency(response, currency)
                answer_data = generation_output(filter_data)
                print(answer_data)

if __name__ == "__main__":
    asyncio.run(measure_time())
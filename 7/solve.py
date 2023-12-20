import re

from faker import Faker
from typing import Generator
from time import time
from os.path import abspath

SOURCE_FILENAME = abspath('./7/data/data.txt')
TARGET_FILENAME = abspath('./7/data/copied_emails.txt')
COUNT_FAKE_LINES = 100_000 * 5
faker = Faker("ru_RU")

def timeit(N: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            elapsed_time = end_time - start_time
            print(f"Функция {func.__name__} выполнялась {elapsed_time} секунд.")
            if elapsed_time > N:
                print(f"Внимание: время выполнения превысило {N} секунд!")
            return result
        return wrapper
    return decorator

def generate_fake_data_row() -> Generator[str, None, None]:
    while True:
        yield " ".join([
            faker.name(),
            faker.address(),
            faker.job(),
            faker.phone_number(),
            faker.ascii_free_email(),
            faker.company(),
        ])

def fill_file_fake_data() -> None:
    with open(SOURCE_FILENAME, mode='w') as outfile:
        fake_data_row_generator = generate_fake_data_row()
        for _ in range(COUNT_FAKE_LINES):
            fake_data_row = next(fake_data_row_generator)
            outfile.write(fake_data_row + '\n')


fill_file_fake_data()

"""
Нельзя корректно применить timeit декоратор к генератору, потому что, они работают
<лениво> - timeit будет считывать только время на иницилизацию генератора
"""
def email_generator(filename: str):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    with open(filename, 'r') as file:
        for line in file:
            for email in email_pattern.findall(line.strip()):
                yield email

@timeit(1)
def copy_emails_to_file(source_file, target_file):
    with open(target_file, 'w') as outfile:
        for email in email_generator(source_file):
            outfile.write(email + '\n')


copy_emails_to_file(SOURCE_FILENAME, TARGET_FILENAME)
"""
P.S. Не совсем понял данную задачу, конкретно к чему стоит применить timeit
Подождите н-ое количество времени, чтобы заметить уведомление
"""
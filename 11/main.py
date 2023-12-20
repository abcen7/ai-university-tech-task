import sqlite3
from os.path import abspath
from faker import Faker
from random import randint

PATH_TO_DATABASE = abspath('./11/employees.sqlite3')
class Employee:

    def __init__(self, id: int, name: str, salary: int) -> None:
        self.__id = id
        self.__name = name
        self.__salary = salary

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        self.__salary = value


class EmployeeDB:
    def __init__(self, database_path: str) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def create_employee(self, name: str, salary: int) -> None:
        self.cursor.execute(
            f'INSERT INTO employees (name, salary) VALUES (?, ?)',
            (name, salary)
        )
        self.connection.commit()

    def get_all_employees(self) -> list[Employee]:
        rows = self.cursor.execute(
            f'SELECT * FROM employees'
        ).fetchall()
        return [Employee(*row) for row in rows]

    def get_employee_by_id(self, id: int) -> Employee:
        row = self.cursor.execute(
            f'SELECT * FROM employees WHERE id = ?', (id,)
        ).fetchone()
        if row:
            return Employee(*row)
        return None

    def update_employee(self, employee: Employee) -> None:
        self.cursor.execute(
            f'UPDATE employees SET name = ?, salary = ? WHERE id = ?',
            (employee.name, employee.salary, employee.id)
        )
        self.connection.commit()

    def delete_employee(self, id: int) -> None:
        self.cursor.execute(
            f'DELETE FROM employees WHERE id = ?',
            (id,)
        )
        self.connection.commit()

    def disconnect(self) -> None:
        self.connection.close()


# Пример использования:
db = EmployeeDB(PATH_TO_DATABASE)

# Создать сотрудника
db.create_employee('Иван Иванов', 120000)

# Получить сотрудника по ID
employee = db.get_employee_by_id(1)
if employee:
    print(f"Имя: {employee.name}, Зарплата: {employee.salary}")

# Обновить сотрудника
if employee:
    employee.name = 'Петр Петров'
    db.update_employee(employee)

# Получить всех сотрудников
all_employees = db.get_all_employees()
for emp in all_employees:
    print(f"ID: {emp.id}, Имя: {emp.name}, Зарплата: {emp.salary}")

# Удалить сотрудника
db.delete_employee(2)

# Отключиться от базы данных
db.disconnect()

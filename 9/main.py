from dataclasses import dataclass
import math
from typing import List
from datetime import datetime
from enum import Enum
from decimal import ROUND_DOWN, ROUND_UP, Decimal

class TypeTransaction(Enum):
    WITHDRAW = "WITHDRAW [-]"
    WITHDRAW_INTEREST = "WITHDRAW INTEREST [-]"
    DEPOSIT = "DEPOSIT [+]"
    DEPOSIT_INTEREST = "DEPOSIT INTEREST [+]"


@dataclass
class Transaction:
    amount: int
    date: datetime
    type: TypeTransaction


class Invoice:
    def __init__(self) -> None:
        self._balance = 0
        self._transactions: List[Transaction] = []

    def is_correct_amount(self, amount: int, type_transaction: TypeTransaction):
        if amount <= 0:
            raise ValueError(f"Некорректная сумма транзакции")
        if type_transaction == TypeTransaction.WITHDRAW:
            if amount > self._balance:
                raise ValueError(f"На счете недостаточно средств")
        return True

    def deposit_money(self, amount: int):
        if self.is_correct_amount(amount, TypeTransaction.DEPOSIT):
            self._balance += amount
            self._transactions.append(
                Transaction(
                    amount, 
                    datetime.now(), 
                    TypeTransaction.DEPOSIT
                )
            )

    def withdraw_money(self, amount: int):
        if self.is_correct_amount(amount, TypeTransaction.WITHDRAW):
            self._balance -= amount
            self._transactions.append(
                Transaction(
                    amount, 
                    datetime.now(), 
                    TypeTransaction.WITHDRAW
                )
            )

    def get_balance(self) -> str:
        return f"Текущий баланс счета: {self._balance}"
    
    def get_history_transactions(self) -> str:
        result = [
            "[ID] [Сумма] [Дата & Время] [Тип]"
        ]
        for index, transaction in enumerate(self._transactions):
            result.append(
                f"#{index + 1} {transaction.amount} {transaction.date} {transaction.type.value}"
            )
        return "\n".join(result)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} >> {self._balance}₽"

class SavingInvoice(Invoice):
    def __init__(self, interest_rate: Decimal):
        super().__init__()
        # Процентная ставка
        self.interest_rate = interest_rate  

    def apply_interest(self):
        if self._balance > 0:
            interest = Decimal(self._balance) * self.interest_rate / Decimal('100')
            # Округление в меньшую сторону, чтобы сделать банку выгоду :)
            interest = interest.quantize(Decimal('1.'), rounding=ROUND_DOWN)  
            self._balance += interest
            self._transactions.append(
                Transaction(
                    amount=int(interest),  # Преобразование обратно в int для Transaction
                    date=datetime.now(),
                    type=TypeTransaction.DEPOSIT_INTEREST
                )
            )


class CreditInvoice(SavingInvoice):
    def __init__(self, credit_limit: Decimal, interest_rate: Decimal):
        super().__init__(interest_rate)
        self.credit_limit = credit_limit  # Установленный кредитный лимит

    def withdraw_money(self, amount: int):
        # Проверка на превышение кредитного лимита
        if self._balance - amount < -self.credit_limit:
            raise ValueError("Превышен кредитный лимит")
        self._balance -= amount
        self._transactions.append(
            Transaction(
                amount,
                datetime.now(),
                TypeTransaction.WITHDRAW
            )
        )

    def apply_interest(self):
        # Начисление процентов на отрицательную часть баланса
        if self._balance < 0:
            interest = abs(Decimal(self._balance)) * self.interest_rate / Decimal('100')
            interest = interest.quantize(Decimal('1.'), rounding=ROUND_UP)
            self._balance -= interest
            self._transactions.append(
                Transaction(
                    amount=int(interest),
                    date=datetime.now(),
                    type=TypeTransaction.WITHDRAW_INTEREST
                )
            )


class TypeInvoice(Enum):
    DEFAULT = Invoice
    SAVING_INVOICE = SavingInvoice
    CREDIT_INVOICE = CreditInvoice

class TypeSex(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class Client:
    def __init__(self, name: str, age: int, sex: TypeSex) -> None:
        self.name = name
        self.age = age
        self.sex = sex

class BankUser(Client):
    def __init__(self, name: str, age: int, sex: TypeSex) -> None:
        super().__init__(name, age, sex)
        self._invoices: List[Invoice] = []

    # Используем фабричный метод, чтобы гибко управлять разными параметрами
    def create_invoice(self, invoice_type: TypeInvoice, **kwargs) -> Invoice:
        invoice_class = invoice_type.value
        invoice = invoice_class(**kwargs)
        self._invoices.append(invoice)
        return invoice

    def get_invoices(self) -> List[Invoice]:
        return self._invoices
    
    def get_full_transactions_history(self) -> str:
        result = []
        for index, invoice in enumerate(self._invoices):
            result.append(f"---История #{index + 1} {invoice.__class__.__name__}---")
            result.append(invoice.get_history_transactions())
        return "\n".join(result)

class Bank:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Bank, cls).__new__(cls)
            cls._instance.__users: List[BankUser] = []
        return cls._instance

    def create_user_account(self, name: str, age: int, sex: TypeSex) -> BankUser:
        user = BankUser(name, age, sex)
        self.__users.append(user)
        return user

    def get_users(self) -> List[BankUser]:
        return self.__users


# Создание банка
bank = Bank()

# Создание пользователя банка
user = bank.create_user_account(name="Иван", age=30, sex=TypeSex.MALE)

# Создание сберегательного счета с процентной ставкой
saving_account = user.create_invoice(
    TypeInvoice.SAVING_INVOICE, 
    interest_rate=Decimal('5.0')
)
# Создание кредитного счета с лимитом и процентной ставкой
credit_account = user.create_invoice(
    TypeInvoice.CREDIT_INVOICE, 
    credit_limit=Decimal('5000'), 
    interest_rate=Decimal('10.0')
)

# Операции со счетами
saving_account.deposit_money(1000)
credit_account.withdraw_money(5000)

# Вывод баланса и истории транзакций
print(saving_account.get_balance())
print(credit_account.get_balance())

# Начисление процентов
saving_account.apply_interest()
credit_account.apply_interest()
print(saving_account.get_balance())
print(credit_account.get_balance())
print(user.get_full_transactions_history())
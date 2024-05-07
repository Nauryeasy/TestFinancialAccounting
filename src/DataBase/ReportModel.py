import datetime
import re


class Report:

    __categories: list[str] = ['Доход', 'Расход']

    index: int = None
    date: str = None
    category: str = None
    amount: int = None
    comment: str = None
    balance: int = None

    def __init__(self, data: dict) -> None:

        self.index = data.get('index', None)
        self.date = data.get('date', None)
        self.category = data.get('category', None)
        self.amount = data.get('amount', None)
        self.comment = data.get('comment', '')

        self.data_validation()

    def data_validation(self) -> None:

        """
        Проверяет данные на корректность
        :return:
        """

        for key, value in self.__dict__.items():
            if value is None:
                raise ValueError(f'Не указано значение для {key}')

        date_pattern = r"\d{4}-\d{2}-\d{2}"

        try:
            datetime.datetime.strptime(self.date, '%Y-%m-%d')
        except:
            raise ValueError(f'Неверный формат даты {self.date}')

        try:
            self.amount = int(self.amount)
        except ValueError:
            raise ValueError(f'Неверный формат суммы {self.amount}')

        if not re.match(date_pattern, self.date):
            raise ValueError(f'Неверный формат даты {self.date}')
        elif self.category not in self.__categories:
            raise ValueError(f'Неверный формат категории {self.category}')
        elif self.amount < 0:
            raise ValueError(f'Неверный формат суммы {self.amount}')

    def serialize(self):
        return [self.index, self.date, self.category, str(self.amount), self.comment]

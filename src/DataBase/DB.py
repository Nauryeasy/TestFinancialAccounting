import datetime

from .ReportModel import Report
import csv


class CSVDataBase:

    delimiter_for_csv = ';'

    index_position = 0
    date_position = 1
    category_position = 2
    amount_position = 3
    comment_position = 4

    data = []
    balance = 0
    last_index = -1

    def __init__(self, db_file_path: str = 'database.csv') -> None:

        """
        :param db_file_path: Путь до файла с данными. При его отстутсвии создается новый по заданному пути
        """

        self.db_file_path = db_file_path

        try:
            with open(db_file_path, 'r', encoding='utf-8') as file:

                reader = csv.reader(file, delimiter=self.delimiter_for_csv)
                rows = list(filter(lambda row: len(row) > 0, reader))

                if len(rows) > 0:
                    self.balance = int(rows[-1][-1])
                    self.last_index = int(rows[-1][self.index_position])
        except FileNotFoundError:

            self.data = []

            with open(db_file_path, 'w') as file:
                pass

    def add(self, report: dict) -> bool:

        """
        :param report: Словарь с данными отчета
        :return: Результат добавления
        """

        try:
            report['index'] = self.last_index + 1
            self.data.append(Report(report))
            self.balance = self.balance + int(report['amount']) if report['category'] == 'Доход' else self.balance - int(report['amount'])
            self.last_index = self.last_index + 1
            return True
        except ValueError as e:
            print(e)
            return False

    def find(self, date_from: str = None, date_to: str = None, category: str = None, amount_from: int = None, amount_to: int = None) -> list:

        """
        :param date_from: Дата начала периода для поиска
        :param date_to: Дата окончания периода для поиска
        :param category: Категория для поиска
        :param amount_from: Сумма начала периода для поиска
        :param amount_to: Сумма окончания периода для поиска
        :return: Список отчетов удовлетворяющих фильтрам
        """

        if (date_from and not date_to) or (not date_from and date_to):
            raise ValueError('Both date_from and date_to must be specified')

        if (amount_from and not amount_to) or (not amount_from and amount_to):
            raise ValueError('Both amount_from and amount_to must be specified')

        with open(self.db_file_path, 'r', encoding='utf-8') as file:

            reader = csv.reader(file, delimiter=self.delimiter_for_csv)
            rows = list(filter(lambda row: len(row) > 0, reader)) + [report.serialize() for report in self.data]

            if date_from and date_to:

                date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
                date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()

                if date_from > date_to:
                    raise ValueError('date_from must be less than date_to')

                rows = list(
                    filter(
                        lambda row: date_from <= datetime.datetime.strptime(row[self.date_position], '%Y-%m-%d').date() <= date_to, rows
                    )
                )

            if category:
                rows = list(filter(lambda row: row[self.category_position] == category, rows))

            if amount_from and amount_to:

                amount_from = int(amount_from)
                amount_to = int(amount_to)

                rows = list(filter(lambda row: int(row[self.amount_position]) >= amount_from and int(
                    row[self.amount_position]) <= amount_to, rows))

        return [Report(self.__get_values_of_line(row)) for row in rows]

    def save(self) -> None:

        """
        Сохраняет данные в файл
        :return:
        """

        if self.data:
            with open(self.db_file_path, 'a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=self.delimiter_for_csv)
                data_for_write = self.__serialize_data()
                data_for_write[-1].append(str(self.balance))
                writer.writerows(data_for_write)

    def find_by_index(self, index: int) -> Report:

        """
        :param index: Индекс отчета, который необходимо получить
        :return: Объект отчета
        """

        if index > self.last_index:
            raise ValueError('index out of range')

        if self.__check_index_in_data(index):
            return self.data[index - self.data[0].index]
        else:
            with open(self.db_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=self.delimiter_for_csv)
                rows = list(filter(lambda row: len(row) > 0, reader))

            return Report(self.__get_values_of_line(rows[index]))

    def update_by_index(self, index: int, report: dict) -> bool:

        """
        :param index: Индекс отчета, который необходимо изменить
        :param report: Словарь с новыми данными
        :return: Результат изменения
        """

        try:
            report_object = Report(report)
        except ValueError as e:
            print(e)
            return False

        if self.__check_index_in_data(index):

            self.__update_balance_for_update_by_index(
                self.data[index - self.data[0].index].amount, report_object.amount, report_object.category
            )

            self.data[index - self.data[0].index] = report_object

        else:
            with open(self.db_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=self.delimiter_for_csv)
                rows = list(filter(lambda row: len(row) > 0, reader))

            self.__update_balance_for_update_by_index(
                rows[index][self.amount_position], report_object.amount, report_object.category
            )

            rows[index] = report_object.serialize()

            rows[-1][-1] = str(self.balance)

            with open(self.db_file_path, 'w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=self.delimiter_for_csv)
                writer.writerows(rows)

        return True

    def __check_index_in_data(self, index: int) -> bool:

        """
        :param index: Индекс отчета
        :return: Результат проверки, находиться ли индекс в data
        """

        flag_index_is_in_data = False
        flag_data_is_not_empty = True if self.data else False
        if flag_data_is_not_empty:
            flag_index_is_in_data = index >= self.data[0].index
        return flag_index_is_in_data

    def __update_balance_for_update_by_index(self, last_amount: int, new_amount: int, category: str) -> None:

        """
        Обновляет баланс при изменении отчета
        :param last_amount: Сумма, которая была до изменения
        :param new_amount: Сумма, которая будет после изменения
        :param category: Категория
        :return:
        """

        last_amount = int(last_amount)
        new_amount = int(new_amount)

        if category == 'Доход':
            self.balance = self.balance + new_amount - last_amount
        else:
            self.balance = self.balance - new_amount - last_amount

    def __get_values_of_line(self, row: list) -> dict:

        """
        :param row: Список значений отчета
        :return: Словарь с данными
        """

        values = {
            'index': row[self.index_position],
            'date': row[self.date_position],
            'category': row[self.category_position],
            'amount': row[self.amount_position],
            'comment': row[self.comment_position]
        }
        return values

    def __serialize_data(self):
        return [report.serialize() for report in self.data]


if __name__ == '__main__':
    db = CSVDataBase()


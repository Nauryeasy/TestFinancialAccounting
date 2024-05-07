from .BaseMenuItem import BaseMenuItem


class AddReport(BaseMenuItem):

    name: str = "Добавить запись о доходе/расходе"

    def execute(self) -> None:
        report = {}
        flag = True
        while flag:
            report['date'] = input("Дата (гггг-мм-дд): ")
            report['category'] = input("Категория: ")
            report['amount'] = input("Сумма: ")
            report['comment'] = input("Комментарий: ")

            flag = False if self.handler.db.add(report) else True

        print("Запись успешно добавлена!")

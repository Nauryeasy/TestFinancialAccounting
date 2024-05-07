from .BaseMenuItem import BaseMenuItem


class CorrectReport(BaseMenuItem):

    name: str = "Изменить запись о доходе/расходе"

    def execute(self) -> None:
        print('Укажите индекс записи, которую хотите изменить')

        try:
            index = int(input())
        except:
            print('Некорректный ввод')
            return

        try:
            report = self.handler.db.find_by_index(index)
        except ValueError as e:
            print(e)
            return

        print(f'{report.index}. {report.date} {report.category} {report.amount} {report.comment}')
        print('Вы желаете изменить эту запись? 1 - да, 0 - нет')
        try:
            choice = int(input())
        except:
            print('Некорректный ввод')
            return

        if choice == 1:
            report_dict = {}

            report_dict['index'] = report.index
            report_dict['date'] = input("Дата (гггг-мм-дд): ")
            report_dict['category'] = input("Категория: ")
            report_dict['amount'] = input("Сумма: ")
            report_dict['comment'] = input("Комментарий: ")

            result = self.handler.db.update_by_index(index, report_dict)

            if result:
                print('Запись изменена')

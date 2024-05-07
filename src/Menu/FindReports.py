from .BaseMenuItem import BaseMenuItem


class FindReports(BaseMenuItem):

    name: str = "Поиск записей"

    def execute(self) -> None:

        date_from = None
        date_to = None
        category = None
        amount_from = None
        amount_to = None

        print('Указать дату? (гггг-мм-дд): 1 - да, 0 - нет')
        choice = self.check_int_input()
        if choice == 1:
            date_from = input('Укажите дату начала (гггг-мм-дд): ')
            date_to = input('Укажите дату окончания (гггг-мм-дд): ')

        print('Указать категорию? 1 - да, 0 - нет')
        choice = self.check_int_input()
        if choice == 1:
            category = input('Укажите категорию: ')

        print('Указать сумму? 1 - да, 0 - нет')
        choice = self.check_int_input()
        if choice == 1:
            amount_from = input('Укажите начальную сумму: ')
            amount_to = input('Укажите конечную сумму: ')

        try:
            reports = self.handler.db.find(date_from, date_to, category, amount_from, amount_to)
        except ValueError as e:
            print(e)
            return

        for report in reports:
            print(f'{report.index}. {report.date} {report.category} {report.amount} {report.comment}')

        print('')

    @staticmethod
    def check_int_input() -> int:
        try:
            return int(input())
        except:
            return 0

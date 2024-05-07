from .BaseMenuItem import BaseMenuItem


class GetBalance(BaseMenuItem):

    name: str = "Посмотреть баланс"

    def execute(self) -> None:
        print(f"Баланс на текущий момент: {self.handler.db.balance}")
        print('Посмотреть расходы и доходы?')
        choice = input('1 - Да, 2 - Нет: ')
        if choice == '1' or choice == 'Да':
            print('Выбрать дату? (Иначе за все время)')
            choice = input('1 - Да, 2 - Нет: ')
            if choice == '1' or choice == 'Да':
                date_from = input('Введите дату начала (гггг-мм-дд): ')
                date_to = input('Введите дату окончания (гггг-мм-дд): ')
                try:
                    income = [i.amount for i in self.handler.db.find(date_from, date_to, 'Доход')]
                    expense = [i.amount for i in self.handler.db.find(date_from, date_to, 'Расход')]
                except ValueError:
                    print('Неверные даты')
                    return
                print(f'Всего доходов: {sum(income)}')
                print(f'Всего расходов: {sum(expense)}')
            else:
                income = [i.amount for i in self.handler.db.find(None, None, 'Доход')]
                expense = [i.amount for i in self.handler.db.find(None, None, 'Расход')]
                print(f'Всего доходов: {sum(income)}')
                print(f'Всего расходов: {sum(expense)}')
        else:
            pass

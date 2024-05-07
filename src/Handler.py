from . import CSVDataBase
from .Menu import get_menu
from src.Menu import BaseMenuItem


class Handler:

    def __init__(self, db: CSVDataBase) -> None:
        self.menu: list[BaseMenuItem] = [cls(self) for cls in get_menu()]
        self.db = db

    def start(self) -> None:
        while True:
            print('\n'.join([str(i + 1) + '. ' + item.name for i, item in enumerate(self.menu)]))
            try:
                choice = int(input("Выберите пункт меню: "))
            except ValueError:
                print("Некорректный ввод")
                continue

            if choice < 1 or choice > len(self.menu):
                print("Некорректный ввод")
                continue

            self.menu[choice - 1].execute()

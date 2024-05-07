from src import Handler, CSVDataBase

DB = CSVDataBase()
handler = Handler(DB)


if __name__ == '__main__':
    try:
        handler.start()
    except KeyboardInterrupt:
        print("\nBye!")
    finally:
        DB.save()

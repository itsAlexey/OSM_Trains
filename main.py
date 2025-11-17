import sys

def main():
    """
    Функция для управления приложением.
    """
    BBOX_MOSCOW = (55.5, 37.3, 55.9, 37.9)

    if len(sys.argv) < 2:
        print("Ошибка: не указана команда.")
        print("Использование:")
        print("  python main.py import    - для загрузки данных из OSM в базу данных")
        print("  python main.py runserver - для запуска веб-приложения")
        return

    command = sys.argv[1]

    if command == "import":
        # Импортируем функцию 'run_import' только когда она нужна
        from import_data import run_import
        run_import(bbox=BBOX_MOSCOW)

    elif command == "runserver":
        # Импортируем объект 'app' только когда он нужен
        from app import app
        print("Запуск веб-сервера... Откройте http://127.0.0.1:5000 в браузере.")
        app.run(debug=True)

    else:
        print(f"Ошибка: неизвестная команда '{command}'")
        print("Доступные команды: 'import', 'runserver'")


if __name__ == "__main__":
    main()

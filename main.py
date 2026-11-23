from logic import TaskManager
from storage import Storage
from ui import ConsoleUI


def main() -> None:
    storage = Storage()
    manager = TaskManager(storage)

    try:
        manager.load()
    except ValueError as error:
        print(f"Предупреждение: {error}")
        print("Начинаем с пустого списка дел")
        manager.tasks = []

    ui = ConsoleUI(manager)
    ui.run()

    manager.save()
    print("Данные сохранены")


if __name__ == "__main__":
    main()

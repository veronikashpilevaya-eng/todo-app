from collections.abc import Callable

from logic import Task, TaskManager


class ConsoleUI:
    """Консольный интерфейс приложения."""

    def __init__(
        self,
        manager: TaskManager,
        save_callback: Callable[[list[Task]], None] | None = None,
    ):
        self.manager = manager
        self.save_callback = save_callback

    def print_menu(self) -> None:
        print("\n=== Список дел ===")
        print("1. Добавить дело")
        print("2. Показать все дела")
        print("3. Отметить дело выполненным")
        print("4. Удалить дело")
        print("5. Показать только невыполненные")
        print("6. Найти дело по названию")
        print("0. Выход")

    def print_tasks(self, tasks: list[Task] | None = None) -> None:
        items = self.manager.get_all() if tasks is None else tasks
        if not items:
            print("Список пуст")
            return
        for number, task in enumerate(items, start=1):
            print(f"{number}. {task}")

    def _save(self) -> None:
        if self.save_callback is not None:
            try:
                self.save_callback(self.manager.get_all())
            except OSError as error:
                print(f"Не удалось сохранить данные: {error}")

    def add_flow(self) -> None:
        title = input("Название дела: ").strip()
        deadline = input("Срок (ГГГГ-ММ-ДД): ").strip()
        try:
            self.manager.add_task(title, deadline)
            self._save()
            print("Дело добавлено")
        except ValueError as error:
            print(f"Ошибка: {error}")

    def mark_done_flow(self) -> None:
        title = input("Название выполненного дела: ").strip()
        try:
            self.manager.mark_done(title)
            self._save()
            print("Дело отмечено выполненным")
        except ValueError as error:
            print(f"Ошибка: {error}")

    def remove_flow(self) -> None:
        title = input("Название дела для удаления: ").strip()
        try:
            self.manager.remove_task(title)
            self._save()
            print("Дело удалено")
        except ValueError as error:
            print(f"Ошибка: {error}")

    def run(self) -> None:
        while True:
            self.print_menu()
            choice = input("Выберите пункт: ").strip()
            if choice == "1":
                self.add_flow()
            elif choice == "2":
                self.print_tasks()
            elif choice == "3":
                self.mark_done_flow()
            elif choice == "4":
                self.remove_flow()
            elif choice == "5":
                self.print_tasks(self.manager.get_pending())
            elif choice == "6":
                fragment = input("Введите часть названия: ").strip()
                try:
                    self.print_tasks(self.manager.find_by_title(fragment))
                except ValueError as error:
                    print(f"Ошибка: {error}")
            elif choice == "0":
                print("До свидания!")
                return
            else:
                print("Нет такого пункта меню")


def run_app(
    tasks: list[Task],
    save_callback: Callable[[list[Task]], None],
) -> None:
    """Совместимость с прежним способом запуска приложения."""
    ConsoleUI(TaskManager(tasks), save_callback).run()

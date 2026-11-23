from collections.abc import Callable

from logic import Task, add_task, delete_task, mark_task_done


def print_menu() -> None:
    print("\n===== TO-DO LIST =====")
    print("1. Показать задачи")
    print("2. Добавить задачу")
    print("3. Отметить задачу выполненной")
    print("4. Удалить задачу")
    print("0. Выход")


def _show_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("\nСписок задач пуст.")
        return

    print("\nВаши задачи:")
    for position, task in enumerate(tasks, start=1):
        status = "выполнена" if task.done else "не выполнена"
        print(f"{position}. [{status}] {task.title} (срок: {task.deadline})")


def _read_position(prompt: str, tasks: list[Task]) -> int | None:
    raw_position = input(prompt).strip()
    try:
        position = int(raw_position)
    except ValueError:
        print("Введите целый номер задачи.")
        return None

    if position < 1 or position > len(tasks):
        print("Задачи с таким номером нет.")
        return None
    return position


def _save_after_change(
    tasks: list[Task], save_callback: Callable[[list[Task]], None]
) -> bool:
    try:
        save_callback(tasks)
    except OSError as error:
        print(f"Не удалось сохранить задачи: {error}")
        return False
    return True


def run_app(
    tasks: list[Task], save_callback: Callable[[list[Task]], None]
) -> None:
    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "0":
            print("До свидания!")
            return
        if choice == "1":
            _show_tasks(tasks)
        elif choice == "2":
            title = input("Название задачи: ").strip()
            deadline = input("Срок выполнения: ").strip()
            try:
                add_task(tasks, title, deadline)
            except ValueError as error:
                print(error)
                continue
            if _save_after_change(tasks, save_callback):
                print("Задача добавлена.")
            else:
                print("Задача добавлена в текущий список, но не сохранена на диск.")
        elif choice == "3":
            if not tasks:
                print("Список задач пуст.")
                continue
            _show_tasks(tasks)
            position = _read_position("Номер выполненной задачи: ", tasks)
            if position is None:
                continue
            if mark_task_done(tasks, position):
                if _save_after_change(tasks, save_callback):
                    print("Задача отмечена как выполненная.")
                else:
                    print(
                        "Статус изменён в текущем списке, "
                        "но не сохранён на диск."
                    )
            else:
                print("Эта задача уже выполнена.")
        elif choice == "4":
            if not tasks:
                print("Список задач пуст.")
                continue
            _show_tasks(tasks)
            position = _read_position("Номер задачи для удаления: ", tasks)
            if position is None:
                continue
            deleted_task = delete_task(tasks, position)
            if _save_after_change(tasks, save_callback):
                print(f"Задача «{deleted_task.title}» удалена.")
            else:
                print(
                    f"Задача «{deleted_task.title}» удалена из текущего списка, "
                    "но изменение не сохранено на диск."
                )
        else:
            print("Неизвестный пункт меню. Введите число от 0 до 4.")

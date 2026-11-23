from json import JSONDecodeError

from logic import TaskManager
from storage import load_tasks, save_tasks
from ui import ConsoleUI


def main() -> int:
    try:
        manager = TaskManager(load_tasks())
    except (OSError, JSONDecodeError, ValueError) as error:
        print(f"Не удалось загрузить задачи: {error}")
        return 1

    ui = ConsoleUI(manager, save_tasks)
    ui.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

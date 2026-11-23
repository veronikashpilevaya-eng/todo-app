from json import JSONDecodeError

from storage import load_tasks, save_tasks
from ui import run_app


def main() -> int:
    try:
        tasks = load_tasks()
    except (OSError, JSONDecodeError, ValueError) as error:
        print(f"Не удалось загрузить задачи: {error}")
        return 1

    run_app(tasks, save_tasks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

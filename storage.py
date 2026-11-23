import json
from pathlib import Path

from logic import Task


TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks(path: Path = TASKS_FILE) -> list[Task]:
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    if not isinstance(data, list):
        raise ValueError("Корневой элемент JSON должен быть списком задач.")

    tasks = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Запись задачи №{index} должна быть объектом.")
        try:
            tasks.append(
                Task(
                    title=item["title"],
                    deadline=item["deadline"],
                    done=item.get("done", False),
                )
            )
        except KeyError as error:
            raise ValueError(
                f"В задаче №{index} отсутствует поле {error.args[0]!r}."
            ) from error
        except ValueError as error:
            raise ValueError(f"Некорректная задача №{index}: {error}") from error

    return tasks


def save_tasks(tasks: list[Task], path: Path = TASKS_FILE) -> None:
    data = [
        {"title": task.title, "deadline": task.deadline, "done": task.done}
        for task in tasks
    ]
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")

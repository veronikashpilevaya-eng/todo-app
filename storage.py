import json
import os
from pathlib import Path

from logic import Task


TASKS_FILE = Path(__file__).with_name("tasks.json")


class Storage:
    """Отвечает за чтение и запись списка дел в JSON-файл."""

    def __init__(self, path: str | Path = TASKS_FILE):
        self.path = Path(path)

    def save(self, tasks: list[Task]) -> None:
        data = [task.to_dict() for task in tasks]
        backup_path = self.path.with_suffix(self.path.suffix + ".bak")
        if self.path.exists():
            os.replace(self.path, backup_path)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")

    def load(self) -> list[Task]:
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        if not isinstance(data, list):
            raise ValueError("Хранилище повреждено: ожидается список дел")
        tasks = []
        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Хранилище повреждено: запись №{index} должна быть словарём"
                )
            try:
                tasks.append(Task.from_dict(item))
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Хранилище повреждено: некорректная запись №{index}: {error}"
                ) from error
        return tasks


def load_tasks(path: str | Path = TASKS_FILE) -> list[Task]:
    return Storage(path).load()


def save_tasks(tasks: list[Task], path: str | Path = TASKS_FILE) -> None:
    Storage(path).save(tasks)

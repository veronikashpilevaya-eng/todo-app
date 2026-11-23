from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storage import Storage


class Task:
    """Дело в списке дел."""

    def __init__(self, title: str, deadline: str, done: bool = False):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название дела не может быть пустым")
        if not isinstance(deadline, str) or not deadline.strip():
            raise ValueError("Срок выполнения не может быть пустым")
        if not isinstance(done, bool):
            raise ValueError("Статус дела должен иметь логическое значение")
        self.title = title.strip()
        self.deadline = deadline.strip()
        self.done = done

    def to_dict(self) -> dict:
        """Преобразует задачу в словарь для сохранения в JSON."""
        return {
            "title": self.title,
            "deadline": self.deadline,
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создаёт задачу из словаря."""
        return cls(data["title"], data["deadline"], data.get("done", False))

    def mark_done(self) -> None:
        """Отмечает дело выполненным."""
        self.done = True

    def __str__(self) -> str:
        status = "[x]" if self.done else "[ ]"
        return f"{status} {self.title} (срок: {self.deadline})"


class TaskManager:
    """Управляет списком дел."""

    def __init__(
        self,
        storage: Storage | None = None,
        tasks: list[Task] | None = None,
    ):
        self.storage = storage
        self.tasks: list[Task] = list(tasks) if tasks is not None else []

    def load(self) -> None:
        """Загружает задачи из подключённого хранилища."""
        if self.storage is not None:
            self.tasks = self.storage.load()

    def save(self) -> None:
        """Сохраняет задачи в подключённое хранилище."""
        if self.storage is not None:
            self.storage.save(self.get_all())

    def add_task(self, title: str, deadline: str) -> Task:
        task = Task(title, deadline)
        self.tasks.append(task)
        return task

    def remove_task(self, title: str) -> None:
        title = title.strip()
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return
        raise ValueError(f"Дело «{title}» не найдено")

    def mark_done(self, title: str) -> None:
        title = title.strip()
        for task in self.tasks:
            if task.title == title:
                task.mark_done()
                return
        raise ValueError(f"Дело «{title}» не найдено")

    def get_all(self) -> list[Task]:
        """Возвращает копию списка дел."""
        return list(self.tasks)

    def get_pending(self) -> list[Task]:
        """Возвращает только невыполненные дела."""
        return [task for task in self.tasks if not task.done]

    def count(self) -> int:
        return len(self.tasks)

    def find_by_title(self, fragment: str) -> list[Task]:
        """Ищет дела по фрагменту названия без учёта регистра."""
        fragment = fragment.strip().lower()
        if not fragment:
            raise ValueError("Введите текст для поиска")
        return [
            task for task in self.tasks
            if fragment in task.title.lower()
        ]

    def get_sorted_by_deadline(self) -> list[Task]:
        """Возвращает задачи, отсортированные по сроку выполнения."""
        return sorted(self.tasks, key=lambda task: task.deadline)


# Функции сохранены для совместимости с предыдущими версиями проекта.
def add_task(tasks: list[Task], title: str, deadline: str) -> Task:
    task = Task(title, deadline)
    tasks.append(task)
    return task


def mark_task_done(tasks: list[Task], position: int) -> bool:
    if position < 1 or position > len(tasks):
        raise IndexError("Задачи с таким номером нет.")
    task = tasks[position - 1]
    if task.done:
        return False
    task.mark_done()
    return True


def delete_task(tasks: list[Task], position: int) -> Task:
    if position < 1 or position > len(tasks):
        raise IndexError("Задачи с таким номером нет.")
    return tasks.pop(position - 1)

from dataclasses import dataclass


@dataclass
class Task:
    title: str
    deadline: str
    done: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Название задачи не может быть пустым.")
        if not isinstance(self.deadline, str) or not self.deadline.strip():
            raise ValueError("Срок выполнения не может быть пустым.")
        if not isinstance(self.done, bool):
            raise ValueError("Статус задачи должен быть логическим значением.")

        self.title = self.title.strip()
        self.deadline = self.deadline.strip()

    def mark_done(self) -> None:
        """Отмечает дело выполненным."""
        self.done = True

    def __str__(self) -> str:
        status = "выполнено" if self.done else "не выполнено"
        return f"{self.title} (до {self.deadline}) — {status}"


def add_task(tasks: list[Task], title: str, deadline: str) -> Task:
    task = Task(title=title, deadline=deadline)
    tasks.append(task)
    return task


def _get_task(tasks: list[Task], position: int) -> Task:
    if position < 1 or position > len(tasks):
        raise IndexError("Задачи с таким номером нет.")
    return tasks[position - 1]


def mark_task_done(tasks: list[Task], position: int) -> bool:
    task = _get_task(tasks, position)
    if task.done:
        return False
    task.mark_done()
    return True


def delete_task(tasks: list[Task], position: int) -> Task:
    _get_task(tasks, position)
    return tasks.pop(position - 1)

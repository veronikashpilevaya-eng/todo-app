import unittest

from logic import Task, TaskManager


class TestTask(unittest.TestCase):
    def test_mark_done(self):
        task = Task("Дело", "2025-11-01")
        self.assertFalse(task.done)
        task.mark_done()
        self.assertTrue(task.done)

    def test_empty_title_raises(self):
        with self.assertRaises(ValueError):
            Task(" ", "2025-11-01")

    def test_string_representation(self):
        task = Task("Купить хлеб", "2025-11-01")
        self.assertEqual(str(task), "[ ] Купить хлеб (срок: 2025-11-01)")
        task.mark_done()
        self.assertEqual(str(task), "[x] Купить хлеб (срок: 2025-11-01)")


class TestTaskManager(unittest.TestCase):
    def test_add_and_count(self):
        manager = TaskManager()
        manager.add_task("Дело 1", "2025-11-01")
        manager.add_task("Дело 2", "2025-11-02")
        self.assertEqual(manager.count(), 2)

    def test_remove_missing_raises(self):
        manager = TaskManager()
        with self.assertRaises(ValueError):
            manager.remove_task("Нет такого")

    def test_mark_done_and_pending(self):
        manager = TaskManager()
        manager.add_task("Купить хлеб", "2025-11-01")
        manager.add_task("Полить цветы", "2025-11-03")
        manager.mark_done("Купить хлеб")
        self.assertEqual(
            [str(task) for task in manager.get_pending()],
            ["[ ] Полить цветы (срок: 2025-11-03)"],
        )

    def test_get_all_returns_copy(self):
        manager = TaskManager()
        manager.add_task("Дело", "2025-11-01")
        copied = manager.get_all()
        copied.clear()
        self.assertEqual(manager.count(), 1)

    def test_find_by_title_case_insensitive(self):
        manager = TaskManager()
        manager.add_task("Купить Хлеб", "2025-11-01")
        self.assertEqual(len(manager.find_by_title("хЛеБ")), 1)


if __name__ == "__main__":
    unittest.main()

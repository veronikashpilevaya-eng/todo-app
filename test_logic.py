import unittest

from logic import Task, TaskManager


class TestTask(unittest.TestCase):
    def test_default_not_done(self):
        self.assertFalse(Task("Дело", "2025-11-01").done)

    def test_mark_done(self):
        task = Task("Дело", "2025-11-01")
        task.mark_done()
        self.assertTrue(task.done)

    def test_title_is_stripped(self):
        self.assertEqual(Task(" Хлеб ", "2025-11-01").title, "Хлеб")

    def test_empty_title_raises(self):
        with self.assertRaises(ValueError):
            Task("", "2025-11-01")

    def test_spaces_only_title_raises(self):
        with self.assertRaises(ValueError):
            Task(" ", "2025-11-01")

    def test_empty_and_blank_titles_raise(self):
        for bad in ["", " ", "\t\n", " \t "]:
            with self.subTest(title=repr(bad)):
                with self.assertRaises(ValueError):
                    Task(bad, "2025-11-01")

    def test_to_dict(self):
        task = Task("Купить хлеб", "2025-11-01", True)
        self.assertEqual(
            task.to_dict(),
            {"title": "Купить хлеб", "deadline": "2025-11-01", "done": True},
        )

    def test_from_dict(self):
        task = Task.from_dict(
            {"title": "Купить хлеб", "deadline": "2025-11-01", "done": True}
        )
        self.assertEqual(str(task), "[x] Купить хлеб (срок: 2025-11-01)")

    def test_from_dict_default_done(self):
        task = Task.from_dict({"title": "Дело", "deadline": "2025-11-01"})
        self.assertFalse(task.done)

    def test_from_dict_missing_title_raises(self):
        with self.assertRaises(KeyError):
            Task.from_dict({"deadline": "2025-11-01"})

    def test_valid_date(self):
        self.assertEqual(Task("Дело", "2025-11-01").deadline, "2025-11-01")

    def test_invalid_date_format_raises(self):
        with self.assertRaisesRegex(ValueError, "Срок должен быть в формате"):
            Task("Дело", "завтра")

    def test_invalid_calendar_date_raises(self):
        with self.assertRaises(ValueError):
            Task("Дело", "2025-13-40")


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
        self.manager.add_task("Хлеб", "2025-11-01")
        self.manager.add_task("Цветы", "2025-11-03")

    def test_add_and_count(self):
        self.assertEqual(self.manager.count(), 2)

    def test_get_all_returns_copy(self):
        tasks = self.manager.get_all()
        tasks.pop()
        self.assertEqual(self.manager.count(), 2)

    def test_mark_done_and_get_pending(self):
        self.manager.mark_done("Хлеб")
        self.assertEqual([task.title for task in self.manager.get_pending()], ["Цветы"])

    def test_remove_existing(self):
        self.manager.remove_task("Хлеб")
        self.assertEqual(self.manager.count(), 1)

    def test_remove_missing_raises(self):
        with self.assertRaises(ValueError):
            self.manager.remove_task("Нет такого")

    def test_mark_done_missing_raises(self):
        with self.assertRaises(ValueError):
            self.manager.mark_done("Нет такого")

    def test_get_sorted_by_deadline(self):
        result = self.manager.get_sorted_by_deadline()
        self.assertEqual([task.title for task in result], ["Хлеб", "Цветы"])


def test_title_is_stripped_pytest_style():
    task = Task(" Хлеб ", "2025-11-01")
    assert task.title == "Хлеб"


if __name__ == "__main__":
    unittest.main()

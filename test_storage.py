import json
import os
import tempfile
import unittest

from logic import Task, TaskManager
from storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmpdir.name, "tasks.json")
        self.storage = Storage(self.path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_missing_file_returns_empty(self):
        self.assertEqual(self.storage.load(), [])

    def test_save_and_load_roundtrip(self):
        tasks = [Task("Хлеб", "2025-11-01", True), Task("Цветы", "2025-11-03")]
        self.storage.save(tasks)
        loaded = self.storage.load()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Хлеб")
        self.assertTrue(loaded[0].done)
        self.assertFalse(loaded[1].done)

    def test_saved_json_contains_russian_text(self):
        self.storage.save([Task("Купить хлеб", "2025-11-01")])
        with open(self.path, "r", encoding="utf-8") as file:
            self.assertIn("Купить хлеб", file.read())

    def test_corrupted_file_raises(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{это не json")
        with self.assertRaises(ValueError):
            self.storage.load()

    def test_not_a_list_raises(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump({"title": "вместо списка"}, file, ensure_ascii=False)
        with self.assertRaises(ValueError):
            self.storage.load()

    def test_invalid_task_record_raises(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump([{"deadline": "2025-11-01"}], file)
        with self.assertRaises(ValueError):
            self.storage.load()

    def test_backup_is_created_before_overwrite(self):
        self.storage.save([Task("Старое дело", "2025-11-01")])
        self.storage.save([Task("Новое дело", "2025-11-02")])
        backup = self.path + ".bak"
        with open(backup, "r", encoding="utf-8") as file:
            previous_data = json.load(file)
        self.assertEqual(previous_data[0]["title"], "Старое дело")
        self.assertEqual(self.storage.load()[0].title, "Новое дело")

    def test_manager_autosaves_operations(self):
        manager = TaskManager(self.storage)
        manager.add_task("Хлеб", "2025-11-01")
        self.assertEqual(self.storage.load()[0].title, "Хлеб")
        manager.mark_done("Хлеб")
        self.assertTrue(self.storage.load()[0].done)
        manager.remove_task("Хлеб")
        self.assertEqual(self.storage.load(), [])


if __name__ == "__main__":
    unittest.main()

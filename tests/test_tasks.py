import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta

import reports
import search
import validation
from storage import load_tasks
from task import Task
from task_manager import TaskManager


class TestTasks(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.folder.name, "data", "tasks.json")
        self.manager = TaskManager(self.file_path)

    def tearDown(self):
        self.folder.cleanup()

    def add_sample(self, title="Sample", due_date="05-10-2026",
                   priority="High", due_time="18:30"):
        return self.manager.add_task(title, "Sample description", "College",
                                     priority, due_date, due_time)

    def test_create_task(self):
        task = Task(1, "Study", "Read chapter 1", "College", "High",
                    "05-10-2026", "18:30")
        self.assertEqual(task.title, "Study")
        self.assertEqual(task.status, "Pending")
        self.assertTrue(validation.is_valid_date(task.created_date))
        self.assertTrue(validation.is_valid_time(task.created_time))

    def test_missing_file_is_created(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.assertEqual(self.manager.get_all_tasks(), [])

    def test_add_task(self):
        task = self.add_sample()
        self.assertEqual(task.task_id, 1)
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
        second = self.add_sample("Second")
        self.assertEqual(second.task_id, 2)

    def test_update_task(self):
        task = self.add_sample()
        self.manager.update_task(task.task_id, title="New Title", priority="Low")
        updated = self.manager.get_task(task.task_id)
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.priority, "Low")
        self.assertEqual(updated.category, "College")

    def test_update_missing_task(self):
        self.assertIsNone(self.manager.update_task(99, title="X"))

    def test_delete_task(self):
        task = self.add_sample()
        self.assertTrue(self.manager.delete_task(task.task_id))
        self.assertIsNone(self.manager.get_task(task.task_id))
        self.assertFalse(self.manager.delete_task(task.task_id))

    def test_complete_and_pending(self):
        task = self.add_sample()
        self.manager.mark_completed(task.task_id)
        self.assertEqual(self.manager.get_task(task.task_id).status, "Completed")
        self.manager.mark_pending(task.task_id)
        self.assertEqual(self.manager.get_task(task.task_id).status, "Pending")

    def test_tasks_are_saved_to_file(self):
        self.add_sample("Saved Task")
        new_manager = TaskManager(self.file_path)
        self.assertEqual(len(new_manager.get_all_tasks()), 1)
        self.assertEqual(new_manager.get_all_tasks()[0].title, "Saved Task")

    def test_empty_file(self):
        with open(self.file_path, "w") as file:
            file.write("")
        self.assertEqual(load_tasks(self.file_path), [])

    def test_corrupted_file(self):
        with open(self.file_path, "w") as file:
            file.write("{not valid json")
        self.assertEqual(load_tasks(self.file_path), [])
        with open(self.file_path) as file:
            self.assertEqual(json.load(file), [])

    def test_invalid_date(self):
        self.assertTrue(validation.is_valid_date("05-10-2026"))
        self.assertFalse(validation.is_valid_date("31-02-2026"))
        self.assertFalse(validation.is_valid_date("2026-10-05"))
        self.assertFalse(validation.is_valid_date("abc"))
        self.assertFalse(validation.is_valid_date(""))

    def test_invalid_time(self):
        self.assertTrue(validation.is_valid_time("18:30"))
        self.assertFalse(validation.is_valid_time("25:00"))
        self.assertFalse(validation.is_valid_time("12:60"))
        self.assertFalse(validation.is_valid_time("abc"))
        self.assertFalse(validation.is_valid_time(""))

    def test_priority_category_and_menu_validation(self):
        self.assertTrue(validation.is_valid_priority("high"))
        self.assertFalse(validation.is_valid_priority("urgent"))
        self.assertTrue(validation.is_valid_category("college"))
        self.assertFalse(validation.is_valid_category("Games"))
        self.assertTrue(validation.is_valid_menu_choice("5", 1, 14))
        self.assertFalse(validation.is_valid_menu_choice("abc", 1, 14))
        self.assertFalse(validation.is_valid_menu_choice("15", 1, 14))
        self.assertFalse(validation.is_not_empty("   "))

    def test_overdue_today_tomorrow(self):
        now = datetime.now()
        yesterday = (now - timedelta(days=1)).strftime("%d-%m-%Y")
        today = now.strftime("%d-%m-%Y")
        tomorrow = (now + timedelta(days=1)).strftime("%d-%m-%Y")
        self.add_sample("Old", yesterday)
        self.add_sample("Today", today, due_time="23:59")
        self.add_sample("Tomorrow", tomorrow)
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(search.get_overdue_tasks(tasks, now)), 1)
        self.assertEqual(len(search.get_today_tasks(tasks, now)), 1)
        self.assertEqual(len(search.get_tomorrow_tasks(tasks, now)), 1)

    def test_completed_task_is_not_overdue(self):
        task = self.add_sample("Old", "01-01-2020")
        self.assertTrue(task.is_overdue())
        self.manager.mark_completed(task.task_id)
        self.assertFalse(task.is_overdue())

    def test_search_and_filter(self):
        self.add_sample("Python Assignment", priority="High")
        self.add_sample("Buy milk", priority="Low")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(search.search_by_title(tasks, "python")), 1)
        self.assertEqual(len(search.search_by_category(tasks, "college")), 2)
        self.assertEqual(len(search.filter_by_priority(tasks, "Low")), 1)
        self.assertEqual(len(search.filter_by_category(tasks, "Work")), 0)

    def test_sorting(self):
        self.add_sample("Later", "10-10-2026")
        self.add_sample("Sooner", "01-10-2026")
        third = self.add_sample("Done", "01-09-2026")
        self.manager.mark_completed(third.task_id)
        ordered = search.sort_tasks(self.manager.get_all_tasks())
        self.assertEqual([t.title for t in ordered], ["Sooner", "Later", "Done"])

    def test_statistics(self):
        self.add_sample("A", "01-01-2020", "High")
        b = self.add_sample("B", "01-01-2030", "Medium")
        self.add_sample("C", "01-01-2030", "Low")
        self.manager.mark_completed(b.task_id)
        stats = reports.get_statistics(self.manager.get_all_tasks())
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 2)
        self.assertEqual(stats["high"], 1)
        self.assertEqual(stats["medium"], 1)
        self.assertEqual(stats["low"], 1)
        self.assertEqual(stats["overdue"], 1)


if __name__ == "__main__":
    unittest.main()

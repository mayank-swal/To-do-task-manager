from storage import DATA_FILE, load_tasks, save_tasks
from task import Task


class TaskManager:
    def __init__(self, file_path=DATA_FILE):
        self.file_path = file_path
        self.tasks = load_tasks(file_path)

    def save(self):
        return save_tasks(self.tasks, self.file_path)

    def generate_id(self):
        if len(self.tasks) == 0:
            return 1
        highest = 0
        for task in self.tasks:
            if task.task_id > highest:
                highest = task.task_id
        return highest + 1

    def add_task(self, title, description, category, priority, due_date, due_time):
        task = Task(self.generate_id(), title, description, category,
                    priority, due_date, due_time)
        self.tasks.append(task)
        self.save()
        return task

    def get_all_tasks(self):
        return list(self.tasks)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def update_task(self, task_id, title="", description="", category="",
                    priority="", due_date="", due_time=""):
        task = self.get_task(task_id)
        if task is None:
            return None
        if title != "":
            task.title = title
        if description != "":
            task.description = description
        if category != "":
            task.category = category
        if priority != "":
            task.priority = priority
        if due_date != "":
            task.due_date = due_date
        if due_time != "":
            task.due_time = due_time
        self.save()
        return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self.save()
        return True

    def mark_completed(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            return None
        task.status = "Completed"
        self.save()
        return task

    def mark_pending(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            return None
        task.status = "Pending"
        self.save()
        return task

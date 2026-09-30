from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M"


class Task:
    def __init__(self, task_id, title, description, category, priority,
                 due_date, due_time, created_date=None, created_time=None,
                 status="Pending"):
        now = datetime.now()
        self.task_id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.due_time = due_time
        self.created_date = created_date or now.strftime(DATE_FORMAT)
        self.created_time = created_time or now.strftime(TIME_FORMAT)
        self.status = status

    def get_due_datetime(self):
        text = self.due_date + " " + self.due_time
        return datetime.strptime(text, DATE_FORMAT + " " + TIME_FORMAT)

    def is_completed(self):
        return self.status == "Completed"

    def is_overdue(self, now=None):
        if now is None:
            now = datetime.now()
        if self.is_completed():
            return False
        return self.get_due_datetime() < now

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "due_date": self.due_date,
            "due_time": self.due_time,
            "created_date": self.created_date,
            "created_time": self.created_time,
            "status": self.status,
        }

    def short_text(self):
        lines = [
            "ID: " + str(self.task_id),
            "Title: " + self.title,
            "Category: " + self.category,
            "Priority: " + self.priority,
            "Due: " + self.due_date + " " + self.due_time,
            "Status: " + self.status,
        ]
        if self.is_overdue():
            lines.append("** OVERDUE **")
        return "\n".join(lines)

    def full_text(self):
        lines = [
            "ID: " + str(self.task_id),
            "Title: " + self.title,
            "Description: " + self.description,
            "Category: " + self.category,
            "Priority: " + self.priority,
            "Due: " + self.due_date + " " + self.due_time,
            "Created: " + self.created_date + " " + self.created_time,
            "Status: " + self.status,
        ]
        if self.is_overdue():
            lines.append("** OVERDUE **")
        return "\n".join(lines)


def task_from_dict(data):
    task = Task(
        task_id=int(data["id"]),
        title=str(data["title"]),
        description=str(data["description"]),
        category=str(data["category"]),
        priority=str(data["priority"]),
        due_date=str(data["due_date"]),
        due_time=str(data["due_time"]),
        created_date=str(data["created_date"]),
        created_time=str(data["created_time"]),
        status=str(data["status"]),
    )
    task.get_due_datetime()
    datetime.strptime(task.created_date + " " + task.created_time,
                      DATE_FORMAT + " " + TIME_FORMAT)
    if task.status not in ("Pending", "Completed"):
        raise ValueError("Invalid status")
    return task

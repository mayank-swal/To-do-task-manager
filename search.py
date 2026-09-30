from datetime import datetime, timedelta


def sort_tasks(tasks):
    return sorted(tasks, key=lambda task: (task.is_completed(), task.get_due_datetime()))


def search_by_title(tasks, keyword):
    keyword = keyword.strip().lower()
    return [task for task in tasks if keyword in task.title.lower()]


def search_by_category(tasks, category):
    category = category.strip().lower()
    return [task for task in tasks if category in task.category.lower()]


def filter_by_priority(tasks, priority):
    return [task for task in tasks if task.priority == priority]


def filter_by_category(tasks, category):
    return [task for task in tasks if task.category == category]


def get_pending_tasks(tasks):
    return [task for task in tasks if not task.is_completed()]


def get_completed_tasks(tasks):
    return [task for task in tasks if task.is_completed()]


def get_overdue_tasks(tasks, now=None):
    if now is None:
        now = datetime.now()
    return [task for task in tasks if task.is_overdue(now)]


def get_tasks_due_on(tasks, day):
    return [task for task in tasks if task.get_due_datetime().date() == day]


def get_today_tasks(tasks, now=None):
    if now is None:
        now = datetime.now()
    return get_tasks_due_on(tasks, now.date())


def get_tomorrow_tasks(tasks, now=None):
    if now is None:
        now = datetime.now()
    return get_tasks_due_on(tasks, now.date() + timedelta(days=1))

import json
import os

from task import task_from_dict

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_FOLDER, "data", "tasks.json")


def create_file_if_missing(file_path):
    folder = os.path.dirname(file_path)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([], file)


def handle_corrupted_file(file_path):
    backup_path = file_path + ".corrupted"
    try:
        os.replace(file_path, backup_path)
        print("Task file was damaged. A backup was saved as " + backup_path)
    except OSError:
        print("Task file was damaged and could not be backed up.")
    create_file_if_missing(file_path)


def load_tasks(file_path=DATA_FILE):
    try:
        create_file_if_missing(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except OSError:
        print("Could not read the task file. Starting with no tasks.")
        return []

    if content.strip() == "":
        return []

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        handle_corrupted_file(file_path)
        return []

    if not isinstance(data, list):
        handle_corrupted_file(file_path)
        return []

    tasks = []
    skipped = 0
    for item in data:
        try:
            tasks.append(task_from_dict(item))
        except (KeyError, ValueError, TypeError, AttributeError):
            skipped += 1

    if skipped > 0:
        print("Warning: " + str(skipped) + " invalid task(s) were skipped.")
    return tasks


def save_tasks(tasks, file_path=DATA_FILE):
    data = [task.to_dict() for task in tasks]
    try:
        folder = os.path.dirname(file_path)
        if folder != "" and not os.path.exists(folder):
            os.makedirs(folder)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        print("Error: could not save tasks to file.")
        return False

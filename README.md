# To-Do & Task Management System

## Overview

The To-Do & Task Management System is a command-line application written in Python. It helps a user keep track of daily tasks: add them, edit them, mark them complete, search them, and see reports such as overdue tasks and task statistics.

## Features

- Add, view, update and delete tasks
- View all tasks or one specific task by its ID
- Mark a task as completed, or mark a completed task as pending again
- Priority levels: Low, Medium, High
- Categories: Personal, College, Work, Shopping, Health, Other
- Search tasks by title or by category
- Filter tasks by priority, category, or status (pending / completed)
- View overdue tasks, tasks due today and tasks due tomorrow
- Task summary with statistics (totals, priorities, overdue count, tasks per category)
- Tasks are sorted by completion status, then due date, then due time
- Due date and time validation (`DD-MM-YYYY` and `HH:MM`)
- Creation date and time are recorded automatically
- Data is saved automatically in `data/tasks.json`
- Invalid input never crashes the program
- Unit tests using `unittest`

## Technologies Used

- Python 3
- JSON (data storage)
- `datetime` module (dates and times)
- `unittest` (testing)
- Git / GitHub (version control)

## Project Structure tree

```text
todo-task-management-system/
│
├── main.py             Starts the program, shows the menu, takes user input
├── task.py             holds the data of one task
├── task_manager.py     Add, update, delete, get and complete tasks, create IDs
├── storage.py          Read and write tasks in the JSON file
├── search.py           Search, filter, overdue, today, tomorrow and sorting
├── reports.py          Task statistics and summary
├── validation.py       Checks and asks for valid input
│
├── data/
│   └── tasks.json      Saved tasks
│
├── tests/
│   ├── __init__.py
│   └── test_tasks.py   Unit tests
│
├── README.md
└── requirements.txt
```

| File |                                         |    Purpose |

| `main.py` |                                Menu and user interaction. It calls functions from the other files. |
| `task.py` | `Task`                         class with the fields ID, title, description, category, priority, due  date, due time, created date, created time and status. |
| `task_manager.py` | `TaskManager`          class that keeps the list of tasks and saves after every change. |
| `storage.py` |                             Loads and saves the JSON file. Creates it if missing and handles empty or damaged files. |
| `search.py` |                                Functions that return filtered lists of tasks. |
| `reports.py` |                               Counts tasks and prints the summary. |
| `validation.py` |                             Checks dates, times, priorities, categories and menu choices, and keeps asking until the input is valid. |




## Requirements

- Python 3.8 or higher



## Running the Project

Run this command from the project folder:

```bash
python main.py
```

On Windows you may need:

```bash
py main.py
```

On some Linux/macOS systems use `python3 main.py`.

## Running Tests

```bash
python -m unittest discover
```

The tests cover task creation, adding, updating, deleting, completing, invalid dates and times, file handling, searching, sorting and statistics.

## Data Storage

Tasks are stored in:

```text
data/tasks.json
```

- If the file does not exist, the program creates it automatically.
- If it is empty, the program starts with no tasks.
- If it is damaged, the program keeps a copy named `tasks.json.corrupted` and starts with a fresh file.

## Usage

1. Start the program with `python main.py`.
2. Type the number of a menu option and press Enter.
3. Follow the prompts.

Basic workflow:

1. Choose **1** to add a task. Enter title, description, category, priority, due date (`DD-MM-YYYY`) and due time (`HH:MM`, 24-hour).
2. Choose **2** to see all tasks.
3. Choose **4** to update a task. Press Enter to keep a value unchanged.
4. Choose **6** when a task is done, or **7** to make it pending again.
5. Choose **8** or **9** to search or filter tasks.
6. Choose **10**, **11** or **12** to see overdue, today's or tomorrow's tasks.
7. Choose **13** for the task summary.
8. Choose **14** to exit. Everything is already saved.

Main menu:

```text
========================================
TO-DO & TASK MANAGEMENT SYSTEM
========================================
1. Add Task
2. View All Tasks
3. View Task
4. Update Task
5. Delete Task
6. Mark Task as Completed
7. Mark Task as Pending
8. Search Tasks
9. Filter Tasks
10. View Overdue Tasks
11. View Today's Tasks
12. View Tomorrow's Tasks
13. Task Summary
14. Exit
``` 
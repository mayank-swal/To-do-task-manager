import reports
import search
import validation
from task_manager import TaskManager

LINE = "-" * 60
CATEGORY_TEXT = "Personal/College/Work/Shopping/Health/Other"

def show_menu():
    print("\n" + "=" * 40)
    print("TO-DO & TASK MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Task")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Mark Task as Completed")
    print("7. Mark Task as Pending")
    print("8. Search Tasks")
    print("9. Filter Tasks")
    print("10. View Overdue Tasks")
    print("11. View Today's Tasks")
    print("12. View Tomorrow's Tasks")
    print("13. Task Summary")
    print("14. Exit")

def print_tasks(tasks, heading):
    print("\n" + heading)
    if not tasks:
        print("No tasks found.")
        return
    print(LINE)
    for task in search.sort_tasks(tasks):
        print(task.short_text())
        print(LINE)
    print("Total: " + str(len(tasks)) + " task(s)")

def add_task(manager):
    print("\n--- Add New Task ---")
    title = validation.ask_text("Enter task title: ")
    description = input("Enter description: ").strip()
    category = validation.ask_category("Enter category (" + CATEGORY_TEXT + "): ")
    priority = validation.ask_priority("Enter priority (Low/Medium/High): ")
    due_date = validation.ask_date("Enter due date (DD-MM-YYYY): ")
    due_time = validation.ask_time("Enter due time (HH:MM): ")

    task = manager.add_task(title, description, category, priority, due_date, due_time)
    print("\nTask added successfully!")
    print("Task ID      : " + str(task.task_id))
    print("Created Date : " + task.created_date)
    print("Created Time : " + task.created_time)

def view_all_tasks(manager):
    print_tasks(manager.get_all_tasks(), "ALL TASKS")

def view_task(manager):
    task = manager.get_task(validation.ask_task_id("Enter task ID: "))
    if task is None:
        print("Task not found.")
        return
    print("\n" + LINE)
    print(task.full_text())
    print(LINE)

def update_task(manager):
    task_id = validation.ask_task_id("Enter task ID to update: ")
    task = manager.get_task(task_id)
    if task is None:
        print("Task not found.")
        return

    print("\nCurrent task details:")
    print(LINE)
    print(task.full_text())
    print(LINE)
    print("Press Enter to keep the current value.\n")

    title = input("New title: ").strip()
    description = input("New description: ").strip()
    category = validation.ask_category("New category (" + CATEGORY_TEXT + "): ", True)
    priority = validation.ask_priority("New priority (Low/Medium/High): ", True)
    due_date = validation.ask_date("New due date (DD-MM-YYYY): ", True)
    due_time = validation.ask_time("New due time (HH:MM): ", True)

    manager.update_task(task_id, title, description, category, priority, due_date, due_time)
    print("\nTask updated successfully!")

def delete_task(manager):
    task_id = validation.ask_task_id("Enter task ID to delete: ")
    task = manager.get_task(task_id)
    if task is None:
        print("Task not found.")
        return

    print("Task to delete: " + task.title)
    if validation.ask_yes_no("Are you sure? (y/n): "):
        manager.delete_task(task_id)
        print("Task deleted successfully!")
    else:
        print("Delete cancelled.")

def complete_task(manager):
    task_id = validation.ask_task_id("Enter task ID to mark as completed: ")
    task = manager.get_task(task_id)
    if task is None:
        print("Task not found.")
    elif task.is_completed():
        print("Task is already completed.")
    else:
        manager.mark_completed(task_id)
        print("Task marked as completed!")

def pending_task(manager):
    task_id = validation.ask_task_id("Enter task ID to mark as pending: ")
    task = manager.get_task(task_id)
    if task is None:
        print("Task not found.")
    elif not task.is_completed():
        print("Task is already pending.")
    else:
        manager.mark_pending(task_id)
        print("Task marked as pending!")

def search_tasks(manager):
    print("\n--- Search Tasks ---")
    print("1. Search by title")
    print("2. Search by category")
    print("3. Back to main menu")
    choice = validation.ask_menu_choice("Enter your choice: ", 1, 3)
    tasks = manager.get_all_tasks()

    if choice == 1:
        keyword = validation.ask_text("Enter title to search: ")
        print_tasks(search.search_by_title(tasks, keyword), "SEARCH RESULTS")
    elif choice == 2:
        keyword = validation.ask_text("Enter category to search: ")
        print_tasks(search.search_by_category(tasks, keyword), "SEARCH RESULTS")

def filter_tasks(manager):
    print("\n--- Filter Tasks ---")
    print("1. Filter by priority")
    print("2. Filter by category")
    print("3. Filter by status")
    print("4. Back to main menu")
    choice = validation.ask_menu_choice("Enter your choice: ", 1, 4)
    tasks = manager.get_all_tasks()

    if choice == 1:
        priority = validation.ask_priority("Enter priority (Low/Medium/High): ")
        print_tasks(search.filter_by_priority(tasks, priority), "TASKS WITH " + priority.upper() + " PRIORITY")
    elif choice == 2:
        category = validation.ask_category("Enter category (" + CATEGORY_TEXT + "): ")
        print_tasks(search.filter_by_category(tasks, category), "TASKS IN CATEGORY: " + category.upper())
    elif choice == 3:
        print("1. Pending")
        print("2. Completed")
        status = validation.ask_menu_choice("Enter your choice: ", 1, 2)
        print_tasks(
            search.get_pending_tasks(tasks) if status == 1 else search.get_completed_tasks(tasks),
            "PENDING TASKS" if status == 1 else "COMPLETED TASKS"
        )

def view_overdue(manager):
    print_tasks(search.get_overdue_tasks(manager.get_all_tasks()), "OVERDUE TASKS")

def view_today(manager):
    print_tasks(search.get_today_tasks(manager.get_all_tasks()), "TASKS DUE TODAY")

def view_tomorrow(manager):
    print_tasks(search.get_tomorrow_tasks(manager.get_all_tasks()), "TASKS DUE TOMORROW")

def view_summary(manager):
    reports.print_statistics(manager.get_all_tasks())

def main():
    manager = TaskManager()

    while True:
        show_menu()
        choice = validation.ask_menu_choice("Enter your choice: ", 1, 14)

        if choice == 1:
            add_task(manager)
        elif choice == 2:
            view_all_tasks(manager)
        elif choice == 3:
            view_task(manager)
        elif choice == 4:
            update_task(manager)
        elif choice == 5:
            delete_task(manager)
        elif choice == 6:
            complete_task(manager)
        elif choice == 7:
            pending_task(manager)
        elif choice == 8:
            search_tasks(manager)
        elif choice == 9:
            filter_tasks(manager)
        elif choice == 10:
            view_overdue(manager)
        elif choice == 11:
            view_today(manager)
        elif choice == 12:
            view_tomorrow(manager)
        elif choice == 13:
            view_summary(manager)
        elif choice == 14:
            print("Thank you for using the To-Do & Task Management System. Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
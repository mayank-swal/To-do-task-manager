from datetime import datetime


def get_statistics(tasks, now=None):
    if now is None:
        now = datetime.now()

    stats = {
        "total": len(tasks),
        "completed": 0,
        "pending": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "overdue": 0,
        "categories": {},
    }

    for task in tasks:
        if task.is_completed():
            stats["completed"] += 1
        else:
            stats["pending"] += 1

        if task.priority == "High":
            stats["high"] += 1
        elif task.priority == "Medium":
            stats["medium"] += 1
        elif task.priority == "Low":
            stats["low"] += 1

        if task.is_overdue(now):
            stats["overdue"] += 1

        if task.category in stats["categories"]:
            stats["categories"][task.category] += 1
        else:
            stats["categories"][task.category] = 1

    return stats


def print_statistics(tasks):
    stats = get_statistics(tasks)
    print("\n" + "=" * 40)
    print("TASK SUMMARY")
    print("=" * 40)
    print("Total Tasks     : " + str(stats["total"]))
    print("Completed       : " + str(stats["completed"]))
    print("Pending         : " + str(stats["pending"]))
    print("High Priority   : " + str(stats["high"]))
    print("Medium Priority : " + str(stats["medium"]))
    print("Low Priority    : " + str(stats["low"]))
    print("Overdue         : " + str(stats["overdue"]))

    if stats["categories"]:
        print("\nTasks by Category")
        print("-" * 40)
        for category in sorted(stats["categories"]):
            print(category.ljust(16) + ": " + str(stats["categories"][category]))

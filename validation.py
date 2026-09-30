from datetime import datetime

PRIORITIES = ["Low", "Medium", "High"]
CATEGORIES = ["Personal", "College", "Work", "Shopping", "Health", "Other"]


def is_not_empty(text):
    return text is not None and text.strip() != ""


def is_valid_date(text):
    try:
        datetime.strptime(text.strip(), "%d-%m-%Y")
        return True
    except (ValueError, AttributeError):
        return False


def is_valid_time(text):
    try:
        datetime.strptime(text.strip(), "%H:%M")
        return True
    except (ValueError, AttributeError):
        return False


def normalize_date(text):
    return datetime.strptime(text.strip(), "%d-%m-%Y").strftime("%d-%m-%Y")


def normalize_time(text):
    return datetime.strptime(text.strip(), "%H:%M").strftime("%H:%M")


def is_valid_priority(text):
    return is_not_empty(text) and text.strip().capitalize() in PRIORITIES


def is_valid_category(text):
    return is_not_empty(text) and text.strip().capitalize() in CATEGORIES


def is_valid_menu_choice(text, low, high):
    try:
        number = int(text.strip())
    except ValueError:
        return False
    return low <= number <= high


def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if is_not_empty(value):
            return value
        print("Input cannot be empty. Please try again.")


def ask_priority(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if value == "" and allow_blank:
            return ""
        if is_valid_priority(value):
            return value.capitalize()
        print("Invalid priority. Please enter Low, Medium or High.")


def ask_category(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if value == "" and allow_blank:
            return ""
        if is_valid_category(value):
            return value.capitalize()
        print("Invalid category. Choose: " + ", ".join(CATEGORIES))


def ask_date(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if value == "" and allow_blank:
            return ""
        if is_valid_date(value):
            return normalize_date(value)
        print("Invalid date. Please use DD-MM-YYYY (example: 05-10-2026).")


def ask_time(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if value == "" and allow_blank:
            return ""
        if is_valid_time(value):
            return normalize_time(value)
        print("Invalid time. Please use HH:MM in 24-hour format (example: 18:30).")


def ask_task_id(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid task ID. Please enter a number.")


def ask_menu_choice(prompt, low, high):
    while True:
        value = input(prompt)
        if is_valid_menu_choice(value, low, high):
            return int(value.strip())
        print("Invalid choice. Please try again.")


def ask_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Please enter y or n.")

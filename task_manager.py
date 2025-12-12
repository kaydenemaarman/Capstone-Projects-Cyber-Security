"""
Task Manager Application

This program allows users to:
- Register new users (admin only)
- Add and view tasks
- View and edit their own tasks
- Generate task and user overview reports
- Display task and user statistics (admin only)

The data is stored in 'user.txt' and 'tasks.txt' text files.
Reports are saved to 'task_overview.txt' and 'user_overview.txt'.

Admin credentials:
username: admin
password: password
"""

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# === Helper Functions (abstraction) ===
def reg_user():
    """Register a new user."""
        
    while True:
        # Request details of new user
        new_username = input("New Username: ")

        # Check if username exists
        if new_username in username_password:
            #  Print error message
            print("This username already exists. Please try a different one.\n")
            continue # Ask again for a username

        # If username is unique, continue
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w", encoding="utf-8") as out_file:
                user_data = []
                for username, password in username_password.items():
                    user_data.append(f"{username};{password}")
                out_file.write("\n".join(user_data))
            break # Exit loop once new user is added

        # Otherwise you present a relevant message.
        else:
            print("Passwords do not match")
        
def add_task():
    """Add a new task."""

    # Prompt a user for the following:
    # - A username of the person whom the task is assigned to,
    # - A title of a task,
    # - A description of the task and
    # - the due date of the task.

    # Ask for the username of the person assigned to the task
    task_username = input("Name of person assigned to task: ")

    # Validate username
    while task_username not in username_password:
        print("User does not exist. Please enter a valid username.")
        task_username = input("Name of person assigned to task: ")
        
    # Ask for task title and description
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Ask for due date and validate format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Add task details to dictionary
    current_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": current_date,
        "completed": False
    }

    # Append to the in-memory task list
    task_list.append(new_task)

    # Write all tasks to the file
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
        task_list_to_write = []
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all():
    """View all tasks."""

    for task in task_list:
        display = (
            f"Task: \t\t {task['title']}\n"
            f"Assigned to: \t {task['username']}\n"
            f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            f"Task Description: \n {task['description']}\n"
        )
        print(display)

def view_mine():
    """View my tasks."""

    user_tasks = [task for task in task_list if task['username'] == current_user]

    if not user_tasks:
        print("You have no tasks to display.")
        return

    # Display tasks with numbers
    for i, task in enumerate(user_tasks, start=1): # Add numbering
            display = (
                f"Task {i}:\n"
                f"  Title: {task['title']}\n"
                f"  Assigned to: {task['username']}\n"
                f"  Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                f"  Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                f"  Task Description: {task['description']}\n"
                f"  Completed: {'Yes' if task['completed'] else 'No'}\n"
                f"{'-'*40}\n"
            )
            print(display)

    # Ask the user to select a task number or return to main menu
    while True:
        try:
            task_choice = int(input("\nEnter the task number to view/edit, or -1 to return to the main menu: "))

            if task_choice == -1:
                print("Returning to the main menu...\n")
                return
                
            elif 1 <= task_choice <= len(user_tasks):
                chosen_task = user_tasks[task_choice - 1]

                # Display chosen task title
                print(f"\nYou selected: {chosen_task['title']}")
                print("1 - Mark task as complete")
                print("2 - Edit task")
                print("3 - Return to main menu")

                action = input("Enter your choice: ")

                # === Mark as Complete ===
                if action == "1":
                    if chosen_task['completed']:
                        print("This task is marked as complete.")
                    else:
                        chosen_task['completed'] = True
                        print("Task marked as complete.\n")

                # === Edit task ===
                if action == "2":
                    if chosen_task['completed']:
                        print("You cannot edit a completed task.\n")
                    else:
                        print("1 - Edit the username assigned to this task")
                        print("2 - Edit the due date")
                        edit_choice = input("Enter your choice: ")

                        # Edit username
                        if edit_choice == "1":
                            new_user = input("Enter the username: ")
                            if new_user in username_password:
                                chosen_task['username'] = new_user
                                print("Username updated successfully.")
                            else:
                                print("This username does not exist. Please register the user first.")

                        # Edit due date
                        elif edit_choice == "2":
                            try:
                                new_due_date = input("Enter the new due date (YYY-MM-DD): ")
                                chosen_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                print("Due date updated successfully.")
                            except ValueError:
                                print("Invalid date format. Please use YYYY-MM-DD.")

                            else:
                                print("Invalid choice. Returning to main menu.")

                elif action == "3":
                    print("Returning to main menu...\n")
                    return
                else:
                    print("Invalid choice. Please try again.")

                # === Save changes to file after any edit ===
                with open("tasks.txt", "w", encoding="utf-8") as task_file:
                    task_list_to_write = []
                    for task in task_list:
                        str_attrs = [
                            task['username'],
                            task['title'],
                            task['description'],
                            task['due_date'].strftime(DATETIME_STRING_FORMAT),
                            task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if task['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))
            
                print("Changes saved successfully.\n")
                return  # Exit after saving and returning to main menu
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(user_tasks)}, or -1 to return to main menu.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        
def generate_reports():
    """Generate reports for tasks and users."""
        
    # Generate two reports:
    # 1. task_overview.txt - contains details about each task
    # 2. user_overview.txt - contains details about each user

    # Task Overview Report
    total_tasks = len(task_list)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    for task in task_list:
        if task['completed']:
            completed_tasks += 1
        else:
            uncompleted_tasks += 1
            # Check if overdue
            if task['due_date'].date() < date.today():
                overdue_tasks += 1

    # Calculate percentages
    if total_tasks > 0:
        incomplete_percent = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        overdue_percent = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    else:
        incomplete_percent = 0
        overdue_percent = 0

    # Write to task_overview.txt
    with open("task_overview.txt", "w", encoding="utf-8") as task_report:
        task_report.write("=== Task Overview ===\n")
        task_report.write(f"Total tasks: {total_tasks}\n")
        task_report.write(f"Completed tasks: {completed_tasks}\n")
        task_report.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_report.write(f"Overdue tasks: {overdue_tasks}\n")
        task_report.write(f"Percentage incomplete: {incomplete_percent:.2f}%\n")
        task_report.write(f"Percentage overdue: {overdue_percent:.2f}%\n")

    # User Overview Report
    total_users = len(username_password)

    with open("user_overview.txt", "w", encoding="utf-8") as user_report:
        user_report.write("=== User Overview ===\n")
        user_report.write(f"Total users: {total_users}\n")
        user_report.write(f"Total tasks: {total_tasks}\n")

        # Loop through each user
        for username in username_password:
            # Get all tasks for this user
            user_tasks = [task for task in task_list if task ['username'] == username]
            user_total = len(user_tasks)

            if user_total > 0:
                user_completed = len([t for t in user_tasks if t['completed']])
                user_uncompleted = user_total - user_completed
                user_overdue = len([
                    t for t in user_tasks
                    if not t['completed'] and t['due_date'].date() < date.today()
                ])

                user_task_percent = (user_total / total_tasks) * 100 if total_tasks > 0 else 0
                user_complete_percent = (user_completed / user_total) * 100
                user_incomplete_percent = (user_uncompleted / user_total) * 100
                user_overdue_percent = (user_overdue / user_total) * 100
            else:
                # Handle case where user has no tasks
                user_task_percent = 0
                user_complete_percent = 0
                user_incomplete_percent = 0
                user_overdue_percent = 0

            # Write to file
            user_report.write(f"User: {username}\n")
            user_report.write(f"Total tasks: {user_total}\n")
            user_report.write(f"Percentage of all tasks: {user_task_percent:.2f}%\n")
            user_report.write(f"Completed: {user_complete_percent:.2f}%\n")
            user_report.write(f"Incomplete: {user_incomplete_percent:.2f}%\n")
            user_report.write(f"Overdue: {user_overdue_percent:.2f}%\n")

    print("Reports generated successfully!")

def display_statistics():
    """Displays the content of 'task_overview.txt' and 'user_overview.txt'
    If the reports do not exist, it will first generate them.
    """

    # Check if the report files exist
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("\nReport files not found. Generating them now...")
        generate_reports()
        print("\nReports have been generated successfully!\n")

    # Read and display the report files
    print("=== Task Overview ===")
    with open("task_overview.txt", "r", encoding="utf-8") as task_file:
        task_data = task_file.read()
        print(task_data)

    print("=== User Overview ===")
    with open("user_overview.txt", "r", encoding="utf-8") as user_file:
        user_data = user_file.read()
        print(user_data)

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [task for task in task_data if task != ""]

task_list = []
for task in task_data:
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = task.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = task_components[5] == "Yes"

    task_list.append(current_task)


#====Login Section====
# This code reads usernames and password from the user.txt file to
# allow a user to login.

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

while True:
    print("LOGIN")
    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in username_password:
        print("User does not exist")
        continue
    if username_password[current_user] != current_pass:
        print("Wrong password")
        continue
    print("Login Successful!")
    break

#====Main Menu Section====
while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input("Select one of the following Options below:\n"
                 "r - Registering a user\n"
                 "a - Adding a task\n"
                 "va - View all tasks\n"
                 "vm - View my task\n"
                 "gr - Generate reports\n"
                 "ds - Display statistics\n"
                 "e - Exit\n"
                 ": ").lower()

    # Add a new user to the user.txt file
    if menu == 'r':
        reg_user()

    # Allow a user to add a new task to task.txt file
    elif menu == 'a':
        add_task()

    # Reads the task from task.txt file and prints to the console in the
    elif menu == 'va':
        view_all()
        
    # Reads the task from task.txt file and prints to the console in the
    elif menu == 'vm':
        view_mine()

    # Generates two reports: tasks_overview.txt and users_overview.txt
    elif menu == 'gr':
        generate_reports()

    # If the user is an admin they can display statistics about number of users
    # and tasks.
    elif menu == 'ds':
        if current_user == 'admin':
            display_statistics()
        else:
            print("Only the admin can view statistics.")

    elif menu == 'e':
        print('Goodbye!!!')
        break

    else:
        print("You have made a wrong choice, Please Try again")

    # === Here ends the main program loop ===


# My brother helped me with this code,
# but mostly trial and error!
# I updated the doc strings, fixed the generate_reports() function, and fixed indentation issues.







import hashlib
import os
import uuid
import datetime

# Data file paths
USER_CREDENTIALS_FILE = "user_credentials.txt"
TASK_DATA_DIR = "task_data"  # Directory to store task files

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_unique_id():
    """Generates a unique ID using uuid.

    Returns:
        str: A unique identifier.
    """
    return str(uuid.uuid4())

def get_valid_date():
    """
    Prompts the user to enter a date and validates the input.

    Returns:
        datetime.date: The date entered by the user.  Returns None on error.
    """
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

def hash_password(password):
    """Hashes the password using SHA-256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    """Registers a new user by prompting for username and password,
    ensuring username uniqueness, and storing the hashed password.
    """
    while True:
        username = input("Enter username: ")
        if os.path.exists(os.path.join(TASK_DATA_DIR, f"{username}.txt")):
            print("Username already exists. Please choose a different one.")
            continue  # Go back to the beginning of the while loop
        if not username:
            print("Username cannot be empty. Please enter a valid username")
            continue
        password = input("Enter password: ")
        if not password:
            print("Password cannot be empty. Please enter a valid password")
            continue
        hashed_password = hash_password(password)
        try:
            with open(USER_CREDENTIALS_FILE, "a") as f:
                f.write(f"{username}:{hashed_password}\n")
            print("User registered successfully.")
            return username  # Return the username upon successful registration
        except Exception as e:
            print(f"Error registering user: {e}")
            return None # Return None on error

def login_user():
    """Logs in an existing user by prompting for username and password,
    validating the credentials, and returning the username upon success.
    """
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)
    try:
        with open(USER_CREDENTIALS_FILE, "r") as f:
            for line in f:
                stored_username, stored_hashed_password = line.strip().split(":")
                if username == stored_username and hashed_password == stored_hashed_password:
                    print("Logged in successfully.")
                    return username
        print("Invalid credentials. Please try again.")
        return None
    except FileNotFoundError:
        print("No users registered yet. Please register first.")
        return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def add_task(username):
    """Adds a new task for the given user.

    Args:
        username (str): The username of the logged-in user.
    """
    task_description = input("Enter task description: ")
    if not task_description:
        print("Task description cannot be empty. Task not added.")
        return

    task_id = generate_unique_id()
    date = get_valid_date()
    if date is None:
        print("Failed to add task: Invalid date.")
        return
    status = "Pending"
    task = {"task_id": task_id, "description": task_description, "status": status, "date": date.isoformat()}
    try:
        with open(os.path.join(TASK_DATA_DIR, f"{username}.txt"), "a") as f:
            f.write(f"{task_id}:{task_description}:{status}:{date.isoformat()}\n")
        print("Task added successfully.")
    except Exception as e:
        print(f"Error adding task: {e}")

def view_tasks(username):
    """Displays all tasks for the given user.

    Args:
        username (str): The username of the logged-in user.
    """
    try:
        with open(os.path.join(TASK_DATA_DIR, f"{username}.txt"), "r") as f:
            tasks = f.readlines()
        if not tasks:
            print("No tasks found.")
            return
        print("\n--- Your Tasks ---")
        for task in tasks:
            task_id, description, status, date_str = task.strip().split(":")
            try:
                display_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                print(f"Task ID: {task_id}, Description: {description}, Status: {status}, Date: {display_date}")
            except ValueError:
                print(f"Skipping task with invalid date: {task}")

    except FileNotFoundError:
        print("No tasks found.")
    except Exception as e:
        print(f"Error viewing tasks: {e}")

def update_task_status(username):
    """Updates the status of a task to "Completed" for the given user.

    Args:
        username (str): The username of the logged-in user.
    """
    task_id = input("Enter the ID of the task to mark as completed: ")
    updated_tasks = []
    task_found = False
    try:
        with open(os.path.join(TASK_DATA_DIR, f"{username}.txt"), "r") as f:
            tasks = f.readlines()
        for task in tasks:
            stored_task_id, description, status, date_str = task.strip().split(":")
            if stored_task_id == task_id:
                if status == "Completed":
                    print("Task already marked as completed.")
                    updated_tasks.append(task)  # Keep the original task data
                else:
                    status = "Completed"
                    updated_tasks.append(f"{stored_task_id}:{description}:{status}:{date_str}\n")
                    print("Task status updated successfully.")
                task_found = True
            else:
                updated_tasks.append(task)
        if not task_found:
            print("Task not found.")

        with open(os.path.join(TASK_DATA_DIR, f"{username}.txt"), "w") as f:
            f.writelines(updated_tasks)

    except FileNotFoundError:
        print("No tasks found.")
    except Exception as e:
        print(f"Error updating task status: {e}")

def delete_task(username):
    """Deletes a task for the given user.

    Args:
        username (str): The username of the logged-in user.
    """
    task_id = input("Enter the ID of the task to delete: ")
    updated_tasks = []
    task_found = False
    try:
        with open(os.path.join(TASK_DATA_DIR, f"{username}.txt"), "r") as f:
            tasks = f.readlines()
        for task in tasks:
            stored_task_id, description, status, date_str = task.strip().split(":")
            if stored_task_id == task_id:
                print("Task deleted successfully.")
                task_found = True
            else:
                updated_tasks.append(task)
        if not task_found:
            print("Task not found.")
        with open(os.path.join(TASK_DATA_DIR, f"{username}.txt"), "w") as f:
            f.writelines(updated_tasks)

    except FileNotFoundError:
        print("No tasks found.")
    except Exception as e:
        print(f"Error deleting task: {e}")

def display_menu(username):
    """Displays the main menu options to the user.

    Args:
        username (str): The username of the logged-in user.
    """
    print("\nTask Manager Menu:")
    print("a. Add a Task")
    print("b. View Tasks")
    print("c. Mark a Task as Completed")
    print("d. Delete a Task")
    print("e. Logout")
    print(f"Logged in as: {username}")

def main():
    """Main function to run the task manager application."""
    # Create the directory for task data if it doesn't exist
    if not os.path.exists(TASK_DATA_DIR):
        os.makedirs(TASK_DATA_DIR)

    clear_screen()
    print("Welcome to the Task Manager!")

    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = register_user()
            if username: #successful registration
                break  # Exit the registration/login loop
        elif choice == '2':
            username = login_user()
            if username: #successful login
                break  # Exit the registration/login loop
        elif choice == '3':
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please try again.")

    # Main task management loop
    while True:
        clear_screen()
        display_menu(username)
        choice = input("Enter your choice: ")

        if choice == 'a':
            add_task(username)
        elif choice == 'b':
            view_tasks(username)
        elif choice == 'c':
            update_task_status(username)
        elif choice == 'd':
            delete_task(username)
        elif choice == 'e':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()

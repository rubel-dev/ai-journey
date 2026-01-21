import json
import os
import sys
from datetime import datetime

# File name for storing tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """
    Load tasks from JSON file.
    Returns a list of tasks.
    """
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
                # Ensure we always return a list
                return tasks if isinstance(tasks, list) else []
        return []
    except json.JSONDecodeError:
        print("Error: Tasks file is corrupted. Starting with empty task list.")
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks):
    """
    Save tasks to JSON file.
    """
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False

def display_menu():
    """
    Display the main menu.
    """
    print("\n" + "="*40)
    print("CLI TO-DO APPLICATION")
    print("="*40)
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark task as complete/incomplete")
    print("4. Delete a task")
    print("5. View completed tasks")
    print("6. View pending tasks")
    print("7. Search tasks")
    print("8. Clear all tasks")
    print("9. Exit")
    print("="*40)

def get_user_choice():
    """
    Get and validate user's menu choice.
    """
    try:
        choice = input("\nEnter your choice (1-9): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 9:
            return int(choice)
        else:
            print("Invalid choice! Please enter a number between 1 and 9.")
            return None
    except Exception as e:
        print(f"Error reading input: {e}")
        return None

def add_task(tasks):
    """
    Add a new task to the list.
    """
    print("\n--- ADD NEW TASK ---")
    
    while True:
        task_description = input("Enter task description: ").strip()
        
        if not task_description:
            print("Task description cannot be empty. Please try again.")
            continue
        
        # Check if task already exists
        for task in tasks:
            if task['description'].lower() == task_description.lower():
                print("This task already exists!")
                return tasks
        
        break
    
    # Get optional due date
    due_date = input("Enter due date (DD/MM/YYYY) or press Enter for none: ").strip()
    
    if due_date:
        try:
            # Validate date format
            datetime.strptime(due_date, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format! Task added without due date.")
            due_date = ""
    
    # Get optional priority
    priority = input("Enter priority (1-High, 2-Medium, 3-Low) or press Enter for Medium: ").strip()
    
    priority_map = {"1": "High", "2": "Medium", "3": "Low"}
    if priority in priority_map:
        priority = priority_map[priority]
    else:
        priority = "Medium"
    
    # Create new task
    new_task = {
        'id': len(tasks) + 1,
        'description': task_description,
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'due_date': due_date if due_date else "No due date",
        'priority': priority
    }
    
    tasks.append(new_task)
    
    if save_tasks(tasks):
        print(f"Task '{task_description}' added successfully!")
    else:
        print("Task added but failed to save to file!")
    
    return tasks

def view_tasks(tasks, task_type="all"):
    """
    Display tasks based on type: all, completed, or pending.
    """
    if not tasks:
        print(f"\nNo {task_type} tasks found!")
        return
    
    filtered_tasks = []
    
    if task_type == "completed":
        filtered_tasks = [task for task in tasks if task['completed']]
        title = "COMPLETED TASKS"
    elif task_type == "pending":
        filtered_tasks = [task for task in tasks if not task['completed']]
        title = "PENDING TASKS"
    else:
        filtered_tasks = tasks
        title = "ALL TASKS"
    
    if not filtered_tasks:
        print(f"\nNo {task_type} tasks found!")
        return
    
    print(f"\n--- {title} ---")
    print(f"Total: {len(filtered_tasks)} task(s)")
    print("-" * 60)
    
    for task in filtered_tasks:
        status = "✓" if task['completed'] else "✗"
        priority_color = ""
        
        # Add color based on priority
        if task['priority'] == "High":
            priority_color = "\033[91m"  # Red
        elif task['priority'] == "Medium":
            priority_color = "\033[93m"  # Yellow
        else:
            priority_color = "\033[92m"  # Green
        
        print(f"ID: {task['id']}")
        print(f"Task: {task['description']}")
        print(f"Status: {status} | Priority: {priority_color}{task['priority']}\033[0m")
        print(f"Created: {task['created_at']} | Due: {task['due_date']}")
        print("-" * 40)

def mark_task_complete(tasks):
    """
    Mark a task as complete or incomplete.
    """
    if not tasks:
        print("\nNo tasks available!")
        return tasks
    
    view_tasks(tasks, "all")
    
    try:
        task_id = int(input("\nEnter the ID of the task to mark: ").strip())
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return tasks
    
    # Find the task
    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task_found = True
            old_status = "complete" if task['completed'] else "incomplete"
            task['completed'] = not task['completed']
            new_status = "complete" if task['completed'] else "incomplete"
            
            if save_tasks(tasks):
                print(f"Task ID {task_id} marked as {new_status}!")
            else:
                print("Task updated but failed to save to file!")
                task['completed'] = not task['completed']  # Revert change
            break
    
    if not task_found:
        print(f"Task with ID {task_id} not found!")
    
    return tasks

def delete_task(tasks):
    """
    Delete a task from the list.
    """
    if not tasks:
        print("\nNo tasks available!")
        return tasks
    
    view_tasks(tasks, "all")
    
    try:
        task_id = int(input("\nEnter the ID of the task to delete: ").strip())
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return tasks
    
    # Find and delete the task
    new_tasks = []
    task_deleted = False
    deleted_description = ""
    
    for task in tasks:
        if task['id'] == task_id:
            task_deleted = True
            deleted_description = task['description']
            continue  # Skip this task (delete it)
        new_tasks.append(task)
    
    if task_deleted:
        # Reassign IDs to maintain sequence
        for i, task in enumerate(new_tasks, 1):
            task['id'] = i
        
        if save_tasks(new_tasks):
            print(f"Task '{deleted_description}' deleted successfully!")
            return new_tasks
        else:
            print("Failed to save changes to file!")
            return tasks
    else:
        print(f"Task with ID {task_id} not found!")
        return tasks

def search_tasks(tasks):
    """
    Search tasks by keyword.
    """
    if not tasks:
        print("\nNo tasks available!")
        return
    
    keyword = input("\nEnter keyword to search: ").strip().lower()
    
    if not keyword:
        print("Keyword cannot be empty!")
        return
    
    results = []
    for task in tasks:
        if keyword in task['description'].lower():
            results.append(task)
    
    if results:
        print(f"\nFound {len(results)} task(s) containing '{keyword}':")
        print("-" * 60)
        for task in results:
            status = "✓" if task['completed'] else "✗"
            print(f"ID: {task['id']} | {task['description']} | Status: {status}")
    else:
        print(f"No tasks found containing '{keyword}'.")

def clear_all_tasks():
    """
    Clear all tasks after confirmation.
    """
    confirmation = input("\nAre you sure you want to delete ALL tasks? (yes/no): ").strip().lower()
    
    if confirmation == "yes":
        empty_list = []
        if save_tasks(empty_list):
            print("All tasks have been deleted!")
            return empty_list
        else:
            print("Failed to save changes!")
            return load_tasks()
    else:
        print("Operation cancelled.")
        return load_tasks()

def show_statistics(tasks):
    """
    Show task statistics.
    """
    if not tasks:
        print("\nNo tasks available!")
        return
    
    total = len(tasks)
    completed = sum(1 for task in tasks if task['completed'])
    pending = total - completed
    
    print("\n--- TASK STATISTICS ---")
    print(f"Total tasks: {total}")
    print(f"Completed: {completed} ({completed/total*100:.1f}%)")
    print(f"Pending: {pending} ({pending/total*100:.1f}%)")
    
    # Count by priority
    high_priority = sum(1 for task in tasks if task['priority'] == "High")
    medium_priority = sum(1 for task in tasks if task['priority'] == "Medium")
    low_priority = sum(1 for task in tasks if task['priority'] == "Low")
    
    print(f"\nBy Priority:")
    print(f"High: {high_priority} | Medium: {medium_priority} | Low: {low_priority}")

def main():
    """
    Main function to run the Todo App.
    """
    print("\n" + "="*50)
    print("WELCOME TO CLI TO-DO APPLICATION")
    print("="*50)
    
    # Load existing tasks
    tasks = load_tasks()
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice is None:
            continue
        
        if choice == 1:
            tasks = add_task(tasks)
        
        elif choice == 2:
            view_tasks(tasks, "all")
            if tasks:
                show_statistics(tasks)
        
        elif choice == 3:
            tasks = mark_task_complete(tasks)
        
        elif choice == 4:
            tasks = delete_task(tasks)
        
        elif choice == 5:
            view_tasks(tasks, "completed")
        
        elif choice == 6:
            view_tasks(tasks, "pending")
        
        elif choice == 7:
            search_tasks(tasks)
        
        elif choice == 8:
            tasks = clear_all_tasks()
        
        elif choice == 9:
            print("\nSaving your tasks...")
            save_tasks(tasks)
            print("Thank you for using CLI To-Do App. Goodbye!")
            print("="*50)
            break
        
        # Small pause for better UX
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Saving tasks...")
        # Load and save tasks one last time
        tasks = load_tasks()
        save_tasks(tasks)
        print("Tasks saved. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try running the program again.")
        sys.exit(1)
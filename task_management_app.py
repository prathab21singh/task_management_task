from task_manager import TaskManager

def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Management Application")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Search tasks by description")
        print("8. Exit")

        try:
            choice = input("Enter your choice: ")

            if choice == "1":
                desc = input("Enter task description: ").strip()
                deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ").strip() or None
                status = input("Enter status (pending/completed): ").strip().lower() or "pending"
                task_manager.add_task(desc, deadline, status)
            elif choice == "2":
                tasks = task_manager.view_tasks()
                print("All Tasks:")
                print()
                for task in tasks:
                    print(task)
            elif choice == "3":
                tasks = task_manager.view_tasks_by_status("pending")
                print("Fetching pending status")
                for task in tasks:
                    print(task)
            elif choice == "4":
                tasks = task_manager.view_tasks_by_status("completed")
                print("Fetching completed status")
                for task in tasks:
                    print(task)
            elif choice == "5":
                task_id = int(input("Enter task ID to update: ").strip())
                new_desc = input("Enter new description : ").strip() or None
                new_status = input("Enter new status (pending/completed): ").strip().lower() or None
                task_manager.update_task(task_id, new_desc, new_status)
            elif choice == "6":
                task_id = int(input("Enter task ID to delete: ").strip())
                task_manager.delete_task(task_id)
            elif choice == "7":
                keyword = input("Enter keyword to search for: ").strip()
                tasks = task_manager.search_tasks_by_description(keyword)
                if tasks:
                    print(f"\nTasks containing '{keyword}':")
                    for task in tasks:
                        print(task)
            elif choice == "8":
                print("Exiting application. bye!")
                break
            else:
                print("Invalid choice! Please enter a valid choice.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

import argparse
import sys
from datetime import datetime
from src.task import Task, SubTask, Priority
from src.storage import save_tasks, load_tasks
from src.scheduler import start_scheduler
from src.validation import validate_email, validate_datetime, validate_task_name, validate_description
from src.logger import get_logger

logger = get_logger()

def create_task(name, description, deadline_str, priority_str='MEDIUM', tags=None):
    # Validate inputs
    if not validate_task_name(name):
        logger.error(f"Invalid task name: {name}")
        print("Error: Invalid task name. Name must be non-empty and less than 200 characters.")
        sys.exit(1)
    
    if not validate_description(description):
        logger.error(f"Invalid description for task: {name}")
        print("Error: Invalid description. Description must be less than 1000 characters.")
        sys.exit(1)
    
    is_valid, deadline = validate_datetime(deadline_str)
    if not is_valid:
        logger.error(f"Invalid deadline format: {deadline_str}")
        print("Error: Invalid deadline format. Use ISO format (e.g., 2023-12-31T23:59:59).")
        sys.exit(1)
    
    # Check for duplicate task names
    tasks = load_tasks()
    if any(task.name == name for task in tasks):
        logger.warning(f"Attempted to create duplicate task: {name}")
        print(f"Error: Task with name '{name}' already exists.")
        sys.exit(1)
    
    # Parse priority
    try:
        priority = Priority.from_string(priority_str)
    except ValueError as e:
        logger.error(f"Invalid priority: {priority_str}")
        print(f"Error: {e}")
        sys.exit(1)
    
    # Parse tags
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    task = Task(name, description, deadline, priority=priority, tags=tag_list)
    tasks.append(task)
    save_tasks(tasks)
    logger.info(f"Task created: {name} (deadline: {deadline}, priority: {priority.name}, tags: {tag_list})")
    print(f"Task '{name}' created.")

def add_sub_task(task_name, sub_name, sub_desc, sub_deadline_str):
    # Validate inputs
    if not validate_task_name(sub_name):
        print("Error: Invalid sub-task name. Name must be non-empty and less than 200 characters.")
        sys.exit(1)
    
    if not validate_description(sub_desc):
        print("Error: Invalid description. Description must be less than 1000 characters.")
        sys.exit(1)
    
    is_valid, sub_deadline = validate_datetime(sub_deadline_str)
    if not is_valid:
        print("Error: Invalid deadline format. Use ISO format (e.g., 2023-12-31T23:59:59).")
        sys.exit(1)
    
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            # Check for duplicate sub-task names
            if any(st.name == sub_name for st in task.sub_tasks):
                print(f"Error: Sub-task with name '{sub_name}' already exists in task '{task_name}'.")
                sys.exit(1)
            
            sub = SubTask(sub_name, sub_desc, sub_deadline)
            task.add_sub_task(sub)
            save_tasks(tasks)
            print(f"Sub-task '{sub_name}' added to '{task_name}'.")
            return
    print("Error: Task not found.")
    sys.exit(1)

def add_subscriber(task_name, email):
    # Validate email
    if not validate_email(email):
        print("Error: Invalid email address format.")
        sys.exit(1)
    
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            # Check for duplicate subscribers
            if email in task.subscribers:
                print(f"Error: '{email}' is already subscribed to task '{task_name}'.")
                sys.exit(1)
            
            task.add_subscriber(email)
            save_tasks(tasks)
            print(f"Subscriber '{email}' added to '{task_name}'.")
            return
    print("Error: Task not found.")
    sys.exit(1)

def list_tasks():
    tasks = load_tasks()
    for task in tasks:
        tags_str = f", Tags: {', '.join(task.tags)}" if task.tags else ""
        print(f"\nTask: {task.name}")
        print(f"  Priority: {task.priority.name}")
        print(f"  Deadline: {task.deadline}")
        print(f"  Completed: {task.completed}")
        if task.tags:
            print(f"  Tags: {', '.join(task.tags)}")
        
        if task.sub_tasks:
            print(f"  Sub-tasks:")
            for st in task.sub_tasks:
                print(f"    - {st.name}")
                print(f"      Deadline: {st.deadline}")
                print(f"      Completed: {st.completed}")

def complete_task(task_name):
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            task.mark_complete()
            save_tasks(tasks)
            logger.info(f"Task completed: {task_name}")
            print(f"Task '{task_name}' marked as completed.")
            return
    logger.warning(f"Attempted to complete non-existent task: {task_name}")
    print("Task not found.")

def complete_sub_task(task_name, sub_task_name):
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            if task.complete_sub_task(sub_task_name):
                save_tasks(tasks)
                print(f"Sub-task '{sub_task_name}' in task '{task_name}' marked as completed.")
                return
            else:
                print(f"Sub-task '{sub_task_name}' not found in task '{task_name}'.")
                return
    print("Task not found.")

def delete_task(task_name):
    tasks = load_tasks()
    initial_count = len(tasks)
    tasks = [task for task in tasks if task.name != task_name]
    if len(tasks) < initial_count:
        save_tasks(tasks)
        logger.info(f"Task deleted: {task_name}")
        print(f"Task '{task_name}' deleted.")
    else:
        logger.warning(f"Attempted to delete non-existent task: {task_name}")
        print("Task not found.")

def delete_sub_task(task_name, sub_task_name):
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            initial_count = len(task.sub_tasks)
            task.sub_tasks = [st for st in task.sub_tasks if st.name != sub_task_name]
            if len(task.sub_tasks) < initial_count:
                save_tasks(tasks)
                print(f"Sub-task '{sub_task_name}' deleted from task '{task_name}'.")
                return
            else:
                print(f"Sub-task '{sub_task_name}' not found in task '{task_name}'.")
                return
    print("Task not found.")

def update_task(task_name, new_name=None, new_description=None, new_deadline=None):
    # Validate inputs
    if new_name and not validate_task_name(new_name):
        print("Error: Invalid task name. Name must be non-empty and less than 200 characters.")
        sys.exit(1)
    
    if new_description and not validate_description(new_description):
        print("Error: Invalid description. Description must be less than 1000 characters.")
        sys.exit(1)
    
    if new_deadline:
        is_valid, parsed_deadline = validate_datetime(new_deadline)
        if not is_valid:
            print("Error: Invalid deadline format. Use ISO format (e.g., 2023-12-31T23:59:59).")
            sys.exit(1)
    
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            # Check for duplicate name if renaming
            if new_name and new_name != task_name:
                if any(t.name == new_name for t in tasks):
                    print(f"Error: Task with name '{new_name}' already exists.")
                    sys.exit(1)
            
            if new_name:
                task.name = new_name
            if new_description:
                task.description = new_description
            if new_deadline:
                task.deadline = parsed_deadline
            save_tasks(tasks)
            print(f"Task '{task_name}' updated.")
            return
    print("Error: Task not found.")
    sys.exit(1)

def update_sub_task(task_name, sub_task_name, new_name=None, new_description=None, new_deadline=None):
    # Validate inputs
    if new_name and not validate_task_name(new_name):
        print("Error: Invalid sub-task name. Name must be non-empty and less than 200 characters.")
        sys.exit(1)
    
    if new_description and not validate_description(new_description):
        print("Error: Invalid description. Description must be less than 1000 characters.")
        sys.exit(1)
    
    if new_deadline:
        is_valid, parsed_deadline = validate_datetime(new_deadline)
        if not is_valid:
            print("Error: Invalid deadline format. Use ISO format (e.g., 2023-12-31T23:59:59).")
            sys.exit(1)
    
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            for st in task.sub_tasks:
                if st.name == sub_task_name:
                    # Check for duplicate name if renaming
                    if new_name and new_name != sub_task_name:
                        if any(s.name == new_name for s in task.sub_tasks):
                            print(f"Error: Sub-task with name '{new_name}' already exists in task '{task_name}'.")
                            sys.exit(1)
                    
                    if new_name:
                        st.name = new_name
                    if new_description:
                        st.description = new_description
                    if new_deadline:
                        st.deadline = parsed_deadline
                    save_tasks(tasks)
                    print(f"Sub-task '{sub_task_name}' in task '{task_name}' updated.")
                    return
            print(f"Error: Sub-task '{sub_task_name}' not found in task '{task_name}'.")
            sys.exit(1)
    print("Error: Task not found.")
    sys.exit(1)

def add_tag(task_name, tag):
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            task.add_tag(tag)
            save_tasks(tasks)
            logger.info(f"Tag '{tag}' added to task '{task_name}'")
            print(f"Tag '{tag}' added to task '{task_name}'.")
            return
    print("Error: Task not found.")
    sys.exit(1)

def remove_tag(task_name, tag):
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            if task.remove_tag(tag):
                save_tasks(tasks)
                logger.info(f"Tag '{tag}' removed from task '{task_name}'")
                print(f"Tag '{tag}' removed from task '{task_name}'.")
            else:
                print(f"Tag '{tag}' not found in task '{task_name}'.")
            return
    print("Error: Task not found.")
    sys.exit(1)

def set_priority(task_name, priority_str):
    try:
        priority = Priority.from_string(priority_str)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name:
            task.set_priority(priority)
            save_tasks(tasks)
            logger.info(f"Priority of task '{task_name}' set to {priority.name}")
            print(f"Priority of task '{task_name}' set to {priority.name}.")
            return
    print("Error: Task not found.")
    sys.exit(1)

def search_tasks(query=None, tag=None, priority=None, completed=None):
    """Search and filter tasks based on criteria."""
    tasks = load_tasks()
    filtered_tasks = tasks
    
    # Filter by query (name or description)
    if query:
        filtered_tasks = [t for t in filtered_tasks
                         if query.lower() in t.name.lower() or query.lower() in t.description.lower()]
    
    # Filter by tag
    if tag:
        filtered_tasks = [t for t in filtered_tasks if t.has_tag(tag)]
    
    # Filter by priority
    if priority:
        try:
            priority_enum = Priority.from_string(priority)
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority_enum]
        except ValueError:
            print(f"Error: Invalid priority '{priority}'")
            sys.exit(1)
    
    # Filter by completion status
    if completed is not None:
        filtered_tasks = [t for t in filtered_tasks if t.completed == completed]
    
    if not filtered_tasks:
        print("No tasks found matching the criteria.")
        return
    
    print(f"Found {len(filtered_tasks)} task(s):")
    for task in filtered_tasks:
        tags_str = f", Tags: {', '.join(task.tags)}" if task.tags else ""
        print(f"Task: {task.name}, Priority: {task.priority.name}, Deadline: {task.deadline}, Completed: {task.completed}{tags_str}")
        for st in task.sub_tasks:
            print(f"  Sub: {st.name}, Deadline: {st.deadline}, Completed: {st.completed}")

def main():
    parser = argparse.ArgumentParser(description="DeadlineHQ - Your Command Center for Staying on Track")
    subparsers = parser.add_subparsers(dest='command')

    # Create task
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument('name', help='Task name')
    create_parser.add_argument('description', help='Task description')
    create_parser.add_argument('deadline', help='Deadline in ISO format (e.g., 2023-12-31T23:59:59)')
    create_parser.add_argument('--priority', dest='priority', default='MEDIUM',
                              help='Priority: LOW, MEDIUM, HIGH, or URGENT (default: MEDIUM)')
    create_parser.add_argument('--tags', dest='tags', help='Comma-separated tags')

    # Add sub-task
    sub_parser = subparsers.add_parser('add_sub')
    sub_parser.add_argument('task_name')
    sub_parser.add_argument('sub_name')
    sub_parser.add_argument('sub_desc')
    sub_parser.add_argument('sub_deadline')

    # Add subscriber
    sub_parser = subparsers.add_parser('add_subscriber')
    sub_parser.add_argument('task_name')
    sub_parser.add_argument('email')

    # List tasks
    list_parser = subparsers.add_parser('list')
    
    # Complete task
    complete_parser = subparsers.add_parser('complete')
    complete_parser.add_argument('task_name')
    
    # Complete sub-task
    complete_sub_parser = subparsers.add_parser('complete_sub')
    complete_sub_parser.add_argument('task_name')
    complete_sub_parser.add_argument('sub_task_name')
    
    # Delete task
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('task_name')
    
    # Delete sub-task
    delete_sub_parser = subparsers.add_parser('delete_sub')
    delete_sub_parser.add_argument('task_name')
    delete_sub_parser.add_argument('sub_task_name')
    
    # Update task
    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('task_name')
    update_parser.add_argument('--name', dest='new_name', help='New task name')
    update_parser.add_argument('--description', dest='new_description', help='New description')
    update_parser.add_argument('--deadline', dest='new_deadline', help='New deadline (ISO format)')
    
    # Update sub-task
    update_sub_parser = subparsers.add_parser('update_sub')
    update_sub_parser.add_argument('task_name')
    update_sub_parser.add_argument('sub_task_name')
    update_sub_parser.add_argument('--name', dest='new_name', help='New sub-task name')
    update_sub_parser.add_argument('--description', dest='new_description', help='New description')
    update_sub_parser.add_argument('--deadline', dest='new_deadline', help='New deadline (ISO format)')
    
    # Add tag
    add_tag_parser = subparsers.add_parser('add_tag', help='Add a tag to a task')
    add_tag_parser.add_argument('task_name')
    add_tag_parser.add_argument('tag')
    
    # Remove tag
    remove_tag_parser = subparsers.add_parser('remove_tag', help='Remove a tag from a task')
    remove_tag_parser.add_argument('task_name')
    remove_tag_parser.add_argument('tag')
    
    # Set priority
    set_priority_parser = subparsers.add_parser('set_priority', help='Set task priority')
    set_priority_parser.add_argument('task_name')
    set_priority_parser.add_argument('priority', help='Priority: LOW, MEDIUM, HIGH, or URGENT')
    
    # Search tasks
    search_parser = subparsers.add_parser('search', help='Search and filter tasks')
    search_parser.add_argument('--query', help='Search in task name or description')
    search_parser.add_argument('--tag', help='Filter by tag')
    search_parser.add_argument('--priority', help='Filter by priority (LOW, MEDIUM, HIGH, URGENT)')
    search_parser.add_argument('--completed', type=lambda x: x.lower() == 'true',
                              help='Filter by completion status (true/false)')

    # Start scheduler
    start_parser = subparsers.add_parser('start')

    args = parser.parse_args()

    if args.command == 'create':
        create_task(args.name, args.description, args.deadline, args.priority, args.tags)
    elif args.command == 'add_sub':
        add_sub_task(args.task_name, args.sub_name, args.sub_desc, args.sub_deadline)
    elif args.command == 'add_subscriber':
        add_subscriber(args.task_name, args.email)
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'complete':
        complete_task(args.task_name)
    elif args.command == 'complete_sub':
        complete_sub_task(args.task_name, args.sub_task_name)
    elif args.command == 'delete':
        delete_task(args.task_name)
    elif args.command == 'delete_sub':
        delete_sub_task(args.task_name, args.sub_task_name)
    elif args.command == 'update':
        update_task(args.task_name, args.new_name, args.new_description, args.new_deadline)
    elif args.command == 'update_sub':
        update_sub_task(args.task_name, args.sub_task_name, args.new_name, args.new_description, args.new_deadline)
    elif args.command == 'add_tag':
        add_tag(args.task_name, args.tag)
    elif args.command == 'remove_tag':
        remove_tag(args.task_name, args.tag)
    elif args.command == 'set_priority':
        set_priority(args.task_name, args.priority)
    elif args.command == 'search':
        search_tasks(args.query, args.tag, args.priority, args.completed)
    elif args.command == 'start':
        start_scheduler()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
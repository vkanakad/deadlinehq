import json
import os
import shutil
from datetime import datetime
from typing import List
from .task import Task, SubTask, Priority
from .config import get_config

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Priority):
            return obj.name
        return super().default(obj)

def datetime_decoder(dct):
    for key, value in dct.items():
        if key.endswith('_time') or key == 'deadline':
            try:
                dct[key] = datetime.fromisoformat(value)
            except (ValueError, TypeError):
                pass
    return dct

def save_tasks(tasks: List[Task], filename: str = None):
    """Save tasks to JSON file with optional backup.
    
    Args:
        tasks: List of tasks to save
        filename: Optional filename override (uses config default if not provided)
    """
    config = get_config()
    
    if filename is None:
        filename = config.get('storage', 'tasks_file', default='tasks.json')
    
    # Create backup if enabled
    if config.get('storage', 'backup_enabled', default=False) and os.path.exists(filename):
        backup_dir = config.get('storage', 'backup_directory', default='backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'tasks_backup_{timestamp}.json')
        shutil.copy2(filename, backup_file)
    
    data = []
    for task in tasks:
        task_data = {
            'name': task.name,
            'description': task.description,
            'deadline': task.deadline,
            'completed': task.completed,
            'priority': task.priority,
            'tags': task.tags,
            'subscribers': task.subscribers,
            'sub_tasks': [
                {
                    'name': st.name,
                    'description': st.description,
                    'deadline': st.deadline,
                    'completed': st.completed
                } for st in task.sub_tasks
            ]
        }
        data.append(task_data)
    
    with open(filename, 'w') as f:
        json.dump(data, f, cls=DateTimeEncoder, indent=4)

def load_tasks(filename: str = None) -> List[Task]:
    """Load tasks from JSON file.
    
    Args:
        filename: Optional filename override (uses config default if not provided)
        
    Returns:
        List of loaded tasks, or empty list if file doesn't exist
    """
    config = get_config()
    
    if filename is None:
        filename = config.get('storage', 'tasks_file', default='tasks.json')
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f, object_hook=datetime_decoder)
        tasks = []
        for task_data in data:
            # Handle priority
            priority_str = task_data.get('priority', 'MEDIUM')
            if isinstance(priority_str, str):
                try:
                    priority = Priority[priority_str]
                except KeyError:
                    priority = Priority.MEDIUM
            else:
                priority = Priority.MEDIUM
            
            # Handle tags
            tags = task_data.get('tags', [])
            
            task = Task(
                task_data['name'],
                task_data['description'],
                task_data['deadline'],
                priority=priority,
                tags=tags
            )
            task.completed = task_data.get('completed', False)
            task.subscribers = task_data.get('subscribers', [])
            for st_data in task_data.get('sub_tasks', []):
                st = SubTask(st_data['name'], st_data['description'], st_data['deadline'])
                st.completed = st_data.get('completed', False)
                task.add_sub_task(st)
            tasks.append(task)
        return tasks
    except FileNotFoundError:
        return []
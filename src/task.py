from datetime import datetime
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    
    @classmethod
    def from_string(cls, value: str) -> 'Priority':
        """Convert string to Priority enum.
        
        Args:
            value: Priority as string (case-insensitive)
            
        Returns:
            Priority enum value
            
        Raises:
            ValueError: If value is not a valid priority
        """
        value_upper = value.upper()
        try:
            return cls[value_upper]
        except KeyError:
            raise ValueError(f"Invalid priority: {value}. Must be one of: LOW, MEDIUM, HIGH, URGENT")

class SubTask:
    def __init__(self, name: str, description: str, deadline: datetime):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.completed = False
    
    def mark_complete(self):
        """Mark this sub-task as completed."""
        self.completed = True
    
    def mark_incomplete(self):
        """Mark this sub-task as incomplete."""
        self.completed = False

class Task:
    def __init__(self, name: str, description: str, deadline: datetime,
                 priority: Priority = Priority.MEDIUM, tags: List[str] = None):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.tags: List[str] = tags if tags is not None else []
        self.sub_tasks: List[SubTask] = []
        self.subscribers: List[str] = []  # email addresses
        self.completed = False

    def add_sub_task(self, sub_task: SubTask):
        self.sub_tasks.append(sub_task)

    def add_subscriber(self, email: str):
        self.subscribers.append(email)
    
    def add_tag(self, tag: str):
        """Add a tag to the task.
        
        Args:
            tag: Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the task.
        
        Args:
            tag: Tag to remove
            
        Returns:
            True if tag was removed, False if tag didn't exist
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False
    
    def has_tag(self, tag: str) -> bool:
        """Check if task has a specific tag.
        
        Args:
            tag: Tag to check
            
        Returns:
            True if task has the tag, False otherwise
        """
        return tag in self.tags
    
    def set_priority(self, priority: Priority):
        """Set task priority.
        
        Args:
            priority: Priority level
        """
        self.priority = priority
    
    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True
    
    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.completed = False
    
    def complete_sub_task(self, sub_task_name: str) -> bool:
        """Mark a specific sub-task as completed by name.
        
        Args:
            sub_task_name: Name of the sub-task to complete
            
        Returns:
            True if sub-task was found and marked complete, False otherwise
        """
        for sub_task in self.sub_tasks:
            if sub_task.name == sub_task_name:
                sub_task.mark_complete()
                return True
        return False
    
    def is_fully_completed(self) -> bool:
        """Check if task and all sub-tasks are completed.
        
        Returns:
            True if task and all sub-tasks are completed, False otherwise
        """
        if not self.completed:
            return False
        return all(st.completed for st in self.sub_tasks)
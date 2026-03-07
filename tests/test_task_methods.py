import pytest
from datetime import datetime
from src.task import Task, SubTask


class TestSubTask:
    def test_subtask_creation(self):
        """Test creating a sub-task."""
        deadline = datetime(2024, 12, 31)
        sub = SubTask("Sub Task", "Description", deadline)
        
        assert sub.name == "Sub Task"
        assert sub.description == "Description"
        assert sub.deadline == deadline
        assert sub.completed is False
    
    def test_mark_complete(self):
        """Test marking sub-task as complete."""
        sub = SubTask("Sub", "Desc", datetime.now())
        assert sub.completed is False
        
        sub.mark_complete()
        assert sub.completed is True
    
    def test_mark_incomplete(self):
        """Test marking sub-task as incomplete."""
        sub = SubTask("Sub", "Desc", datetime.now())
        sub.mark_complete()
        assert sub.completed is True
        
        sub.mark_incomplete()
        assert sub.completed is False


class TestTask:
    def test_task_creation(self):
        """Test creating a task."""
        deadline = datetime(2024, 12, 31)
        task = Task("Test Task", "Description", deadline)
        
        assert task.name == "Test Task"
        assert task.description == "Description"
        assert task.deadline == deadline
        assert task.completed is False
        assert task.sub_tasks == []
        assert task.subscribers == []
    
    def test_add_sub_task(self):
        """Test adding sub-tasks."""
        task = Task("Main", "Desc", datetime.now())
        sub1 = SubTask("Sub 1", "Desc 1", datetime.now())
        sub2 = SubTask("Sub 2", "Desc 2", datetime.now())
        
        task.add_sub_task(sub1)
        assert len(task.sub_tasks) == 1
        
        task.add_sub_task(sub2)
        assert len(task.sub_tasks) == 2
        assert task.sub_tasks[0].name == "Sub 1"
        assert task.sub_tasks[1].name == "Sub 2"
    
    def test_add_subscriber(self):
        """Test adding subscribers."""
        task = Task("Task", "Desc", datetime.now())
        
        task.add_subscriber("user1@example.com")
        assert len(task.subscribers) == 1
        
        task.add_subscriber("user2@example.com")
        assert len(task.subscribers) == 2
        assert "user1@example.com" in task.subscribers
        assert "user2@example.com" in task.subscribers
    
    def test_mark_complete(self):
        """Test marking task as complete."""
        task = Task("Task", "Desc", datetime.now())
        assert task.completed is False
        
        task.mark_complete()
        assert task.completed is True
    
    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task("Task", "Desc", datetime.now())
        task.mark_complete()
        
        task.mark_incomplete()
        assert task.completed is False
    
    def test_complete_sub_task(self):
        """Test completing a sub-task by name."""
        task = Task("Main", "Desc", datetime.now())
        sub1 = SubTask("Sub 1", "Desc 1", datetime.now())
        sub2 = SubTask("Sub 2", "Desc 2", datetime.now())
        task.add_sub_task(sub1)
        task.add_sub_task(sub2)
        
        result = task.complete_sub_task("Sub 1")
        assert result is True
        assert task.sub_tasks[0].completed is True
        assert task.sub_tasks[1].completed is False
    
    def test_complete_nonexistent_sub_task(self):
        """Test completing a non-existent sub-task."""
        task = Task("Main", "Desc", datetime.now())
        
        result = task.complete_sub_task("Nonexistent")
        assert result is False
    
    def test_is_fully_completed(self):
        """Test checking if task and all sub-tasks are completed."""
        task = Task("Main", "Desc", datetime.now())
        sub1 = SubTask("Sub 1", "Desc 1", datetime.now())
        sub2 = SubTask("Sub 2", "Desc 2", datetime.now())
        task.add_sub_task(sub1)
        task.add_sub_task(sub2)
        
        # Task not completed
        assert task.is_fully_completed() is False
        
        # Task completed but sub-tasks not
        task.mark_complete()
        assert task.is_fully_completed() is False
        
        # One sub-task completed
        sub1.mark_complete()
        assert task.is_fully_completed() is False
        
        # All completed
        sub2.mark_complete()
        assert task.is_fully_completed() is True
    
    def test_is_fully_completed_no_subtasks(self):
        """Test is_fully_completed with no sub-tasks."""
        task = Task("Task", "Desc", datetime.now())
        
        assert task.is_fully_completed() is False
        
        task.mark_complete()
        assert task.is_fully_completed() is True

import pytest
from datetime import datetime
from src.task import Task, SubTask

def test_task_creation():
    deadline = datetime(2023, 12, 31)
    task = Task("Test Task", "Description", deadline)
    assert task.name == "Test Task"
    assert task.deadline == deadline
    assert not task.completed

def test_add_sub_task():
    task = Task("Main", "Desc", datetime.now())
    sub = SubTask("Sub", "Sub desc", datetime.now())
    task.add_sub_task(sub)
    assert len(task.sub_tasks) == 1
    assert task.sub_tasks[0].name == "Sub"
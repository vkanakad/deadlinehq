import pytest
import os
import json
from datetime import datetime
from src.task import Task, SubTask
from src.storage import save_tasks, load_tasks


@pytest.fixture
def temp_tasks_file(tmp_path):
    """Create a temporary tasks file."""
    return str(tmp_path / "test_tasks.json")


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    task1 = Task("Task 1", "Description 1", datetime(2024, 12, 31, 23, 59, 59))
    task1.add_subscriber("test@example.com")
    
    sub1 = SubTask("Sub 1", "Sub desc", datetime(2024, 12, 30, 23, 59, 59))
    task1.add_sub_task(sub1)
    
    task2 = Task("Task 2", "Description 2", datetime(2025, 1, 15, 12, 0, 0))
    task2.completed = True
    
    return [task1, task2]


def test_save_and_load_tasks(temp_tasks_file, sample_tasks):
    """Test saving and loading tasks."""
    save_tasks(sample_tasks, temp_tasks_file)
    
    assert os.path.exists(temp_tasks_file)
    
    loaded_tasks = load_tasks(temp_tasks_file)
    
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].name == "Task 1"
    assert loaded_tasks[0].description == "Description 1"
    assert loaded_tasks[0].deadline == datetime(2024, 12, 31, 23, 59, 59)
    assert len(loaded_tasks[0].sub_tasks) == 1
    assert loaded_tasks[0].sub_tasks[0].name == "Sub 1"
    assert "test@example.com" in loaded_tasks[0].subscribers
    
    assert loaded_tasks[1].name == "Task 2"
    assert loaded_tasks[1].completed is True


def test_load_nonexistent_file():
    """Test loading from a non-existent file."""
    tasks = load_tasks("nonexistent_file.json")
    assert tasks == []


def test_save_empty_tasks(temp_tasks_file):
    """Test saving an empty task list."""
    save_tasks([], temp_tasks_file)
    
    loaded_tasks = load_tasks(temp_tasks_file)
    assert loaded_tasks == []


def test_task_data_integrity(temp_tasks_file, sample_tasks):
    """Test that all task data is preserved through save/load cycle."""
    save_tasks(sample_tasks, temp_tasks_file)
    loaded_tasks = load_tasks(temp_tasks_file)
    
    # Check first task
    assert loaded_tasks[0].name == sample_tasks[0].name
    assert loaded_tasks[0].description == sample_tasks[0].description
    assert loaded_tasks[0].deadline == sample_tasks[0].deadline
    assert loaded_tasks[0].completed == sample_tasks[0].completed
    assert loaded_tasks[0].subscribers == sample_tasks[0].subscribers
    
    # Check sub-task
    assert len(loaded_tasks[0].sub_tasks) == len(sample_tasks[0].sub_tasks)
    assert loaded_tasks[0].sub_tasks[0].name == sample_tasks[0].sub_tasks[0].name
    assert loaded_tasks[0].sub_tasks[0].completed == sample_tasks[0].sub_tasks[0].completed

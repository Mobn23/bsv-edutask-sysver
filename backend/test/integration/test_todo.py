import pytest
from pymongo.errors import WriteError
from bson import ObjectId

from src.util.dao import DAO

@pytest.fixture
def DAO_todo():
    dao_todo = DAO("todo")

    yield dao_todo

    dao_todo.collection.delete_many({
        "description": {"$regex": "Test description$"}
    })

@pytest.fixture
def DAO_task():
    dao_task = DAO("task")

    yield dao_task

    dao_task.collection.delete_many({
        "title": {"$regex": "Test title$"}
    })


@pytest.mark.parametrize('description, expected_exception', [
    ("Test description", None),
    (123, WriteError),
    (None, WriteError)
])
def test_create_todo_with_varied_description(DAO_todo, description, expected_exception):
    """
    Tests creating a todo object with description property as string, integer and None types.
    """
    data = {
        "description": description
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            todo = DAO_todo.create(data)
    else:
        todo = DAO_todo.create(data)
        assert todo["description"] == description


def test_create_task_with_valid_todo(DAO_todo, DAO_task):
    """
    Tests creating a task object containing a todo object with a valid BSON type.
    """
    # Creating a valid todo object.
    todo_data = {
        "description": "Test description"
    }

    new_todo = DAO_todo.create(todo_data)
    todo_id = ObjectId(new_todo['_id']['$oid'])

    # Creating a task object including todo object.
    task_data = {
        "title": "Test title",
        "description": "Test description",
        "todos": [todo_id]
    }

    new_task = DAO_task.create(task_data)

    # Length of task's todos list should be 1.
    assert len(new_task["todos"]) == 1


def test_create_task_with_invalid_todo(DAO_task):
    """
    Tests creating a task object containing a todo object with an invalid BSON type.
    """
    # Creating a task object with a string instead of an ObjectId as BSON type.
    task_data = {
        "title": "Test title",
        "description": "Test description",
        "todos": ["not an ObjectId"]
    }

    # Creating the task object should raise an error.
    with pytest.raises(WriteError):
        DAO_task.create(task_data)

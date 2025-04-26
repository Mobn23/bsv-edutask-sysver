import pytest
from pymongo.errors import WriteError
from bson import ObjectId

from src.util.dao import DAO

@pytest.fixture
def DAO_task():
    dao_task = DAO("task")

    yield dao_task

    dao_task.collection.delete_many({
        "title": {"$regex": "Test title$"}
    })

@pytest.fixture
def DAO_user():
    dao_user = DAO("user")

    yield dao_user

    dao_user.collection.delete_many({
        "email": {"$regex": ".*@example\\.com$"}
    })


@pytest.mark.parametrize('title, expected_exception', [
    ("Test title", None),
    (123, WriteError),
    (None, WriteError)
])
def test_create_task_with_varied_title(DAO_task, title, expected_exception):
    """
    Tests creating a task object with title property as string, integer and None types.
    """
    data = {
        "title": title,
        "description": "Test description"
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            task = DAO_task.create(data)
    else:
        task = DAO_task.create(data)
        assert task["title"] == title


@pytest.mark.parametrize('description, expected_exception', [
    (123, WriteError),
    (None, WriteError)
])
def test_create_task_with_varied_description(DAO_task, description, expected_exception):
    """
    Tests creating a task object with description property as integer and None.
    """
    data = {
        "title": "Test title",
        "description": description
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            task = DAO_task.create(data)
    else:
        task = DAO_task.create(data)
        assert task["description"] == description


def test_create_user_with_valid_task(DAO_task, DAO_user):
    """
    Tests creating a user object containing task property with a valid BSON type.
    """
    # Creating a valid task object.
    task_data = {
        "title": "Test title",
        "description": "Test description"
    }

    new_task = DAO_task.create(task_data)
    task_id = ObjectId(new_task['_id']['$oid'])

    # Creating a valid user object including task object.
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "tasks": [task_id]
    }

    user = DAO_user.create(user_data)

    # Length of user's tasks list should be 1.
    assert len(user["tasks"]) == 1


def test_create_user_with_invalid_task(DAO_user):
    """
    Tests creating a user object containing task property with an invalid BSON type.
    """
    # Creating a user object with a string instead of an ObjectId as BSON type.
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "tasks": ["not an ObjectId"]
    }

    # Creating the user object should raise an error.
    with pytest.raises(WriteError):
        DAO_user.create(user_data)

import pytest
from pymongo.errors import WriteError
from bson import ObjectId

from src.util.dao import DAO

@pytest.fixture
def DAO_video():
    dao_video = DAO("video")

    yield dao_video

    dao_video.collection.delete_many({
        "url": {"$regex": "testurl$"}
    })

@pytest.fixture
def DAO_task():
    dao_task = DAO("task")

    yield dao_task

    dao_task.collection.delete_many({
        "title": {"$regex": "Test title$"}
    })


@pytest.mark.parametrize('url, expected_exception', [
    ("testurl", None),
    (123, WriteError),
    (None, WriteError)
])
def test_create_video_with_varied_url(DAO_video, url, expected_exception):
    """
    Tests creating a video object with url property as string, integer and None types.
    """
    data = {
        "url": url
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            video = DAO_video.create(data)
    else:
        video = DAO_video.create(data)
        assert video["url"] == url


def test_create_task_with_valid_video(DAO_video, DAO_task):
    """
    Tests creating a task object containing a video object with a valid BSON type.
    """
    # Creating a valid video object.
    video_data = {
        "url": "testurl"
    }

    new_video = DAO_video.create(video_data)
    video_id = ObjectId(new_video['_id']['$oid'])

    # Creating a task object including video object.
    task_data = {
        "title": "Test title",
        "description": "Test description",
        "video": video_id
    }

    new_task = DAO_task.create(task_data)

    # Video property should not be None.
    assert new_task["video"] is not None


def test_create_task_with_invalid_video(DAO_task):
    """
    Tests creating a task object containing a video object with an invalid BSON type.
    """
    # Creating a task object with a string instead of an ObjectId as BSON type.
    task_data = {
        "title": "Test title",
        "description": "Test description",
        "video": "invalid video"
    }

    # Creating the task object should raise an error.
    with pytest.raises(WriteError):
        DAO_task.create(task_data)

import pytest
from pymongo.errors import WriteError

from src.util.dao import DAO

@pytest.fixture
def DAO_user():
    dao_user = DAO("user")

    yield dao_user

    dao_user.collection.delete_many({
        "email": {"$regex": ".*@example\\.com$"}
    })

@pytest.mark.parametrize('firstName, expected_exception', [
    ("John", None),
    (123, WriteError),
    (None, WriteError)
])
def test_create_user_with_varied_firstname(DAO_user, firstName, expected_exception):
    """
    Tests three different firstName parameters, one string (that should validate, i.e. not raise an error)
    an integer and a None value that should raise an error.
    """
    data = {
        "firstName": firstName,
        "lastName": "Doe",
        "email": f"{firstName}@example.com"
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            user = DAO_user.create(data)
    else:
        user = DAO_user.create(data)
        assert user["firstName"] == firstName

@pytest.mark.parametrize('lastName, expected_exception', [
    (123, WriteError),
    (None, WriteError)
])
def test_create_user_with_varied_lastname(DAO_user, lastName, expected_exception):
    """
    Tests two different lastName parameters, an integer and a None value that should raise an error.
    lastName as a string has already been tested.
    """
    data = {
        "firstName": "John",
        "lastName": lastName,
        "email": f"John@example.com"
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            user = DAO_user.create(data)
    else:
        user = DAO_user.create(data)
        assert user["lastName"] == lastName

@pytest.mark.parametrize('email, expected_exception', [
    (123, WriteError),
    (None, WriteError)
])
def test_create_user_with_varied_email(DAO_user, email, expected_exception):
    """
    Tests two different email parameters, an integer and a None value that should raise an error.
    email as a string has already been tested.
    """
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": email
    }

    if expected_exception:
        with pytest.raises(expected_exception):
            user = DAO_user.create(data)
    else:
        user = DAO_user.create(data)
        assert user["email"] == email

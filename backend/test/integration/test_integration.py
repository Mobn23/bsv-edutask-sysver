import pytest
from pymongo.errors import WriteError, DuplicateKeyError

from src.util.dao import DAO

@pytest.fixture
def test_dao():
    # initialize a new DAO object with "test_user" as collection
    test_dao = DAO("test_user")

    yield test_dao

    # drop entire collection
    test_dao.drop()

@pytest.mark.integration
def test_create_valid_user(test_dao):
    """
    Tests to create a user with valid input data, i.e. all required properties, correct bson data types, and unique email.
    """
    user_data = {
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@example.com"
    }

    user = test_dao.create(user_data)
    assert user is not None

@pytest.mark.integration
def test_create_duplicate_users(test_dao):
    """
    Tests to create two users with same email.
    Expects DuplicateKeyError to be raised since email must be unique according to ground truth.
    """
    user_data1 = {
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@example.com"
    }

    user_data2 = {
        "firstName": "John2",
        "lastName": "Smith2",
        "email": "john.smith@example.com"
    }

    # Creating first user should not raise any errors.
    test_dao.create(user_data1)

    # Creating second user with same email should raise DuplicateKeyError.
    with pytest.raises(DuplicateKeyError):
        test_dao.create(user_data2)

@pytest.mark.integration
def test_create_invalid_user_wrong_bson_data_type(test_dao):
    """
    Tests to create a user with integer instead of string for email property.
    Expects WriteError to be raised since bson data type is incorrect.
    """
    user_data = {
        "firstName": "John",
        "lastName": "Smith",
        "email": 123
    }

    with pytest.raises(WriteError):
        test_dao.create(user_data)

@pytest.mark.integration
def test_create_invalid_user_missing_field(test_dao):
    """
    Tests to create a user without required property email.
    Expects WriteError to be raised since email is missing and required.
    """
    user_data = {
        "firstName": "John",
        "lastName": "Smith"
    }

    with pytest.raises(WriteError):
        test_dao.create(user_data)

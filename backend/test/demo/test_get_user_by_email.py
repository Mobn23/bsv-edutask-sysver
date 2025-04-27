import pytest
from unittest.mock import MagicMock
from src.controllers import usercontroller


class TestGetUserByEmail:
    """This test demonstrates the cases of the get_user_by_email()"""

    @pytest.mark.unit
    def test_one_user(self):
        """
        Tests get_user_by_email() returning one email as output when there's no duplications .
        """

        mock_dao = MagicMock()
        mock_dao.find.return_value = [
            {"email": "mobn23@student.bth.se"}
        ]

        userController = usercontroller.UserController( dao = mock_dao )
        result = userController.get_user_by_email("mobn23@student.bth.se")
        # print("result", result)
        assert result["email"] == "mobn23@student.bth.se"

    @pytest.mark.unit
    def test_many_users(self, capfd):
        """
            Tests get_user_by_email() returning Error, & the 1st email when duplicated emails found for the same user.
        """

        mock_dao = MagicMock()
        mock_dao.find.return_value = [
            {"email": "mobn23@student.bth.se"},
            {"email": "mobn23@student.bth.se"}
        ]

        userController = usercontroller.UserController( dao = mock_dao )
        result = userController.get_user_by_email("mobn23@student.bth.se")
        out, err = capfd.readouterr()
        # print("result", result)
        # print("out", out)
        assert 'Error: more than one user found with mail mobn23@student.bth.se' in out
        assert result["email"] == "mobn23@student.bth.se"

    @pytest.mark.unit
    def test_passed_invalid_email_format(self):
        """
        Tests get_user_by_email() the passed email parameter's format invalid (Simple validation checking if contains @ as implemented in the dao ).
        """

        mock_dao = MagicMock()
        mock_dao.find.return_value = [
            {"email": "mobn23@student.bth.se"}
        ]

        userController = usercontroller.UserController( dao = mock_dao )
        with pytest.raises(ValueError) as exc_info:
            userController.get_user_by_email("mobn23student.bth.se")

        # print("exc_info", exc_info)
        assert 'Error: invalid email address' in str(exc_info)

    @pytest.mark.unit
    def test_exception_find_returns_nothing(self):
        """
        Tests the exception case when find() returns nothing (users undefined).
        """

        mock_dao = MagicMock()
        mock_dao.find.return_value = []

        userController = usercontroller.UserController( dao = mock_dao )
        with pytest.raises(Exception) as exc_info:
            userController.get_user_by_email("mobn23@student.bth.se")

        print("exc_info: test_exception_find_returns_nothing", exc_info)
        assert isinstance(exc_info.value, Exception)

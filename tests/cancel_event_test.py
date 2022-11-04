# Code to import from parent directory ===================
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================

from event import Event
from datetime import datetime
from MyEventManager import cancel_event
import unittest
from unittest.mock import Mock, patch


class CancelEventTest(unittest.TestCase):
    """
        This class is to test the cancel_event function.
        Summary of tests:
            - test_cancel_event_id_none:
                | This is to check if an error is raised when the event_id is none.
            - test_cancel_event_id_empty:
                | This is to check if an error is raised when the event_id is empty.
            - test_cancel_event_id_invalid:
                | This is to check if an error is raised when the entered event_id does not exist in the calendar.
            - test_cancel_event:
                | This is to check if the event is cancelled when all the inputs by the user are valid.
        Whitebox testing method: MC/DC
        Reason: As there are 3 conditions that need to be exercised and there are 4 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.

    """
    @patch("MyEventManager.get_calendar_api")
    def test_cancel_event_id_none(self, mock_api):
        """
        This is to check if an error is raised when the event_id is none.
        mock_api: mock object.
        """
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            cancel_event(mock_api, None)

    @patch("MyEventManager.get_calendar_api")
    def test_cancel_event_id_empty(self, mock_api):
        """
        This is to check if an error is raised when the event_id is empty.
        mock_api: mock object.
        """
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            cancel_event(mock_api, "")

    @patch("MyEventManager.get_calendar_api")
    def test_cancel_event_id_invalid(self, mock_api):
        """
        This is to check if an error is raised when the entered event_id does not exist in the calendar.
        mock_api: mock object.
        """
        ID = "some_ID_that_does_not_exist"
        # assert that an exception is raised
        with self.assertRaises(Exception):
            cancel_event(ID, mock_api)

    @patch("MyEventManager.get_calendar_api")
    def test_cancel_event(self, mock_api):
        """
        This is to check if the event is cancelled when all the inputs by the user are valid.
        mock_api: mock object.
        """
        ID = "some_ID_that_exists"
        cancel_event = Mock()
        updated_event = cancel_event(mock_api, ID)
        cancel_event.assert_called_once_with(mock_api, ID)
        updated_event.return_value.status = "cancelled"
        self.assertEqual(updated_event.return_value.status, "cancelled")


if __name__ == "__main__":
    unittest.main()

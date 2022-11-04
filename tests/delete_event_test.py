# Code to import from parent directory ===================
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================

from MyEventManager import delete_event
from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock, patch


class DeleteEventTest(unittest.TestCase):
    """
    This class is set to test the delete_event function
    Summary of class:
        - test_delete_raises_error_when_none:
            | This test is to check if the delete_event function raises an error when the event is deleted without it
            being created
        - test_delete_future_event:
            | This test will check if a future event cannot be deleted
        - test_delete_current_date_event:
            | The application should not delete an event on the present date
        - test_delete_past_event:
            | This is to check if the delete function would delete an event on the current date.
        - test_delete_event_raises_error_while_getting_event:
            | This is to check if an error is raised when the event is not found.
    Whitebox testing method: Statement Coverage
    Reason: We used Statement Coverage because this method allowed us to write tests which account for 100% line coverage.
    """

    @patch("MyEventManager.get_calendar_api")
    def test_delete_raises_error_when_none(self, mock_api):
        """
        This test is to check if the delete_event function raises an error when the event is deleted without it
        being created
        """
        # assert an exception raised
        with self.assertRaises(ValueError):
            delete_event(mock_api, None)

    @patch("MyEventManager.get_calendar_api")
    def test_delete_future_event(self, mock_api):
        """
        This test will check if a future event cannot be deleted
        mock_api (Mock): @patch decorator passes this argument
        """
        current_date = datetime.now()
        time_delta = timedelta(days=1)
        event_date = current_date + time_delta

        eventID = "some_event_ID_in_future"
        with patch("MyEventManager.get_event_by_id") as mock_get_event_by_id:
            # mock_get_event_by_id["start"]["date"] = event_date
            mock_get_event_by_id.return_value = {"start": {"date": event_date}}
            with self.assertRaises(ValueError):
                delete_event(mock_api, eventID)

    @patch("MyEventManager.get_calendar_api")
    def test_delete_current_date_event(self, mock_api):
        """
        The application should not delete an event on the present date
        mock_api (Mock): @patch decorator passes this argument
        """
        event_date = datetime.now()

        eventID = "some_event_ID"
        with patch("MyEventManager.get_event_by_id") as mock_get_event_by_id:
            # mock_get_event_by_id["start"]["date"] = event_date
            mock_get_event_by_id.return_value = {"start": {"date": event_date}}
            with self.assertRaises(ValueError):
                deleted_event = delete_event(mock_api, eventID)
                delete_event.side_effect = ValueError(
                    "Cannot delete an event on the current date"
                )

    # deleting events test in the past
    @patch("MyEventManager.get_calendar_api")
    def test_delete_past_event(self, mock_api):
        """
        This is to check if the delete function would delete an event on the current date.
        mock_api (Mock): @patch decorator passes this argument
        """
        current_date = datetime.now()
        time_delta = timedelta(days=-1)
        event_date = current_date + time_delta

        eventID = "some_event_ID_in_future"
        with patch("MyEventManager.get_event_by_id") as mock_get_event_by_id:
            # mock_get_event_by_id["start"]["date"] = event_date
            mock_get_event_by_id.return_value = {"start": {"date": event_date}}
            try:
                delete_event(mock_api, eventID)
            except ValueError:
                self.fail("delete_event() raised ValueError unexpectedly!")

    @patch("MyEventManager.get_calendar_api")
    def test_delete_event_raises_error_while_getting_event(self, mock_api):
        """
        This is to check if an error is raised when the event is not found.
        mock_api (Mock): @patch decorator passes this argument
        """
        eventID = "some_event_ID_that_does_not_exist"
        with patch("MyEventManager.get_event_by_id") as mock_get_event_by_id:
            mock_get_event_by_id.side_effect = ValueError("Event not found")
            with self.assertRaises(ValueError):
                delete_event(mock_api, eventID)


if __name__ == "__main__":
    unittest.main()

# Code to import from parent directory ===================
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================

from event import Event
from address import Address
from people.attendee import Attendee
from MyEventManager import post_event
from datetime import datetime
import unittest
from unittest.mock import Mock, patch



class PostEventTest(unittest.TestCase):
    """
    This class is to test the post_event function
    Summary of tests:
        - test_post_event_raises_error_when_none:
            | This test is to check if the post_event function raises an error when the event is None

        - test_post_event_invalid_attendees:
            | This test is to check if the post_event function raises an error when the details of attendees are invalid

        - test_post_event_invalid_address:
            | This test is to check if the post_event function raises an error when the details of address are invalid

        - test_post_event:
            | This test is to check if the post_event function works as expected when all the details are valid
    """

    @patch("MyEventManager.get_calendar_api")
    def test_post_event_raises_error_when_none(self, mock_api):
        """
        This test tests whether the function post_event raises an error when
        the event is None.
        Args:
            mock_api (Mock): @patch decorator passes this argument
        """
        # assert that an exception is raised
        with self.assertRaises(AttributeError):
            post_event(mock_api, None)

    @patch("MyEventManager.get_calendar_api")
    def test_post_event_invalid_attendees(self, mock_api):
        """
        This test tests whether the function post_event raises an error when
        the event contains attendees with invalid arguments.
        Args:
            mock_api (Mock): @patch decorator passes this argument
        """
        # Initialising Address
        test_address = Address(
            "Mr. Johnny", "st. Monash University", "Clayton", "VIC", "3800"
        )
        # Initialising Attendees
        test_attendee = [
            Attendee("John 1", "john@email.com"),
            Attendee("John", "johnemail.com"),
        ]
        # Initialising Event
        test_event = Event(
            "Test Event",
            "Test description",
            time=datetime.now(),
            address=test_address,
            attendees=test_attendee,
        )
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            post_event(mock_api, test_event)

    @patch("MyEventManager.get_calendar_api")
    def test_post_event_invalid_address(self, mock_api):
        """
        This test tests whether the function post_event raises an error when
        the event contains an invalid address.
        Args:
            mock_api (Mock): @patch decorator passes this argument
        """
        # Initialising Address
        # Incorrect spelling for street
        test_address = Address(
            "Mr. Johnny",
            "stret Monash University",
            "Clayton",
            "VIC",
            "3800",
        )
        # Initialising Attendees
        test_attendee = [
            Attendee("John Doe", "johndoe@email.com"),
            Attendee("Jane Doe", "janedoe@email.com"),
        ]
        # Initialising Event
        test_event = Event(
            "Test Event",
            "Test description",
            time=datetime.now(),
            address=test_address,
            attendees=test_attendee,
        )
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            post_event(mock_api, test_event)

    @patch("MyEventManager.get_calendar_api")
    def test_post_event(self, mock_api):
        """This test is to check if the post_event function works
        It works by mocking the get_calendar_api function and checking if the event is created
        Additionally, the response of the API is also a Mock object.
        Finally, the event body is compared against the union of the mocked response and the event body

        Args:
            mock_api (Mock): Mock object for the get_calendar_api function
        """

        test_address = Address(
            "Mr. Johnny", "st . Monash University", "Clayton", "VIC", "3800"
        )
        test_attendees = [
            Attendee("John Doe", "johndoe@email.com"),
            Attendee("Jane Doe", "jane@email.com"),
        ]

        event = Event(
            "Testing",
            "This is a test",
            datetime(2022, 10, 10, 10, 10, 10),
            test_address,
            test_attendees,
        )

        # response = Mock()
        # response.return_value = post_event(mock_api, event)
        # response.return_value = event.body()
        # self.assertEqual(event.body(), response.return_value)

        response = post_event(mock_api, event)
        response.return_value = mock_api.events.return_value.insert.call_args_list
        self.assertEqual(event.body(), response.return_value[0][1]["body"])


if __name__ == "__main__":
    unittest.main()

# Code to import from parent directory ===================
import sys
import os
from unittest.mock import patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================
import unittest
from MyEventManager import search_events


class SearchEventTest(unittest.TestCase):
    @patch("MyEventManager.get_calendar_api")
    def test_tag_is_none(self, mock_api):
        """
        This test is to check if the search_event function raises an error when the tag is None
        """
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            search_events(mock_api, None, None)

    @patch("MyEventManager.get_calendar_api")
    def test_tag_is_empty(self, mock_api):
        """
        This test is to check if the search_event function raises an error when the tag is empty
        """
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            search_events(mock_api, "", None)

    @patch("MyEventManager.get_calendar_api")
    def test_value_is_none(self, mock_api):
        """
        This test is to check if the search_event function raises an error when the value is None
        """
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            search_events(mock_api, "summary", None)

    @patch("MyEventManager.get_calendar_api")
    def test_value_is_empty(self, mock_api):
        """
        This test is to check if the search_event function raises an error when the value is empty
        """
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            search_events(mock_api, "summary", "")

    @patch("MyEventManager.get_calendar_api")
    def test_no_event_matched(self, mock_api):
        """
        This test is to check if the search_event function returns an empty list when no event is matched
        """
        # assert that an exception is raised
        with patch("MyEventManager.search_events") as search_events:
            events = search_events(mock_api, "summary", "some_value", mock_api)
            self.assertEqual(len(events), 0)


if __name__ == "__main__":
    unittest.main()

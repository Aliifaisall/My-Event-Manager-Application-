import unittest
from unittest.mock import MagicMock, Mock, patch

# Add other imports here if needed
import MyEventManager
from tests.address_test import AddressTest
from tests.attendees_test import AttendeesTest
from tests.event_test import EventTest
from tests.post_events_test import PostEventTest
from tests.delete_event_test import DeleteEventTest
from tests.cancel_event_test import CancelEventTest

class MyEventManagerTest(unittest.TestCase):
    # This test tests number of upcoming events.
    # def setUp(self):
    #     self.MyEventManager = MyEventManager()

    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count,
            1,
        )

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs["maxResults"], num_events)

    # Add more test cases here
    @patch("MyEventManager.get_calendar_api")
    def test_get_upcoming_events_raise_error(self, mock_api):
        """
        This test tests whether the function get_upcoming_events raises an error when
        the number of events is less than 1.
        Args:
            mock_api (Mock): @patch decorator passes this argument
        """
        num_events = 0
        time = "2020-08-03T00:00:00.000000Z"
        # assert that an exception is raised
        with self.assertRaises(ValueError):
            MyEventManager.get_upcoming_events(mock_api, time, num_events)

    def test_get_upcoming_events_time(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs["timeMin"], time)




def main():
    def load_test(test_class: unittest.TestCase) -> unittest.TestSuite:
        return unittest.TestLoader().loadTestsFromTestCase(test_class)

    # Create the test suite from the cases above.
    # fmt: off
    my_event_manager_test_suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(my_event_manager_test_suite)

    # Our test suites
    address_test_suite = load_test(AddressTest)
    attendees_test_suite = load_test(AttendeesTest)
    event_test_suite = load_test(EventTest)
    post_events_test_suite = load_test(PostEventTest)
    delete_event_test_suite = load_test(DeleteEventTest)
    cancel_event_test_suite = load_test(CancelEventTest)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(address_test_suite)
    runner.run(attendees_test_suite)
    runner.run(event_test_suite)
    runner.run(post_events_test_suite)
    runner.run(delete_event_test_suite)
    runner.run(cancel_event_test_suite)

    # # Create the test suite for the event location address
    # address_test_suite = unittest.TestLoader().loadTestsFromTestCase(AddressTest)
    # # running the test suite for the event address
    # unittest.TextTestRunner(verbosity=2).run(address_test_suite)

    # # create the test suite for the event attendess
    # attendees_test_suite = unittest.TestLoader().loadTestsFromTestCase(AttendeesTest)
    # # running the test suite for the event attendees
    # unittest.TextTestRunner(verbosity=2).run(attendees_test_suite)

    # # create the test suite for the event as a whole
    # event_test_suite = unittest.TestLoader().loadTestsFromTestCase(EventTest)
    # # running the test suite for the event attendees
    # unittest.TextTestRunner(verbosity=2).run(event_test_suite)


main()
if __name__ == "_main_":
    unittest.main()

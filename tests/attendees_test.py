# Code to import from parent directory ===================
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================


import unittest
from people.attendee import Attendee


class AttendeesTest(unittest.TestCase):
    """
        This class is to test the attendee function.
        Summary of tests:
            - test_attendee_name:
                | This is to check if the validation raises an error with an empty name.
            - test_attendee_name1:
                | This is to check if the validation checks off when the name is valid.
            - test_attendee_name2:
                | This is to check if the validation raises an error when the name is anything except alphabets or space.
            - test_attendee_email:
                | This is to check if the validation raises an error with an empty email.
            - test_attendee_email1:
                | This is to check if the validation raises an error when the email does not follow the provided regex format.
            - test_attendee_email2:
                | This is to check if the validation checks off when the email is valid.
        Whitebox testing method: MC/DC
        Reason: We've used MC/DC testing method for testing the name and email of the attendee separately.
    """

    def test_attendees_name(self):
        """
        This is to check if the validation raises an error with an empty name.
        Whitebox testing method: MC/DC
        Reason: As there are 2 conditions that need to be exercised and there are 3 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.
        """
        name = ""
        attendees = Attendee(name, "email@mail.com")
        with self.assertRaises(ValueError):
            attendees.validate()

    def test_attendees_name1(self):
        """
        This is to check if the validation checks off when the name is valid.
        Whitebox testing method: MC/DC
        Reason: As there are 2 conditions that need to be exercised and there are 3 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.
        """
        name = "ALI"
        attendees = Attendee(name, "email@mail.com")
        self.assertTrue(attendees.validate())

    def test_attendees_name2(self):
        """
        This is to check if the validation raises an error when the name is anything except alphabets or space.
        Whitebox testing method: MC/DC
        Reason: As there are 2 conditions that need to be exercised and there are 3 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.
        """
        name = "!@#$%RDWEDFER@#"
        attendees = Attendee(name, "email@mail.com")
        with self.assertRaises(ValueError):
            attendees.validate()

    def test_attendees_email(self):
        """
        This is to check if the validation raises an error with an empty email.
        Whitebox testing method: MC/DC
        Reason: As there are 2 conditions that need to be exercised and there are 3 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.
        """
        email = ""
        attendees = Attendee("Ali", email)
        with self.assertRaises(ValueError):
            attendees.validate()

    def test_attendees_email1(self):
        """
        This is to check if the validation raises an error when the email does not follow the provided regex format.
        Whitebox testing method: MC/DC
        Reason: As there are 2 conditions that need to be exercised and there are 3 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.
        """
        email = "Ali"
        attendees = Attendee("Ali", email)
        with self.assertRaises(ValueError):
            attendees.validate()

    def test_attendees_email2(self):
        """
        This is to check if the validation checks off when the email is valid.
        Whitebox testing method: MC/DC
        Reason: As there are 2 conditions that need to be exercised and there are 3 tests to do that which suffices the
        N + 1 criteria for this whitebox testing method.
        """
        email = "Ali@mail.com"
        attendees = Attendee("Ali", email)
        self.assertTrue(attendees.validate())


if __name__ == "__main__":
    unittest.main()

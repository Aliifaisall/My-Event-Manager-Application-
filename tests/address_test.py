# Code to import from parent directory ===================
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# ========================================================

from address import Address
import unittest


class AddressTest(unittest.TestCase):
    """
        This class is to test the address function
        Summary of tests:
            - test_address_name:
                | This test is to check if the validation raises an error with an empty name

            - test_address_name2:
                | This test is to check if capital letters are valid

            - test_address_name3:
                | This test is to check if lowercase letters are valid

            - test_address_name4:
                | This test is to check that name does not accept anything except the alphabet letters.

            - test_address_street:
                | This test is to check if the validation raises an error with an empty street name.

            - test_address_street3:
                | This test is to check if the validation checks with a valid input.

            - test_address_street4:
                | This test is to check that name does not accept anything except the alphabet letters.

            - test_address_postcode:
                | This is to check if the validation raises an error when the user inserts a postcode that is less than
                3 digits.

            - test_address_postcode1:
                | This is to check if the validation checks off when the user inserts a postcode within the range that are
                specified in the specification.

            - test_address_postcode2:
                | This is to check if the validation raises an error when the user inserts something bigger than 10 characters.

            - test_address_postcode3:
                | This is to check if the validation raises an error when the user inserts an empty postcode.

            - test_address_suburb:
                | This is to check if the validation raises an error when the suburb is an empty string.

            - test_address_suburb1:
                | This is to check if the validation raises an error when the input suburb is out of the english alphabet.

            - test_address_suburb2:
                | This is to check if the validation checks off when the input suburb is within the english alphabet.

            - test_address_state:
                | This is to check if the validation raises an error when length of the input for state less than 1 or empty.

            - test_address_state1:
                | This is to check if the validation checks off when the lenght of the state is within the specified range.

            - test_address_state2:
                | This is to check if the validation raises an error when the length of the input state is more than 3 characters.

            - test_address_state3:
                | This is to check if the validation raises an error when the input state is out of the english alphabet.

        Whitebox Testing Method: Branch Coverage
        Reason: As the test functions in this class all together are exercising every possible alternative branch for the
        validate function in address.py atleast once, therefore Branch Coverage is the most suitable Whitebox testing
        strategy for this.
        """

    def test_address_name(self):
        """
        This test is to check if the validation raises an error with an empty name
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple invalid and valid inputs
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks whether the input is empty or not.
        """
        name = ""
        address = Address(name, "street", "HOWIT", "VIC", "3168")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_name2(self):
        """
        This test is to check if capital letters are valid
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple invalid and valid inputs
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the name contains nothing except alphabets and
        space.
        """
        name = "ALI"
        address = Address(name, "street", "HOWIT", "VIC", "3168")
        self.assertTrue(address.validate())

    def test_address_name3(self):
        """
        This test is to check if lowercase letters are valid
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple invalid and valid inputs
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the name contains nothing except alphabets and
        space.
        """
        name = "ali"
        address = Address(name, "street", "HOWIT", "VIC", "3168")
        self.assertTrue(address.validate())

    def test_address_name4(self):
        """
        This test is to check that name does not accept anything except the alphabet letters.
        Blackbox testing method: Equivalence Partitioning
        Reason: the name should not accept anything outside the alphabetic letters
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the name contains nothing except alphabets and
        space.
        """
        name = "2346"
        address = Address(name, "street", "HOWIT", "VIC", "3168")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_street(self):
        """
        This test is to check if the validation raises an error with an empty street name.
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple invalid and valid inputs
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the street is not an empty string.
        """
        street = ""
        address = Address("Ali", street, "HOWIT", "VIC", "3168")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_street3(self):
        """
        This test is to check if the validation checks with a valid input.
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple valid and invalid inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the street is nothincg except alphanumeric
        characters and spaces and is valid street according to the provided list.
        """
        street = "avenue"
        address = Address("Ali", street, "HOWIT", "VIC", "3168")
        self.assertTrue(address.validate())

    def test_address_street4(self):
        """
        This test is to check if the validation raises an error when the spelling for street name is wrong.
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple valid and invalid inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the street is nothincg except alphanumeric
        characters and spaces and is valid street according to the provided list.
        """
        street = "stret"
        address = Address("Ali", street, "HOWIT", "VIC", "3168")
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_postcode(self):
        """
        This is to check if the validation raises an error when the user inserts a postcode that is less than 3 digits.
        Blackbox testing method: Boundary Value Partitioning
        Reason: As the input has to be between a range of specified inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the input is nothing except numbers and falls
        in the specified range or not.
        """
        postcode = "12"
        address = Address("Ali", "street", "HOWIT", "VIC", postcode)
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_postcode1(self):
        """
        This is to check if the validation checks off when the user inserts a postcode within the range that are
        specified in the specification.
        Blackbox testing method: Boundary Value Partitioning
        Reason: As the input has to be between a range of specified inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the input is nothing except numbers and falls
        in the specified range or not.
        """
        postcode = "12398"
        address = Address("Ali", "street", "HOWIT", "VIC", postcode)
        self.assertTrue(address.validate())

    def test_address_postcode2(self):
        """
        This is to check if the validation raises an error when the user inserts something bigger than 10 characters.
        Blackbox testing method: Boundary Value Partitioning
        Reason: As the input has to be between a range of specified inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the input is nothing except numbers and falls
        in the specified range or not.
        """
        postcode = "12334567891"
        address = Address("Ali", "street", "HOWIT", "VIC", postcode)
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_postcode3(self):
        """
        This is to check if the validation raises an error when the user inserts an empty postcode.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the postcode is empty or not.
        """

    def test_address_suburb(self):
        """
        This is to check if the validation raises an error when the suburb is an empty string.
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple valid and invalid inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the suburb is empty or not.
        """
        suburb = ""
        address = Address("Ali", "street", suburb, "VIC", "3148")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_suburb1(self):
        """
        This is to check if the validation raises an error when the input suburb is out of the english alphabet.
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple valid and invalid inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the suburb is nothing except alphabets and
        spaces.
        """
        suburb = "122334"
        address = Address("Ali", "street", suburb, "VIC", "3148")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_suburb2(self):
        """
        This is to check if the validation checks off when the input suburb is within the english alphabet.
        Blackbox testing method: Equivalence Partitioning
        Reason: As there are multiple valid and invalid inputs.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the suburb is nothing except alphabets and
        spaces.
        """
        suburb = "howit"
        address = Address("Ali", "street", suburb, "VIC", "3148")
        self.assertTrue(address.validate())

    def test_address_state(self):
        """
        This is to check if the validation raises an error when length of the input for state less than 1 or empty.
        Blackbox testing method: Boundary Value Partitioning
        Reason: As the input cannot be anything out of the english alphabet and the length is to be within a specified range.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks that the state is empty or not.
        """
        state = ""
        address = Address("Ali", "street", "howit", state, "3148")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_state1(self):
        """
        This is to check if the validation checks off when the length of the state is within the specified range.
        Blackbox testing method: Boundary Value Partitioning
        Reason: As the input cannot be anything out of the english alphabet and the length is to be within a specified range.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks if the state is nothing except alphabet and spaces
        and also fall in the specified range.
        """
        state = "VIC"
        address = Address("Ali", "street", "howit", state, "3148")
        self.assertTrue(address.validate())

    def test_address_state2(self):
        """
        This is to check if the validation raises an error when the length of the input state is more than 3 characters.
        Blackbox testing method: Boundary Value Partitioning
        Reason: As the input cannot be anything out of the english alphabet and the length is to be within a specified range.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks if the state is nothing except alphabet and spaces
        and also fall in the specified range.
        """
        state = "ABCDEF"
        address = Address("Ali", "street", "howit", state, "3148")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()

    def test_address_state3(self):
        """
        This is to check if the validation raises an error when the input state is out of the english alphabet.
        Blackbox testing method: Random Testing
        Reason: As the input for this test can be anything except the english alphabet.
        Whitebox testing method: Branch Coverage
        Reason: This test function covers the branch where it checks if the state is nothing except alphabet and spaces.
        """
        state = "12344"
        address = Address("Ali", "street", "howit", state, "3148")
        # self.assertFalse(address.validate())
        with self.assertRaises(ValueError):
            address.validate()


if __name__ == "__main__":
    unittest.main()

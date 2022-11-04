from importlib.util import set_loader
import re


def split_multiple(delimiters, string):
    regex_pattern = "|".join(map(re.escape, delimiters))
    return re.split(regex_pattern, string)


class Address:
    """
    This class is used to create an address object.
    Args:
        name: A string input for the name of the person.
        street: A string input for the street the person lives on.
        suburb: A string input for the suburb the person lives in.
        state: A string input for the state the person lives in.
        postcode: A string or an integer input for the postcode of the place the person lives in.
    """
    def __init__(self, name: str, street: str, suburb: str, state: str, postcode: int or str ) -> None:
        """
        Constructor to initialise the parameters for an address.
        """
        self.name = name
        self.street = street
        self.suburb = suburb
        self.state = state
        self.postcode = str(postcode)
        self.valid_streets = [
            "st",
            "street",
            "avenue",
            "way",
            "ave",
            "walk",
            "rd",
            "road",
        ]
        # fmt: off
        # self.white_list_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
        #                            "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "."]
        # fmt: on

    def validate(self) -> bool:
        """
        This function is to check if the address fulfils all the criteria for being a valid address.
        """
        delimiters = [" ", ".", "-", ",", "/", "\\", ";", ":"]

        # Testing address name
        if self.name == "":
            raise ValueError("Name cannot be empty")

        if not all(
                char.isalpha() or char.isspace() or char in delimiters for char in self.name
        ):
            raise ValueError("Name can only contain letters and spaces")

        # Testing street ==========================================================
        if self.street == "":
            raise ValueError("Street cannot be empty")

        street_words = split_multiple(delimiters, self.street)
        if not (
                all(
                    char.isalnum() or char.isspace() or char in [".", ","]
                    for char in street_words
                    if char != ""
                )
                and any(word.lower() in self.valid_streets for word in street_words)
        ):
            raise ValueError(
                "Street can only contain letters, spaces, and valid street suffixes"
            )

        # Testing suburb ==========================================================
        if self.suburb == "":
            raise ValueError("Suburb cannot be empty")

        if not all(
                char.isalpha() or char.isspace() or char in delimiters
                for char in self.suburb
        ):
            raise ValueError("Suburb can only contain letters and spaces")

        # Testing state ==========================================================
        if self.state == "":
            raise ValueError("State cannot be empty")

        if not 3 <= len(str(self.state)) <= 5:
            raise ValueError("State must be between 3 and 5 characters")

        if not all(char.isalpha() or char.isspace() for char in self.state):
            raise ValueError("State can only contain letters and spaces")

        # Testing postcode ==========================================================
        if self.postcode == "":
            raise ValueError("Postcode cannot be empty")

        if not all(char.isnumeric() for char in self.postcode):
            raise ValueError("Postcode can only contain numbers")

        if not 4 <= len(str(self.postcode)) <= 10:
            raise ValueError("Postcode must be between 4 and 10 characters")

        return True

    def body(self) -> str:
        """
        This function returns a string value for the api.
        """
        return str(self)

    def __str__(self) -> str:
        """
        This function converts the object to a string and overrides the string method.
        """
        string = ""
        string += f"Name: {self.name}\n"
        string += f"Street: {self.street}\n"
        string += f"Suburb: {self.suburb}\n"
        string += f"State: {self.state}\n"
        string += f"Postcode: {self.postcode}\n"
        return string

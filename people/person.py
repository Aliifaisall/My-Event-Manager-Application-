class Person:
    """
    This class is used as a super class for attendee.py and event_organiser.py.
    """
    def __init__(self, name: str, email: str) -> None:
        """
        Constructor to initialise the parameters for a person.
        """
        self.name = name  # This is displayName
        self.email = email
        self.organiser = False
        self.white_list_letters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]

    def validate(self) -> None:
        """
        This function is being overridden by the attendee.py and event_organiser.py.
        """
        pass

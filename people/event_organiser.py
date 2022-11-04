from person import Person
import re


class EventOrganiser(Person):
    """
    This class is used to creat an Event organiser object.
    """

    def __init__(self, name, email):
        """
        Constructor to initialise the parameters for an event organiser.
        """
        super().__init__(name, email)
        self.organiser = True

    def validate(self):
        """
        This function is to check if the event organiser fulfils all the criteria for being a valid event organiser.
        """
        if self.name == "":
            raise ValueError("Name cannot be empty")

        if not all(
                char.isalpha() or char.isspace() for char in self.name
        ):
            raise ValueError("Name can only contain letters and spaces")

        email_regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"

        if not re.match(email_regex, self.email):
            raise ValueError("Email is incorrect")
        return True

from people.person import Person
import re


class Attendee(Person):
    """
    This class is used to create a new attendee object.
    """
    def __init__(self, name, email):
        """
        Constructor to initialise the parameters for an attendee.
        """
        super().__init__(name, email)

    def validate(self):
        """
        This function is to check if the attendee fulfils all the criteria for being a valid attendee.
        """
        # testing attendees name ==================================================================
        if self.name == "":
            raise ValueError("Name cannot be empty")
      
        for char in self.name.lower():
            if not (char.isalpha() or char.isspace()):
                raise ValueError("Name can only contain letters and spaces")
        
        # testing attendees email ========================================================
        if self.email == "":
            raise ValueError("Email cannot be empty")

        email_regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if not re.match(email_regex, self.email):
            raise ValueError("Email is not valid")

        return True

    def body(self):
        """
        This function returns a string value for the api.
        """
        return {
            "email": self.email,
            "displayName": self.name,
            "responseStatus": "needsAction",
        }


if __name__ == "__main__":
    person = Attendee("Vansh", "abc@email.com")
    print(person.validate())

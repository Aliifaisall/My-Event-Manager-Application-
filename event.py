from datetime import datetime
from datetime import datetime, timezone
import uuid
import random
from address import Address
from people.attendee import Attendee


def generate_id():
    """
    This function is used to generate an id.
    """
    # fmt: off
    valid_chars = (
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "v",
    )
    # fmt: on
    _uuid = list(str(uuid.uuid4()).replace("-", random.choice(valid_chars)))
    for i, char in enumerate(_uuid):
        if char not in valid_chars:
            _uuid[i] = random.choice(valid_chars)

    return "".join(_uuid)


class Event:
    """
    This class is used to create an object for an event.
    """
    def __init__(
        self,
        event_name: str,
        description: str,
        time: datetime,
        address: Address,
        attendees: list[Attendee],
    ) -> None:
        """
        Initialize an event object. This object will hold details about an event
        Args:
            id (str): The unique identifier of the event
            description (str): Description of the event
            time (datetime): The time of the event
            address (str): The address of the event
        """
        # Generate a valid unique ID based on the UUID standar RFC 4122
        self.id = generate_id()
        self.event_name = event_name
        self.description = description
        self.time = time.replace(tzinfo=timezone.utc)
        self.address = address
        self.attendees = attendees
        # fmt: off
        self.white_list_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                                   "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
        # fmt: on

    def validate(self) -> bool:
        """
        Validates the event object
        Returns:
        bool: True if the event is valid, False otherwise
        """
        if self.event_name == "":
            raise ValueError("Event name cannot be empty")

        if not all(char.isalnum() or char.isspace() for char in self.event_name):
            raise ValueError("Event name can only contain letters and spaces")

        if len(self.attendees) > 20:
            raise ValueError("Event cannot have more than 20 attendees")

        for attendee in self.attendees:
            if isinstance(attendee, Attendee):
                attendee.validate()

            elif isinstance(attendee, dict):
                if not attendee["email"] or not attendee["displayName"]:
                    raise ValueError("Attendee must have an email and display name")
            else:
                return ValueError("Attendee should be an Attendee object")

        if not self.address.validate():
            raise ValueError("Address is not valid")

        if self.time == "":
            raise ValueError("Time cannot be empty")

        if self.time.year >= 2050:
            raise ValueError("date can't be after 2050")

        return True

    def body(self) -> dict:
        """
        Returns:
            dict: The body of the event to be sent to the Google Calendar API
        """
        MAX_ATTENDEES = 20

        if not self.validate():
            return {}

        return {
            "id": self.id,
            "description": self.description,
            "summary": self.event_name,
            "location": self.address.body(),
            "start": {"dateTime": self.time.isoformat()},
            "end": {"dateTime": self.time.isoformat()},
            "maxAttendees": MAX_ATTENDEES,
            "attendees": [attendee.body() for attendee in self.attendees],
        }

    def __str__(self) -> str:
        string = ""
        string += f"ID: {self.id}\n"
        string += f"Name | Summary: {self.event_name}\n"
        string += f"Description: {self.description}\n"
        string += f"Time: {self.time}\n"
        string += f"Address-Name: {self.address.name}\n"
        string += f"Address-Street: {self.address.street}\n"
        string += f"Address-Suburb: {self.address.suburb}\n"
        string += f"Address-State: {self.address.state}\n"
        string += f"Address-Postcode: {self.address.postcode}\n"
        string += f"Attendees: {self.attendees}\n"
        return string


if __name__ == "__main__":
    print(generate_id())

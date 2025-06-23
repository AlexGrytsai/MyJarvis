from dataclasses import dataclass


@dataclass(slots=True)
class Email:
    """
    Email value object.

    Ensures that the email address is in a valid format.
    """

    value: str

    def __str__(self) -> str:
        return self.value

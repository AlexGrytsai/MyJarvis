import re
from dataclasses import dataclass

from src.myjarvis.domain.exceptions import EmailNotValid


@dataclass(frozen=True, slots=True)
class Email:
    """
    Email value object.

    Ensures that the email address is in a valid format.
    """

    value: str

    def __post_init__(self) -> None:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.value):
            raise EmailNotValid("Email is not valid")

    def __str__(self) -> str:
        return self.value

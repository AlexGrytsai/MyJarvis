"""Commands Package.

This package contains all the commands that modify the state of the system.
Following the CQRS pattern, commands are responsible for changing data and
do not return any data.

Each file in this module should represent a single command and contain a data
structure (e.g., a Pydantic model or a dataclass) that holds the necessary
information to execute that command.
"""

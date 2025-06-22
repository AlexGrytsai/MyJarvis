"""Queries Package.

This package contains all the queries that retrieve data from the system without
altering its state. Following the CQRS pattern, queries are responsible for reading
data and should not have any side effects.

Each file in this module should represent a single query and contain a data structure
(e.g., a Pydantic model or a dataclass) that holds the parameters for that query.
The query handlers will return Data Transfer Objects (DTOs) defined in the
`application.dto` package.
"""

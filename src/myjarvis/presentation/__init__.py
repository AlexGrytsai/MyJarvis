"""
This package contains the presentation layer of the MyJarvis application.

The presentation layer is responsible for handling user interactions and presenting
data to the user. It is the entry point for all external requests and is responsible
for translating them into application-specific commands and queries.

This layer is composed of three main sub-packages:
- `api`: Contains the API endpoints for the application.
- `middleware`: Contains custom middleware for handling requests.
- `schemas`: Contains Pydantic schemas for data validation and serialization.

The presentation layer interacts with the application layer to execute business
logic and retrieve data. It should not contain any business logic itself and
should be kept as thin as possible.
"""

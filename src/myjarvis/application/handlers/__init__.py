"""Handlers Package.

This package is responsible for handling the application's commands and queries.
It acts as the intermediary that receives requests from the presentation layer (in
the form of command or query objects) and executes the appropriate business logic.

- `command_handlers.py`: Contains handlers for all commands that modify system state.
- `query_handlers.py`: Contains handlers for all queries that read system state.

Handlers orchestrate the workflow of a use case. They typically use repositories to
retrieve domain entities, invoke methods on those entities or on domain services,
and then use repositories to persist any changes. For queries, they fetch data and
map it to DTOs.
"""

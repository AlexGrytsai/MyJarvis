"""Application Layer.

This layer orchestrates the application's use cases. It does not contain any business
logic but rather coordinates the domain objects to perform the required tasks. It's the
entry point for the presentation layer to interact with the domain.

It uses the Command and Query Responsibility Segregation (CQRS) pattern to separate
read and write operations.
"""

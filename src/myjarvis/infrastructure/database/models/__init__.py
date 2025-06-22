"""SQLAlchemy ORM models.

This package contains the SQLAlchemy models that map to the database tables.
Each module in this package defines a class that represents a table in the database.
These models are used by the repository implementations to interact with the database.

A declarative base should be defined (e.g., in a shared `base.py` or within `session.py`)
and all models in this package should inherit from it. This allows Alembic to discover
the models for database migrations.
""" 
"""
This package contains the Pydantic schemas for the MyJarvis application.

Pydantic schemas are used for data validation, serialization, and documentation.
They define the expected structure and types of data for API requests and
responses.

Using schemas ensures that the data flowing into and out of the application is
well-formed and consistent. They are a crucial part of building a robust and
maintainable API with FastAPI.

This package is organized by feature, with each module containing the schemas
related to a specific domain entity or feature:
- `agent_schemas.py`: Schemas for AI agents.
- `node_schemas.py`: Schemas for nodes.
- `chat_schemas.py`: Schemas for chat messages.
""" 
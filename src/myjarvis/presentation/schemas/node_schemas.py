"""
This module will contain the Pydantic schemas for node-related data.

These schemas will be used to represent nodes in API responses, providing clients
with information about the available services that can be attached to agents.

Implementation Details:
- Create a `NodeRead` schema for representing nodes.
  - It will include fields like `id`, `name`, `description`, `node_type`, and
    a list of `commands` that the node can execute.
  - This schema will be used when listing all available nodes.

Example:
    from pydantic import BaseModel, Field
    from uuid import UUID

    class NodeRead(BaseModel):
        id: UUID
        name: str = Field(..., min_length=1, max_length=100)
        description: str
        node_type: str
        commands: list[str]

        class Config:
            from_attributes = True
""" 
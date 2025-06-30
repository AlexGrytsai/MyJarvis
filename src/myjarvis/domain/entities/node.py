"""
This module defines the Node entity.

A Node represents an external tool or service that an AIAgent can interact
with, such as Google Docs, a database, or a search engine. Each Node has a
description of its capabilities and a set of commands it can execute. This
information helps the LLM decide which tool to use for a given task.

Implementation details:
- It should have fields like `node_id`, `name`, `description`, a list of
  `commands`, and `node_type` (e.g., 'API', 'Database').
- The `commands` should be well-defined, perhaps as a list of objects, each
  with a name, description, and parameter schema.
- The entity should have methods to validate its configuration.
"""


class Node:
    pass

"""
This module will contain the API endpoints for managing nodes.

Nodes are the services that can be attached to AI agents, such as Google Docs,
Email, Calendar, etc. This module will provide a way to list available nodes.
Direct management of nodes (creation, update, deletion) might be an
administrative task and not exposed to regular users.

Implementation Details:
- Create a FastAPI `APIRouter` for nodes.
- Implement the following endpoint:
  - `GET /nodes/`: Get a list of all available nodes in the system.
    - Output: A list of `NodeRead` schemas.
    - This will likely call a `GetAllNodesHandler` or a similar query handler
      in the application layer, which needs to be created. This handler will
      retrieve all available node types from a registry or the database.
- Use the dependency injection system to get the required handlers.
- Use the schemas from `src/myjarvis/presentation/schemas/node_schemas.py` for
  response validation.
"""

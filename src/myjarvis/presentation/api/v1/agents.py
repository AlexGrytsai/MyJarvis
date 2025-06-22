"""
This module will contain the API endpoints for managing AI agents.

It will provide CRUD (Create, Read, Update, Delete) functionality for AI agents,
allowing users to create new agents, retrieve information about existing agents,
update their properties, and delete them.

Implementation Details:
- Create a FastAPI `APIRouter` for agents.
- Implement the following endpoints:
  - `POST /agents/`: Create a new AI agent.
    - Input: `AgentCreate` schema.
    - Output: `AgentRead` schema.
    - It will call the `CreateAgentHandler` from the application layer.
  - `GET /agents/`: Get a list of all AI agents for the authenticated user.
    - Output: A list of `AgentRead` schemas.
    - It will call the `GetUserAgentsHandler` from the application layer.
  - `GET /agents/{agent_id}`: Get a specific AI agent by its ID.
    - Input: `agent_id` path parameter.
    - Output: `AgentRead` schema.
    - It will call the `GetAgentHandler` from the application layer.
  - `PUT /agents/{agent_id}`: Update an AI agent.
    - Input: `agent_id` path parameter and `AgentUpdate` schema.
    - Output: `AgentRead` schema.
    - This will require a new `UpdateAgentHandler` in the application layer.
  - `DELETE /agents/{agent_id}`: Delete an AI agent.
    - Input: `agent_id` path parameter.
    - Output: A success message.
    - This will require a new `DeleteAgentHandler` in the application layer.
  - `POST /agents/{agent_id}/nodes/{node_id}`: Attach a node to an agent.
    - Input: `agent_id` and `node_id` path parameters.
    - Output: A success message.
    - It will call the `AttachNodeHandler` from the application layer.
- Use the dependency injection system to get the required handlers.
- Use the schemas from `src/myjarvis/presentation/schemas/agent_schemas.py`
  for request and response validation.
""" 
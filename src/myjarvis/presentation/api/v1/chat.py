"""
This module will contain the API endpoints for interacting with AI agents.

It will provide a way for users to send messages to their AI agents and receive
responses. This is the core interactive part of the application.

Implementation Details:
- Create a FastAPI `APIRouter` for chat.
- Implement the following endpoint:
  - `POST /chat/{agent_id}`: Send a message to an AI agent.
    - Input: `agent_id` path parameter and a `ChatMessage` schema containing
      the message content.
    - Output: A `ChatMessage` schema containing the agent's response.
    - This endpoint will call the `SendMessageHandler` from the application
      layer.
    - It should handle both regular and streaming responses. For streaming,
      a WebSocket or Server-Sent Events (SSE) endpoint could be used.
      - `POST /chat/{agent_id}/stream`: For streaming responses.
- Use the dependency injection system to get the `SendMessageHandler`.
- Use the schemas from `src/myjarvis/presentation/schemas/chat_schemas.py` for
  request and response validation.
""" 
"""
This module will contain the Pydantic schemas for chat-related data.

These schemas will define the structure of messages sent between the user and
the AI agents.

Implementation Details:
- Create a `ChatMessageCreate` schema for the user's incoming message.
  - It should contain the message `content` (string).
- Create a `ChatMessageRead` schema for the agent's response.
  - It should contain the `content` of the response and could also include
    metadata, such as the `sender` (`user` or `agent`).

Example:
    from pydantic import BaseModel, Field

    class ChatMessageCreate(BaseModel):
        content: str = Field(..., min_length=1)

    class ChatMessageRead(BaseModel):
        content: str
        sender: str # "user" or "agent"
"""

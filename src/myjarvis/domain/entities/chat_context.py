"""
This module defines the ChatContext entity.

The ChatContext entity is responsible for storing the history of a conversation
between a user and an AI agent. It maintains a list of messages, allowing the
agent to have a memory of previous interactions.

Implementation details:
- The class can be a Pydantic BaseModel.
- It should contain fields like `context_id`, `agent_id`, `messages`, and
  `created_at`.
- The `messages` field should be a list of `Message` value objects.
- It should have methods to manage the conversation, such as `add_message` and
  `clear_context`.
- It might also include logic for truncating the context to fit within the
  LLM's context window size.
"""

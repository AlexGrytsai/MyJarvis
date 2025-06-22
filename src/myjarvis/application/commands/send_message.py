"""Send Message Command.

This module defines the command for sending a message to an AI agent and getting a
response. This is a primary interaction command within the system.

Implementation Details:
-----------------------
This file should contain a Pydantic model or a dataclass named `SendMessageCommand`
that encapsulates the data required for the interaction.

`SendMessageCommand` should include:
- `agent_id`: The ID of the agent to which the message is sent.
- `user_id`: The ID of the user sending the message.
- `message_text`: The content of the user's message.
- `chat_context_id`: (Optional) The ID of an existing chat context to continue a
  conversation. If not provided, a new context might be created.

The handler, `SendMessageHandler`, will be complex. It will:
1.  Retrieve the agent, its nodes, and the chat context.
2.  Use the `AgentService` from the domain layer to process the message.
3.  The service will interact with the configured LLM, providing the base prompt,
    chat history, and available tools (from the attached nodes).
4.  The LLM's response will be processed and returned.
5.  The chat context will be updated with the new messages.

Note: While this command causes a change (updating chat context), it also needs to
return a value (the AI's response). This is a common exception to the "commands
don't return data" rule in CQRS for practical reasons.
"""

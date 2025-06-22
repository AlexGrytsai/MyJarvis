"""
This module defines the AgentService.

The AgentService contains domain logic that involves the AIAgent but does not
naturally belong to the AIAgent entity itself. This could include complex
interactions between an agent, its nodes, and the LLM.

For example, a primary responsibility of this service could be to process an
incoming message: receive the user input, format a prompt using the agent's
configuration and chat history, interact with the selected LLM, interpret the
LLM's response (e.g., a tool-use request), and execute commands on the
appropriate nodes.

Implementation details:
- The service should be stateless.
- It will depend on repository interfaces to fetch domain entities and on
  abstract interfaces for external systems like LLMs.
- It might have a method like `process_message(agent: AIAgent,
  user_message: Message) -> Message`.
"""

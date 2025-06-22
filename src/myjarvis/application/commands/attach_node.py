"""Attach Node Command.

This module defines the command for attaching a Node (a tool or service) to an existing
AI agent. This command is part of the Application layer and follows the CQRS pattern.

Implementation Details:
-----------------------
This file should contain a Pydantic model or a dataclass named `AttachNodeCommand`
that encapsulates the data required to attach a node.

`AttachNodeCommand` should include:
- `agent_id`: The ID of the agent to which the node will be attached.
- `node_id`: The ID of the node to attach.
- `user_id`: The ID of the user performing the action, for authorization purposes.

The handler for this command, `AttachNodeHandler`, will be located in the
`application.handlers.command_handlers` module. It will receive this command object,
validate that the user owns the agent, find the agent and the node entities, and then
call a domain service or a method on the agent entity to perform the attachment.
"""

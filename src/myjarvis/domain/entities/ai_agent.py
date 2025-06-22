"""
This module defines the AIAgent entity.

The AIAgent is a core entity of the domain. It represents an AI agent that can
be created by a User. Each agent has a specific configuration, including a base
prompt, a selected LLM model, and a set of connected Nodes (tools) that it can
use.

Implementation details:
- The class should be a Pydantic BaseModel for data validation.
- It should include fields like `agent_id`, `user_id`, `name`, `base_prompt`,
  `llm_model`, `created_at`, and a list of `node_ids`.
- It should contain business logic methods such as `attach_node`,
  `detach_node`, `update_prompt`, etc.
- The entity should ensure its invariants, for example, an agent cannot have
  duplicate nodes.
"""

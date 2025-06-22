"""
This module defines the NodeService.

The NodeService is responsible for domain logic related to nodes that does not
fit within the Node entity itself. This might include operations for managing
the lifecycle of nodes or for discovering available node types from a central
registry.

While most of the node interaction logic will be handled by the `AgentService`
(interpreting LLM requests to use a tool), this service can handle broader,
node-specific administrative tasks.

Implementation details:
- The service will be stateless.
- It could have methods like `get_available_node_types()` or
  `validate_node_configuration(node: Node)`.
"""

"""
This module defines the base interface for all Nodes.

A Node is an external service that an AI Agent can interact with. To ensure
consistency and interchangeability, all specific node implementations must
inherit from the `BaseNode` abstract class defined in this module.

The `BaseNode` class enforces the implementation of two key methods:
- `execute_command`: To run a specific command on the node.
- `get_available_commands`: To list all commands supported by the node.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseNode(ABC):
    """
    Abstract base class for all Node implementations.

    This class defines the common interface that all nodes must adhere to,
    allowing the system to interact with different services (like Google Docs,
    email, etc.) in a uniform way.
    """

    @abstractmethod
    def execute_command(
        self, command: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a specific command on the node.

        Args:
            command: The name of the command to execute.
            params: A dictionary of parameters required for the command.

        Returns:
            A dictionary containing the result of the command execution.
            The structure of the result will depend on the command.
        """
        pass

    @abstractmethod
    def get_available_commands(self) -> List[str]:
        """
        Get a list of available commands for this node.

        This method helps the LLM understand what actions it can perform
        with this node.

        Returns:
            A list of strings, where each string is a command name.
        """
        pass

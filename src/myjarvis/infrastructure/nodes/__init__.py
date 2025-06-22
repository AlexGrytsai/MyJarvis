"""
This package contains implementations of various "Nodes".

Nodes are external services that an AI Agent can interact with, such as
Google Docs, Email, Calendar, Search services, etc. Each node implementation
encapsulates the logic for connecting to and interacting with its respective
service, providing a standardized interface for the Application layer.

Each node must inherit from the `BaseNode` abstract class and implement its
methods to ensure consistent behavior across all nodes.
""" 
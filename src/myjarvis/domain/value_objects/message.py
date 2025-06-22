"""
This module defines the Message value object.

A Message represents a single entry in a chat context, containing the content
of the message, who sent it (user or agent), and when it was sent.

Implementation details:
- The class should be a Pydantic BaseModel and immutable (`frozen=True`).
- It should contain fields like `content` (str), `sender` (e.g., an Enum
  'USER' | 'AGENT'), and `timestamp` (datetime).
- This object is part of the ChatContext entity.
"""

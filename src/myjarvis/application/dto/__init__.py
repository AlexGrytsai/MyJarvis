"""Data Transfer Objects (DTOs) Package.

This package contains Data Transfer Objects. DTOs are simple objects that are used
to transfer data between layers, particularly between the Application and Presentation
layers.

They help to decouple the infrastructure (e.g., API schemas) from the domain model,
preventing the exposure of internal domain entities to the outside world. They carry
data and have no behavior.

DTOs in this package will typically be defined using Pydantic models to ensure
data validation and serialization.
"""

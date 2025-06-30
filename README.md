# MyJarvis

> **Note:** This project is currently under active development. The core domain model for the `User`, `AIAgent`, and `ChatContext` aggregates and the basic project structure are in place.

## About The Project

MyJarvis is a service for creating AI agents with access to a variety of tools and services, referred to as "Nodes". Users can create multiple AI agents, each customized with a unique base prompt, a specific LLM (like OpenAI, Anthropic, Gemini), and a set of connected Nodes.

Each AI agent (AIAgent) is a core domain entity that:
- Belongs to a specific User (user_id)
- Has a unique identifier (AgentId), name, and description
- Stores a base prompt and selected LLM model (LlmModel)
- Maintains a list of connected Nodes (node_ids)
- Supports updating name, description, prompt, and LLM model
- Allows attaching and detaching Nodes (tools)
- Tracks creation, update, and (soft) deletion timestamps
- Supports soft delete and restore operations

**ChatContext** is a core domain entity that:
- Manages the message history between a user and an agent
- Stores limits for chat history (max messages, max tokens, timeout)
- Supports adding, updating, removing, restoring, and clearing messages
- Handles partial removal and expiration of messages based on timeout
- Encapsulates business logic for message operations via MessageOperationsService and MessageCollection
- Allows updating chat limits dynamically

These Nodes can include:
- Google Docs
- Email services
- Google Calendar
- Search engines
- Vector databases
- And more.

A simple agent might function as a basic chatbot without any connected Nodes, while more complex agents can leverage these tools to perform sophisticated tasks. Agents can also maintain chat context history, enabling more stateful and intelligent conversations.

The project is built following the principles of Domain-Driven Design (DDD) and SOLID to ensure a clean, scalable, and maintainable architecture.

## Tech Stack

- **Backend:** Python 3.13, FastAPI
- **ORM:** SQLAlchemy, Alembic
- **Database:** PostgreSQL (planned)
- **Cache:** Redis
- **Authentication:** Firebase
- **Containerization:** Docker, Docker Compose
- **LLM Integrations:** OpenAI, Anthropic, Google Gemini
- **Tooling:** Pydantic, Pytest, Black, Flake8, Mypy

## Architecture

The project follows a layered architecture inspired by Domain-Driven Design:

- **Domain Layer:** Contains the core business logic, entities, value objects, and domain services. This layer is the heart of the application and has no dependencies on other layers. The AIAgent entity encapsulates agent configuration, node management, and lifecycle operations (update, soft delete, restore). The ChatContext entity manages chat history, message operations, and chat limits.
- **Application Layer:** Orchestrates the use cases of the application. It uses commands and queries to interact with the domain layer but does not contain business logic itself.
- **Infrastructure Layer:** Implements external concerns like database access, third-party API integrations (Nodes, LLMs), caching, etc. It provides concrete implementations for the interfaces defined in the domain layer (e.g., Repositories).
- **Presentation Layer:** Exposes the application's functionality through an API (e.g., REST API with FastAPI). It handles HTTP requests, serialization, and user authentication.

## Project Structure

```
MyJarvis/
├── src/
│   └── myjarvis/
│       ├── domain/         # Domain entities (User, AIAgent, ChatContext, Node), value objects, business logic
│       ├── application/
│       ├── infrastructure/
│       └── presentation/
├── tests/
├── migrations/
├── docker/
├── scripts/
├── config/
└── main.py
```

A more detailed structure can be found in `detailed_plan.md`.

## Roadmap

The project development is planned in several stages:
1.  **Environment & Core Infrastructure Setup**
2.  **Domain Layer Implementation**
    - [x] `User` Aggregate (Entity, Value Objects, Repository Interface).
    - [x] `AIAgent` and `Node` Aggregates.
    - [x] `ChatContext` Entity (message history, limits, operations).
3.  **Application Layer Implementation**
4.  **Database & Persistence (Infrastructure)**
5.  **Node System Implementation (Infrastructure)**
6.  **LLM Provider Integrations (Infrastructure)**
7.  **Cache & External Services (Infrastructure)**
8.  **Presentation Layer (API)**
9.  **Testing (Unit, Integration, E2E)**
    - [x] Unit tests for domain layer (`User`, `AIAgent`, `ChatContext`, `MessageOperationsService`, etc.)
    - [ ] Integration tests for persistence layer.
    - [ ] E2E tests for API endpoints.
10. **DevOps & Deployment**

## Getting Started

> Instructions for setting up and running the project locally will be added soon. The primary method for running the application will be via Docker.

```sh
# Clone the repository
git clone https://github.com/AlexGrytsai/MyJarvis.git

# Navigate to the project directory
cd MyJarvis

# Build and run with Docker Compose (example)
docker-compose up --build
```

## License

Distributed under the MIT License. See `LICENSE` for more information. (A `LICENSE` file will be added later). 
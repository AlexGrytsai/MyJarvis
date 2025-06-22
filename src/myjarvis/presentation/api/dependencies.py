"""
This module will contain dependency injection providers for the API.

Dependency injection is a key principle of the Clean Architecture, and it is used
to decouple the different layers of the application. This module will provide
the dependencies required by the API endpoints, such as repositories, services,
and use case handlers.

Implementation Details:
- Define provider functions for each dependency (e.g., `get_user_repository`).
- Use FastAPI's `Depends` function to inject the dependencies into the route
  handlers.
- Initialize dependencies such as database sessions, repositories, and
  application service handlers here.

Example:
    from typing import Annotated
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from myjarvis.application.services import AgentService
    from myjarvis.infrastructure.database.session import get_db_session
    from myjarvis.infrastructure.database.repositories import (
        SQLAlchemyAgentRepository
    )

    def get_agent_service(
        session: Session = Depends(get_db_session)
    ) -> AgentService:
        repo = SQLAlchemyAgentRepository(session)
        return AgentService(agent_repository=repo)

    AgentServiceDep = Annotated[AgentService, Depends(get_agent_service)]
""" 
"""
This module will implement the authentication middleware.

The authentication middleware is responsible for verifying the user's identity
before allowing them to access protected endpoints. It will inspect the request
for authentication credentials, such as a JWT token, and validate them.

Implementation Details:
- The middleware will be implemented as a FastAPI middleware function or class.
- It will extract the authentication token from the `Authorization` header.
- The token will be decoded and validated. Initially, this will be integrated
  with Firebase Auth.
- If the token is valid, the middleware will extract the user information
  (e.g., user ID) and attach it to the request state (`request.state.user`).
  This will make the user information available to the dependency injection
  system and the route handlers.
- If the token is invalid or missing, the middleware will return a 401
  Unauthorized or 403 Forbidden response.
- A dependency will be created (e.g., `get_current_user`) that reads the user
  from the request state, ensuring that the user is authenticated for protected
  routes.

Example:
    from fastapi import Request, HTTPException
    from starlette.middleware.base import BaseHTTPMiddleware
    from myjarvis.infrastructure.external.firebase_auth import verify_firebase_token

    class AuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                user_data = verify_firebase_token(token)
                if user_data:
                    request.state.user = user_data
                    response = await call_next(request)
                    return response
            raise HTTPException(status_code=401, detail="Not authenticated")
""" 
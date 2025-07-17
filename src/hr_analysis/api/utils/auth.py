"""API utility functions (e.g., authentication) for HR Analytics API."""

def authenticate_user(token: str) -> bool:
    """Dummy authentication utility."""
    return token == "valid-token"

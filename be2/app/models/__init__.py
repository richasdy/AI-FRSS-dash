"""
Models package
"""
try:
    from .auth import User, get_admin_by_username, add_admin
    __all__ = ["User", "get_admin_by_username", "add_admin"]
except ImportError as e:
    print(f"Warning: Could not import auth models: {e}")
    __all__ = []

try:
    from .faces import *
except ImportError:
    pass  # faces module optional


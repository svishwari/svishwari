"""Generic resource factory with caching and its common instances."""

from typing import Callable, Any


class ResourceFactory:  # pylint: disable=too-few-public-methods
    """Resource factory."""

    def __init__(self, get_resource_method: Callable):
        """Initialization

        Args:
            get_resource_method (Callable): method to get resource.
        """
        self.resource = None
        self.get_resource_method = get_resource_method

    def get_resource(self, *args, **kwargs) -> Any:
        """Get resource. Instantiate the resource if called first
        time and cache it.
        Args:
            *args (object): resource arguments.
            **kwargs (dict): resource keyword arguments.
        Returns:
            Any: Cached resource.
        """
        if not self.resource:
            self.resource = self.get_resource_method(*args, **kwargs)
        return self.resource

    def reset_resource(self):
        """Uncache resource."""
        self.resource = None

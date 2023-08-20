import inspect
from ..configuration import config

class AdaptersManager:
    """
    Manager for a set of adapters, synchronized with a configuration variable.
    Used directly as interface with the selected adapter, manager methods become
    adapter methods.

    Deal with functions or classes adapters.

    Usage exemple:
    >>> manager = AdaptersManager(adapters)
    >>> manager.adapter_method(...)
    >>> manager(args for an adapter call)
    """
    def __init__(self, adapters, config_var=None):
        self._adapters_list = adapters
        self._adapter = None
        self._selected = None
        self._config_var = config_var

        # Require an existing adapter as default.
        default = getattr(config, self._config_var)
        self.select(default)

    def select(self, name, *args, **kwargs):
        """
        Change the adapter used by the manager, with the ability to pass
        arguments for the instantiation of an adapter class.
        """
        name = name.lower()
        if name not in self._adapters_list:
            raise Exception(f"Adapter: '{name}' not in {self.options}.")

        config(**{self._config_var: name})
        self._selected = name
        self._adapter = self._adapters_list[name]
        if inspect.isclass(self._adapter):
            self._adapter = self._adapter(*args, **kwargs)

    @property
    def options(self):
        """ Find available adapters. """
        return set(self._adapters_list.keys())

    def _use_adapter(self):
        configured_adapter = getattr(config, self._config_var)
        if configured_adapter != self._selected:
            self.select(configured_adapter)
        return self._adapter

    def __getattr__(self, *args, **kwargs):
        return self._use_adapter().__getattribute__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._use_adapter().__call__(*args, **kwargs)

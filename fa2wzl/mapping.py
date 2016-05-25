from fa2wzl import exceptions


class MappedAttributeState(object):
    def __init__(self):
        self.loaded = False
        self.value = None


class MappedAttribute(object):
    """Class that manages attributes that are lazily loaded from somewhere.
    """

    def __init__(self, load_func):
        """Create a mapped attribute.

        Args:
            load_func: Callable that populates this attribute
        """
        self._load_func = load_func

    def _get_attribute_state(self, instance):
        if not hasattr(instance, "_attr_state"):
            setattr(instance, "_attr_state", {})

        if self not in instance._attr_state:
            instance._attr_state[self] = MappedAttributeState()

        return instance._attr_state[self]

    def __get__(self, instance, owner):
        state = self._get_attribute_state(instance)

        if not state.loaded:
            self._load_func(instance)

        if not state.loaded:
            raise exceptions.ScraperError()

        return state.value

    def __set__(self, instance, value):
        state = self._get_attribute_state(instance)
        state.loaded = True
        state.value = value

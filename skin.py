import copy


__all__ = ("Skin",)
__version__ = "0.0.2"
version = tuple(map(int, __version__.split(".")))


class SkinValueError(ValueError):
    pass


ANY = object()
FORBIDDEN = (str, bytes, bytearray, memoryview, range)
DEFAULT_VALUE = object()


class Skin:

    def __init__(self, value=DEFAULT_VALUE, *, allowed=ANY, forbidden=FORBIDDEN, parent=None):
        if value is DEFAULT_VALUE:
            value = {}
        if not hasattr(value, "__getitem__"):
            raise SkinValueError("{!r} have no '__getitem__' method".format(value))
        if allowed is not ANY and not isinstance(value, allowed):
            raise SkinValueError("{!r} not in allowed".format(value))
        if forbidden is ANY or isinstance(value, forbidden):
            raise SkinValueError("{!r} in forbidden".format(value))
        if isinstance(value, self.__class__):
            value = value.value
        super().__setattr__("value", value)
        config = dict(parent=parent, allowed=allowed, forbidden=forbidden)
        super().__setattr__("_skin_config", config)

    def __getattr__(self, name):
        if hasattr(self.value, name):
            return getattr(self.value, name)
        return self[name]

    def __getitem__(self, name):
        try:
            return self.__class__(self.value[name])
        except SkinValueError:
            return self.value[name]
        except (KeyError, IndexError):
            config = self._skin_config.copy()
            config["parent"] = (self, name)
            return self.__class__({}, **config)

    def __setattr__(self, name, value):
        if hasattr(self.value, name):
            setattr(self.value, name, value)
        else:
            self[name] = value

    def __setitem__(self, name, value):
        self.value[name] = value
        if self._skin_config["parent"] is not None:
            skin, parent_name = self._skin_config["parent"]
            skin[parent_name] = self.value

    def __delattr__(self, name):
        if hasattr(self.value, name):
            delattr(self.value, name)
        else:
            del self[name]

    def __delitem__(self, name):
        del self.value[name]

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.value)

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __reversed__(self):
        return reversed(self.value)

    def __contains__(self, item):
        return item in self.value

    def __copy__(self):
        return Skin(copy.copy(self.value))

    def __deepcopy__(self, memo):
        return Skin(copy.deepcopy(self.value, memo))

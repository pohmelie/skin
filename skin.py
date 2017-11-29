import copy
import functools


__all__ = ("Skin",)
__version__ = "0.0.5"
version = tuple(map(int, __version__.split(".")))


class SkinValueError(ValueError):
    pass


DEFAULT_VALUE = object()
ANY = object()
FORBIDDEN = (str, bytes, bytearray, memoryview, range)
TRANSPARENT_ATTRIBUTES = {"value", "__class__", "__deepcopy__"}


def _wrapper_or_value(self, value=DEFAULT_VALUE, *, parent=None, parent_name=None):
    try:
        cls = self.__class__
        getter = super(cls, self).__getattribute__
        return cls(value, allowed=getter("allowed"), forbidden=getter("forbidden"),
                   _parent=parent, _parent_name=parent_name)
    except SkinValueError:
        return value


class Skin:

    def __init__(self, value=DEFAULT_VALUE, *, allowed=ANY, forbidden=FORBIDDEN, _parent=None, _parent_name=None):
        if value is DEFAULT_VALUE:
            value = {}
        if isinstance(value, self.__class__):
            value = value.value
        else:
            if not hasattr(value, "__getitem__"):
                raise SkinValueError("{!r} have no '__getitem__' method".format(value))
            if allowed is not ANY and not isinstance(value, allowed):
                raise SkinValueError("{!r} not in allowed".format(value))
            if forbidden is ANY or isinstance(value, forbidden):
                raise SkinValueError("{!r} in forbidden".format(value))
        setter = super().__setattr__
        setter("value", value)
        setter("allowed", allowed)
        setter("forbidden", forbidden)
        setter("parent", _parent)
        setter("parent_name", _parent_name)

    def __getattribute__(self, name):
        if name not in TRANSPARENT_ATTRIBUTES:
            raise AttributeError
        return super().__getattribute__(name)

    def __getattr__(self, name):
        if hasattr(self.value, name):
            return getattr(self.value, name)
        return self[name]

    def __getitem__(self, name):
        try:
            return _wrapper_or_value(self, self.value[name])
        except (KeyError, IndexError):
            return _wrapper_or_value(self, parent=self, parent_name=name)

    def __setattr__(self, name, value):
        if hasattr(self.value, name):
            setattr(self.value, name, value)
        else:
            self[name] = value

    def __setitem__(self, name, value):
        self.value[name] = value
        getter = super().__getattribute__
        parent = getter("parent")
        if parent is not None:
            parent[getter("parent_name")] = self.value

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
        yield from map(functools.partial(_wrapper_or_value, self), self.value)

    def __reversed__(self):
        yield from map(functools.partial(_wrapper_or_value, self), reversed(self.value))

    def __contains__(self, item):
        return item in self.value

    def __copy__(self):
        return Skin(copy.copy(self.value))

    def __deepcopy__(self, memo):
        return Skin(copy.deepcopy(self.value, memo))

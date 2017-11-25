[![travis](https://img.shields.io/travis/pohmelie/suit.svg)](https://travis-ci.org/pohmelie/suit)
[![coveralls](https://img.shields.io/coveralls/pohmelie/suit.svg)](https://coveralls.io/github/pohmelie/suit)

# Suit
Getitem-objects «suit» for attribute-like access.

## Reason
[addict](https://github.com/mewwts/addict) and [python-box](https://github.com/cdgriffith/Box) do not respect `dict` reference transparency.
### addict
``` python
>>> from addict import Dict
>>> original = {"foo": [1, 2, 3]}
>>> d = Dict(original)
>>> d.foo
[1, 2, 3]
>>> type(d.foo)
<class 'list'>
>>> d.foo.append(4)
>>> original
{'foo': [1, 2, 3]}
>>> d.foo
[1, 2, 3, 4]
>>>
```
### python-box
``` python
>>> from box import Box
>>> original = {"foo": [1, 2, 3]}
>>> b = Box(original)
>>> b.foo
<BoxList: [1, 2, 3]>
>>> type(b.foo)
<class 'box.BoxList'>
>>> b.foo.append(4)
>>> original
{'foo': [1, 2, 3]}
>>> b.foo
<BoxList: [1, 2, 3, 4]>
>>>
```
### suit
``` python
>>> from suit import Suit
>>> original = {"foo": [1, 2, 3]}
>>> s = Suit(original)
>>> s.foo
Suit([1, 2, 3])
>>> type(s.foo)
<class 'suit.Suit'>
>>> type(s.foo.value)
<class 'list'>
>>> s.foo.value is original["foo"]
True
>>> s.foo.append(4)
>>> original
{'foo': [1, 2, 3, 4]}
>>>
```
# Documentation
``` python
Suit(value=DEFAULT_VALUE, *, allowed=ANY, forbidden=FORBIDDEN)
```
* value — any object with `__getitem__` method (default: `dict`).
* allowed — tuple of allowed types to wrap or `suit.ANY` for all types allowed (default: `suit.ANY`)
* forbidden — tuple of forbidden types to wrap (default: `(str, bytes, bytearray, memoryview, range)`)

What is `allowed` and `forbidden`?

Since suit target is not to recreate containers there should be a rule to determine is object container or endpoint-node. Some objects (listed above as `forbidden`) have `__getitem__` method, but wont act like containers.

Example:
You have original dictionary `{"foo": "bar"}`, and you expect from suit that `Suit({"foo": "bar"}).foo` is `"bar"` string, not suit wrapper. But, `str`, `bytes`, etc. have `__getitiem__` method. That is why there is `allowed` and `forbidden` tuples. I hope defaults are enough for 99% usecases.
In general: if `value` have no `__getitem__` or not allowed or forbidden you will get `SuitValueError` exception, which suit catches to determine if object can be wrapped.

Suit class have two hardcoded attributes:
* `value` — original object, which suit wraps
* `_suit_config` — some suit internals

Suit supports both "item" and "attribute" notations:
``` python
>>> s = Suit({"foo": "bar"})
>>> s.foo is s["foo"]
True
>>>
```
But, in case of nested containers:
``` python
>>> s = Suit({"foo": {"bar": "baz"}})
>>> s.foo is s["foo"]
False
>>> s.foo.value is s["foo"].value
True
>>>
```
Suit use strict order to find "items":
* in case of attribute access:
    * suit attribute
    * value attribute
    * value item
    * orphan item
* in case of item access:
    * value item
    * orphan item

Orphan item is just naming for item, which is not yet set. Example:
``` python
>>> s = Suit()
>>> s.foo.bar
Suit({})
>>> s
Suit({})
>>>
```

As you can see there is no "foo" or "bar" items. But in case of setting:
``` python
>>> s = Suit()
>>> s.foo.bar = "baz"
>>> s
Suit({'foo': {'bar': 'baz'}})
>>>
```
Since suit is just wrapper, which do not recreate container you can use any object with `__getitem__`:
``` python
>>> import collections
>>> s = Suit(collections.defaultdict(list))
>>> s.foo.append(1)
>>> s
Suit(defaultdict(<class 'list'>, {'foo': [1]}))
>>>
```

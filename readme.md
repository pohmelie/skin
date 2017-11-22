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
# Usage
The main goal of `suit` is to modify original object and don't recreate container. Think of `suit` as a way to reach original object «nodes». Any object, which have `__getitem__` can be used with attribute access:
``` python
>>> l = [1, 2, 3]
>>> s = Suit(l)
>>> s
Suit([1, 2, 3])
>>> s.value
[1, 2, 3]
>>> s[0]
1
>>> s.append(4)
>>> s
Suit([1, 2, 3, 4])
>>> l
[1, 2, 3, 4]
>>>
```
``` python
>>> import collections
>>> o = collections.defaultdict(list)
>>> d = Dict(o)
>>> d.bar.append(0)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
    d.bar.append(0)
TypeError: 'Dict' object is not callable
>>> o
defaultdict(<class 'list'>, {})
>>> s = Suit(o)
>>> s.foo
Suit([])
>>> s.foo.append(0)
>>> s
Suit(defaultdict(<class 'list'>, {'foo': [0]}))
>>> o
defaultdict(<class 'list'>, {'foo': [0]})
>>>
```
`suit` acts like object it wraps with exception of missed attributes access (which converts to item access) and pair of suit-state attributes:
* `value`: original object, which current instance of `Suit` holds.
* `_suit_config`: `Suit` state for `allowed`, `forbidden` and `parents` info.

More documentation comming soon... also check out `suit.py` and `tests.py`, since `Suit` is extremely small.

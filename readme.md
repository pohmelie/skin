[![travis](https://img.shields.io/travis/pohmelie/skin.svg)](https://travis-ci.org/pohmelie/skin)
[![coveralls](https://img.shields.io/coveralls/pohmelie/skin.svg)](https://coveralls.io/github/pohmelie/skin)
[![pypi](https://img.shields.io/pypi/v/skin.svg)](https://pypi.python.org/pypi/skin)

# Skin
Getitem-objects «skin» for attribute-like access.

## Reason
[addict](https://github.com/mewwts/addict), [python-box](https://github.com/cdgriffith/Box), [tri.struct](https://github.com/TriOptima/tri.struct), [dotmap](https://github.com/drgrib/dotmap), [ddict](https://github.com/rbehzadan/ddict), [easydict](https://github.com/makinacorpus/easydict) do not respect `dict` reference transparency.
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
### skin
``` python
>>> from skin import Skin
>>> original = {"foo": [1, 2, 3]}
>>> s = Skin(original)
>>> s.foo
Skin([1, 2, 3])
>>> type(s.foo)
<class 'skin.Skin'>
>>> type(s.foo.value)
<class 'list'>
>>> s.foo.value is original["foo"]
True
>>> s.foo.append(4)
>>> original
{'foo': [1, 2, 3, 4]}
>>>
```
# Similar projects
* [addict](https://github.com/mewwts/addict)
* [python-box](https://github.com/cdgriffith/Box)
* [tri.struct](https://github.com/TriOptima/tri.struct)
* [dotmap](https://github.com/drgrib/dotmap)
* [ddict](https://github.com/rbehzadan/ddict)
* [easydict](https://github.com/makinacorpus/easydict)
* [dot_access](https://github.com/kootenpv/dot_access)

And much more, since some of them are python 2 only.

# Benchmark (v0.0.5)

||Skin (skin)|Dict (addict)|DotMap (dotmap)|DotAccessDict (ddict)|Box (box)|EasyDict (easydict)|Dot (dot_access)|
|---|---|---|---|---|---|---|---|
|Create from `dict`|1.1x|9.3x|11.1x|9.2x|4.7x|11.2x|1.0x|
|Create from key-word arguments|-|1.8x|1.0x|1.5x|2.6x|1.9x|-|
|Get exist element|48.6x|7.9x|7.3x|6.8x|136.6x|1.0x|25.4x|
|Get non-exist element|2.5x|1.0x|1.4x|1.2x|-|-|1.3x|
|Set exist element|14.2x|2.9x|2.2x|2.6x|43.8x|1.0x|-|
|Set non-exist element|2.4x|1.4x|1.1x|1.0x|-|-|-|
|Support `items` iteration|-|3.0x|3.7x|2.7x|42.1x|1.0x|-|
|Support `values` iteration|-|3.8x|3.8x|3.1x|50.6x|1.0x|-|
|Support `len`|19.7x|4.7x|4.2x|4.2x|83.3x|1.0x|-|
|Support `copy`|1.8x|1.0x|-|-|-|-|-|
|Support `deepcopy`|2.7x|1.1x|1.0x|-|4.1x|1.7x|-|
|Wrapped modification affect original|1.0x|-|-|-|-|-|-|
|Original modification affect wrapped|2.0x|-|-|-|-|-|1.0x|
|`defaultdict` as original|1.0x|-|-|-|-|-|-|
|Non-dict as original|1.9x|-|-|-|-|-|1.0x|

`items` and `values` support mean that values of iteration will be wrapped too.

# Documentation
``` python
Skin(value=DEFAULT_VALUE, *, allowed=ANY, forbidden=FORBIDDEN)
```
* value — any object with `__getitem__` method (default: `dict`).
* allowed — tuple of allowed types to wrap or `skin.ANY` for all types allowed (default: `skin.ANY`)
* forbidden — tuple of forbidden types to wrap (default: `(str, bytes, bytearray, memoryview, range)`)

What is `allowed` and `forbidden`?

Since skin target is not to recreate containers there should be a rule to determine is object container or endpoint-node. Some objects (listed above as `forbidden`) have `__getitem__` method, but wont act like containers.

Example:
You have original dictionary `{"foo": "bar"}`, and you expect from skin that `Skin({"foo": "bar"}).foo` is `"bar"` string, not skin wrapper. But, `str`, `bytes`, etc. have `__getitiem__` method. That is why there is `allowed` and `forbidden` tuples. I hope defaults are enough for 99% usecases.
In general: if `value` have no `__getitem__` or not allowed or forbidden you will get `SkinValueError` exception, which skin catches to determine if object can be wrapped.

**Skin class have only one accessible attribute: `value` — original object, which skin wraps** :tada:

Skin supports both "item" and "attribute" notations:
``` python
>>> s = Skin({"foo": "bar"})
>>> s.foo is s["foo"]
True
>>>
```
But, in case of nested containers:
``` python
>>> s = Skin({"foo": {"bar": "baz"}})
>>> s.foo is s["foo"]
False
>>> s.foo.value is s["foo"].value
True
>>>
```
Both objects `s.foo` and `s["foo"]` is instances of `Skin`, but since they are created dynamicaly they are not the same object.

Skin use strict order to find "items":
* in case of attribute access:
    * skin attribute
    * value attribute
    * value item
    * orphan item
* in case of item access:
    * value item
    * orphan item

Orphan item is just naming for item, which is not yet set. Example:
``` python
>>> s = Skin()
>>> s.foo.bar
Skin({})
>>> s
Skin({})
>>>
```

As you can see there is no "foo" or "bar" items. But in case of setting:
``` python
>>> s = Skin()
>>> s.foo.bar = "baz"
>>> s
Skin({'foo': {'bar': 'baz'}})
>>>
```
Since skin is just wrapper, which do not recreate container you can use any object with `__getitem__`:
``` python
>>> import collections
>>> s = Skin(collections.defaultdict(list))
>>> s.foo.append(1)
>>> s
Skin(defaultdict(<class 'list'>, {'foo': [1]}))
>>>
```

# Benchmark (v0.0.5)
``` text
Create instance:
  Box            0.7227337849326432
  Dict           0.8247780610108748
  Skin           0.14907896996010095
  tri.struct     0.014445346896536648
Access exist:
  dict           0.005448702024295926
  Box            0.32549735193606466
  Dict           0.21359142300207168
  Skin           1.5485703510930762
Access non-exist:
  Dict           0.2847607780713588
  Skin           1.007843557978049
```

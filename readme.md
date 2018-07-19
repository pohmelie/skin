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

# Benchmark

||Skin (skin)|Dict (addict)|DotMap (dotmap)|DotAccessDict (ddict)|Box (box)|EasyDict (easydict)|Dot (dot_access)|dict (builtins)|
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Create from `dict`|4.0x|37.0x|45.5x|37.1x|19.0x|44.6x|4.2x|1.0x|
|Create from key-word arguments|-|11.1x|6.4x|9.4x|16.3x|11.7x|-|1.0x|
|Get exist element (attribute access)|33.6x|7.7x|7.1x|6.5x|132.4x|1.0x|25.4x|-|
|Get exist element (item access)|31.1x|5.5x|3.7x|2.0x|154.1x|2.1x|26.8x|1.0x|
|Get non-exist element (attribute access)|1.8x|1.0x|1.4x|1.2x|-|-|1.3x|-|
|Get non-exist element (item access)|1.6x|1.0x|1.4x|-|-|-|1.2x|-|
|Set exist element (attribute access)|10.6x|3.0x|2.3x|2.5x|47.7x|1.0x|-|-|
|Set exist element (item access)|29.0x|6.7x|3.9x|4.2x|164.6x|4.6x|-|1.0x|
|Set non-exist element (attribute access)|1.6x|1.3x|1.0x|1.0x|-|-|-|-|
|Set non-exist element (item access)|1.5x|1.3x|1.0x|-|-|-|-|-|
|Support `items` iteration|-|2.9x|3.8x|2.7x|40.5x|1.0x|-|-|
|Support `values` iteration|-|3.9x|4.2x|3.6x|59.3x|1.0x|-|-|
|Support `len`|13.9x|4.7x|4.3x|4.1x|80.5x|1.0x|-|-|
|Support `copy`|1.3x|1.0x|-|-|-|-|-|-|
|Support `deepcopy`|2.1x|1.1x|1.0x|-|3.8x|1.6x|-|-|
|Wrapped modification affect original|1.0x|-|-|-|-|-|-|-|
|Original modification affect wrapped|1.3x|-|-|-|-|-|1.0x|-|
|`defaultdict` as original|1.0x|-|-|-|-|-|-|-|
|Non-dict as original|1.3x|-|-|-|-|-|1.0x|-|

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
You have original dictionary `{"foo": "bar"}`, and you expect from skin that `Skin({"foo": "bar"}).foo` is `"bar"` string, not skin wrapper. But, `str`, `bytes`, etc. have `__getitiem__` method. That is why there is `allowed` and `forbidden` tuples. I hope defaults are good enough for 99% usecases.
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

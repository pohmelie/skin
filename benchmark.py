import timeit


setup = """
from box import Box
from addict import Dict
from skin import Skin

o = {"foo": {"bar": [0, 1, {"baz": "value"}]}}
b = Box(o)
d = Dict(o)
s = Skin(o)
"""

print("Create instance:")
print("\t[Box]:\t", timeit.timeit("Box(o)", setup=setup))
print("\t[Dict]:\t", timeit.timeit("Dict(o)", setup=setup))
print("\t[Skin]:\t", timeit.timeit("Skin(o)", setup=setup))

print("Access exist:")
print("\t[dict]:\t", timeit.timeit("o['foo']['bar'][-1]['baz']", setup=setup))
print("\t[Box]:\t", timeit.timeit("b.foo.bar[-1].baz", setup=setup))
print("\t[Dict]:\t", timeit.timeit("d.foo.bar[-1].baz", setup=setup))
print("\t[Skin]:\t", timeit.timeit("s.foo.bar[-1].baz", setup=setup))

print("Access non-exist:")
print("\t[Dict]\t", timeit.timeit("d.one.two.three = 1", setup=setup))
print("\t[Skin]\t", timeit.timeit("s.one.two.three = 1", setup=setup))

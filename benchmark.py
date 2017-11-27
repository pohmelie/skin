import timeit


SETUP = """
from box import Box
from addict import Dict
from skin import Skin
from tri.struct import Struct

o = {"foo": {"bar": [0, 1, {"baz": "value"}]}}
b = Box(o)
d = Dict(o)
s = Skin(o)
st = Struct(o)
"""


def run(title, stmt, fmt="  {:<15}{}", count=10 ** 5, setup=SETUP):
    print(fmt.format(title, timeit.timeit(stmt, setup=setup, number=count)))


print("Create instance:")
run("Box", "Box(o)")
run("Dict", "Dict(o)")
run("Skin", "Skin(o)")
run("tri.struct", "Struct(o)")

print("Access exist:")
run("dict", "o['foo']['bar'][-1]['baz']")
run("Box", "b.foo.bar[-1].baz")
run("Dict", "d.foo.bar[-1].baz")
run("Skin", "s.foo.bar[-1].baz")

print("Access non-exist:")
run("Dict", "d.one.two.three = 1")
run("Skin", "s.one.two.three = 1")

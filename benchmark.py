import time
import copy
import collections
import importlib


def generate_available_wrappers():
    for name, module in WRAPPER_NAMES:
        try:
            yield getattr(importlib.import_module(module), name)
        except ImportError:
            print("Can't import {} from {}".format(name, module))


WRAPPER_NAMES = (
    ("Box", "box"),
    ("Dict", "addict"),
    ("Struct", "tri.struct"),
    ("DotMap", "dotmap"),
    ("DotAccessDict", "ddict"),
    ("EasyDict", "easydict"),
    ("Dot", "dot_access"),
    ("Skin", "skin"),
)
WRAPPERS = tuple(generate_available_wrappers())
COUNT = 10 ** 4
ORIGINAL = {
    "foo": {
        "bar": [
            0,
            1,
            {
                "baz": "value",
                "foo": {
                    "bar": [
                        0,
                        1,
                        {
                            "baz": "value"
                        }
                    ]
                }
            }
        ]
    }
}


class Timer:

    def __enter__(self):
        self.t = time.perf_counter()
        return self

    def __exit__(self, *exc_info):
        self.t = time.perf_counter() - self.t


def create_from_dict(original, wrapper):
    with Timer() as timer:
        wrapper(original)
    return timer.t


def create_from_kwargs(original, wrapper):
    with Timer() as timer:
        wrapper(a=1, b=[1, 2, 3])
    return timer.t


def get_exist_element(original, wrapper):
    w = wrapper(original)
    with Timer() as timer:
        assert w.foo.bar[-1].foo.bar[2].baz == "value", "Wrong node value"
    return timer.t


def get_non_exist_element(original, wrapper):
    w = wrapper(original)
    with Timer() as timer:
        w.one.two.three
    return timer.t


def set_exist_element(original, wrapper):
    w = wrapper(original)
    with Timer() as timer:
        w.foo.bar[-1].foo.bar[2].baz = 1
    assert w.foo.bar[-1].foo.bar[2].baz == 1, "Wrong node value"
    return timer.t


def set_non_exist_element(original, wrapper):
    w = wrapper(original)
    with Timer() as timer:
        w.one.two.three = 1
    assert w.one.two.three == 1, "Wrong node value"
    return timer.t


def support_items_iteration(original, wrapper):
    w = wrapper({"foo": {"bar": 1}, "bar": {"bar": 1}})
    with Timer() as timer:
        for k, v in w.items():
            assert isinstance(k, str), "Key is not string"
            assert v.bar == 1, "Iterated value is not wrapped"
    return timer.t


def support_values_iteration(original, wrapper):
    w = wrapper({"foo": {"bar": 1}, "bar": {"bar": 1}})
    with Timer() as timer:
        for v in w.values():
            assert v.bar == 1, "Iterated value is not wrapped"
    return timer.t


def support_len(original, wrapper):
    w = wrapper(original)
    with Timer() as timer:
        assert len(w.foo.bar) == 3, "Length is wrong"
    return timer.t


def support_copy(original, wrapper):
    w = wrapper({"foo": [1, 2, 3]})
    with Timer() as timer:
        nw = copy.copy(w)
        nw.foo.append(4)
        assert w.foo[-1] == 4, "Need 4, got {}".format(w.foo[-1])
    return timer.t


def support_deepcopy(original, wrapper):
    w = wrapper({"foo": [1, 2, 3]})
    with Timer() as timer:
        nw = copy.deepcopy(w)
        nw.foo.append(4)
        assert w.foo[-1] == 3, "Need 3, got {}".format(w.foo[-1])
    return timer.t


def wrapped_modification_affect_original(original, wrapper):
    w = wrapper(original)
    assert original["foo"]["bar"][-1]["foo"]["bar"][2]["baz"] != 1, "Wrong original value"
    with Timer() as timer:
        w.foo.bar[-1].foo.bar[2].baz = 1
    assert original["foo"]["bar"][-1]["foo"]["bar"][2]["baz"] == 1, "Wrong node value"
    return timer.t


def original_modification_affect_wrapped(original, wrapper):
    w = wrapper(original)
    assert original["foo"]["bar"][-1]["foo"]["bar"][2]["baz"] != 1, "Wrong original value"
    with Timer() as timer:
        assert w.foo.bar[-1].foo.bar[2].baz == "value"
        original["foo"]["bar"][-1]["foo"]["bar"][2]["baz"] = 1
        assert w.foo.bar[-1].foo.bar[2].baz == 1, "Wrong node value"
    return timer.t


def third_as_original(original, wrapper):
    w = wrapper(collections.defaultdict(list))
    with Timer() as timer:
        w.foo.append(1)
    return timer.t


def non_dict_as_original(original, wrapper):
    w = wrapper([{"foo": "bar"}, {"bar": "foo"}])
    with Timer() as timer:
        assert w[0].foo == "bar", "Need 'bar', got {!r}".format(w[0].foo)
        assert w[1].bar == "foo", "Need 'foo', got {!r}".format(w[1].foo)
    return timer.t


BENCHMAKRS = (
    ("Create from `dict`", create_from_dict),
    ("Create from key-word arguments", create_from_kwargs),
    ("Get exist element", get_exist_element),
    ("Get non-exist element", get_non_exist_element),
    ("Set exist element", set_exist_element),
    ("Set non-exist element", set_non_exist_element),
    ("Support `items` iteration", support_items_iteration),
    ("Support `values` iteration", support_values_iteration),
    ("Support `len`", support_len),
    ("Support `copy`", support_copy),
    ("Support `deepcopy`", support_deepcopy),
    ("Wrapped modification affect original", wrapped_modification_affect_original),
    ("Original modification affect wrapped", original_modification_affect_wrapped),
    ("`defaultdict` as original", third_as_original),
    ("Non-dict as original", non_dict_as_original),
)


table = collections.defaultdict(list)
for title, bench in BENCHMAKRS:
    print(title)
    for wrapper in WRAPPERS:
        try:
            total = 0
            for _ in range(COUNT):
                total += bench(copy.deepcopy(ORIGINAL), wrapper)
            result = "[+] {:.3f}".format(total)
        except Exception as e:
            total = "-"
            result = "[-] {}".format(e)
        table[wrapper.__name__].append(total)
        print("  {:<15}{}".format(wrapper.__name__, result))
columns = sorted(table.items(), key=lambda p: sum(isinstance(t, float) for t in p[1]), reverse=True)
head, columns = zip(*columns)
rows = list(zip(*columns))
print("Markdown table:")
module_by_name = dict(WRAPPER_NAMES)
row = ["{} ({})".format(name, module_by_name[name]) for name in head]
print("|".join(["", ""] + row + [""]))
print("|-" * len(BENCHMAKRS) + "|")
for (title, _), row in zip(BENCHMAKRS, rows):
    values = []
    fastest = min(v for v in row if isinstance(v, float))
    for v in row:
        if isinstance(v, float):
            values.append("{:.1f}x".format(v / fastest))
        else:
            values.append(v)
    print("|".join(["", title] + values + [""]))

# bag-multiset

A tiny multiset library: a bag that tracks how many times each element has been inserted, with `insert`, `remove`, and `count` operations.

## Usage

```python
from bag_multiset import Bag, BagError

bag = Bag(["apple", "apple", "banana"])
bag.insert("apple")
bag.remove("banana")

assert bag.count("apple") == 3
assert bag.count("banana") == 0

try:
    bag.remove("banana", times=2)
except BagError:
    pass  # removing more than is present raises
```

## Why this exists

When you need to count occurrences of hashable items and decrement them again, a plain `dict` is almost enough — except that you have to re-derive the "drop the key when it hits zero" rule everywhere, and you end up with ad-hoc `max(0, ...)` guards. This library is that rule, factored into one place, with a dedicated exception so callers can distinguish "not enough" from "wrong type entirely".

The trade-off: this is unordered. If your code cares about insertion order, use a list. The bag's `__iter__` yields each key once per its multiplicity, but the order is whatever Python's dict gives you — do not depend on it.

## Edge cases worth knowing

- `insert(x, times=0)` is a no-op, never raises. This lets `bag.insert(x, bag.count(y))` compose without a guard.
- `remove` raises `BagError` (a `ValueError` subclass) the moment it would push a multiplicity below zero. It does not silently clamp to zero, because that hides bugs in the caller.
- Keys must be hashable. Unhashable values raise `TypeError` at insert time, same as a normal dict lookup.
- `bool` is rejected for the `times` argument even though `isinstance(True, int)` is `True` in Python. Passing `True`/`False` for a count is almost always a bug.

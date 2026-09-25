"""A minimal multiset (bag) implementation.

A bag is an unordered collection that stores the multiplicity of each distinct
key rather than the keys themselves. We use a plain dict internally because:

  * it preserves no ordering guarantees, which keeps the semantics honest —
    callers cannot rely on iteration order and the tests should not either;
  * dict.get / __setitem__ are O(1) average, so insert/remove/count are all
    constant-time on average.

A separate guard class BagError is exported so callers can catch multiplicity
violations (removing more than is present, or asking for a key that was never
inserted) without matching the generic LookupError.
"""


class BagError(ValueError):
    """Raised when an operation would produce a negative multiplicity.

    Subclassing ValueError (rather than inventing a standalone base) keeps
    the exception catchable by code that only knows about the stdlib, while
    still letting library users filter on BagError specifically.
    """


class Bag:
    """An unordered multiset tracking element multiplicities."""

    __slots__ = ("_counts",)

    def __init__(self, iterable=None):
        # dict[str, int] -> key to positive multiplicity. We store only
        # positive counts; keys with zero multiplicity are deleted so that
        # iteration yields exactly the keys currently in the bag.
        self._counts = {}
        if iterable is not None:
            for item in iterable:
                self.insert(item)

    def insert(self, item, times=1):
        """Add ``item`` ``times`` times.

        ``times`` must be a non-negative int. Zero is a no-op rather than an
        error because it composes naturally: ``bag.insert(x, bag.count(y))``
        should never raise even when y is absent.
        """
        if not isinstance(times, int) or isinstance(times, bool):
            raise TypeError("times must be a non-negative int")
        if times < 0:
            raise ValueError("times must be non-negative")
        if times == 0:
            return
        self._counts[item] = self._counts.get(item, 0) + times

    def remove(self, item, times=1):
        """Remove ``item`` ``times`` times.

        Raises BagError if ``times`` exceeds the current multiplicity. We
        refuse to let a multiplicity go negative because that would silently
        make ``count`` return inconsistent values depending on history.
        """
        if not isinstance(times, int) or isinstance(times, bool):
            raise TypeError("times must be a non-negative int")
        if times < 0:
            raise ValueError("times must be non-negative")
        current = self._counts.get(item, 0)
        if times > current:
            raise BagError(
                f"cannot remove {times} of {item!r}; only {current} present"
            )
        remaining = current - times
        if remaining == 0:
            # Drop the key entirely so __contains__ and __iter__ reflect
            # reality. Keeping a zero entry would be a leaky abstraction.
            del self._counts[item]
        else:
            self._counts[item] = remaining

    def count(self, item):
        """Return the multiplicity of ``item`` (0 if absent)."""
        return self._counts.get(item, 0)

    def __contains__(self, item):
        return item in self._counts

    def __iter__(self):
        # Yield each key once per its multiplicity. Ordering is unspecified;
        # callers must not depend on it.
        for key, multiplicity in self._counts.items():
            for _ in range(multiplicity):
                yield key

    def __len__(self):
        # Total number of stored elements, not distinct keys. This matches
        # the intuition that ``len(bag) == sum(bag.count(k) for k in bag)``
        # when bag is iterated as keys-with-multiplicity.
        return sum(self._counts.values())

    def __eq__(self, other):
        if not isinstance(other, Bag):
            return NotImplemented
        return self._counts == other._counts

    def __repr__(self):
        return f"Bag({dict(self._counts)!r})"

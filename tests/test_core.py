import unittest

from bag_multiset import Bag, BagError


class TestBagInsert(unittest.TestCase):
    def test_insert_single(self):
        b = Bag()
        b.insert("a")
        self.assertEqual(b.count("a"), 1)

    def test_insert_repeated(self):
        b = Bag()
        b.insert("a")
        b.insert("a")
        b.insert("a")
        self.assertEqual(b.count("a"), 3)

    def test_insert_multiple_times(self):
        b = Bag()
        b.insert("a", times=4)
        self.assertEqual(b.count("a"), 4)

    def test_insert_zero_is_noop(self):
        b = Bag(["a"])
        b.insert("a", times=0)
        self.assertEqual(b.count("a"), 1)

    def test_insert_negative_raises(self):
        b = Bag()
        with self.assertRaises(ValueError):
            b.insert("a", times=-1)

    def test_insert_bool_rejected(self):
        b = Bag()
        with self.assertRaises(TypeError):
            b.insert("a", times=True)


class TestBagRemove(unittest.TestCase):
    def test_remove_partial(self):
        b = Bag(["a", "a", "a"])
        b.remove("a", times=2)
        self.assertEqual(b.count("a"), 1)
        self.assertIn("a", b)

    def test_remove_all_drops_key(self):
        b = Bag(["a", "a"])
        b.remove("a", times=2)
        self.assertEqual(b.count("a"), 0)
        self.assertNotIn("a", b)

    def test_remove_missing_raises(self):
        b = Bag()
        with self.assertRaises(BagError):
            b.remove("a")

    def test_remove_more_than_present_raises(self):
        b = Bag(["a", "a"])
        with self.assertRaises(BagError):
            b.remove("a", times=3)

    def test_remove_zero_is_noop(self):
        b = Bag(["a"])
        b.remove("a", times=0)
        self.assertEqual(b.count("a"), 1)

    def test_remove_negative_raises(self):
        b = Bag(["a"])
        with self.assertRaises(ValueError):
            b.remove("a", times=-1)

    def test_remove_bool_rejected(self):
        b = Bag(["a"])
        with self.assertRaises(TypeError):
            b.remove("a", times=False)


class TestBagCount(unittest.TestCase):
    def test_count_missing_is_zero(self):
        b = Bag()
        self.assertEqual(b.count("absent"), 0)

    def test_count_after_mixed_ops(self):
        b = Bag(["x", "x", "x"])
        b.remove("x")
        b.insert("x", times=2)
        self.assertEqual(b.count("x"), 4)


class TestBagIteration(unittest.TestCase):
    def test_iter_yields_each_occurrence(self):
        b = Bag(["a", "a", "b"])
        self.assertEqual(sorted(list(b)), ["a", "a", "b"])

    def test_iter_empty(self):
        b = Bag()
        self.assertEqual(list(b), [])


class TestBagLen(unittest.TestCase):
    def test_len_counts_multiplicities(self):
        b = Bag(["a", "a", "b"])
        self.assertEqual(len(b), 3)

    def test_len_after_removal(self):
        b = Bag(["a", "a", "a"])
        b.remove("a", times=2)
        self.assertEqual(len(b), 1)


class TestBagEquality(unittest.TestCase):
    def test_equal_bags(self):
        self.assertEqual(Bag(["a", "a", "b"]), Bag(["b", "a", "a"]))

    def test_unequal_bags(self):
        self.assertNotEqual(Bag(["a", "a"]), Bag(["a"]))

    def test_compare_with_non_bag(self):
        self.assertNotEqual(Bag(["a"]), ["a"])


class TestBagConstructor(unittest.TestCase):
    def test_construct_from_list(self):
        b = Bag([1, 2, 2, 3])
        self.assertEqual(b.count(2), 2)

    def test_construct_empty(self):
        b = Bag()
        self.assertEqual(len(b), 0)

    def test_construct_none_is_empty(self):
        b = Bag(None)
        self.assertEqual(len(b), 0)

    def test_unhashable_key_rejected(self):
        b = Bag()
        with self.assertRaises(TypeError):
            b.insert(["not", "hashable"])


if __name__ == "__main__":
    unittest.main()

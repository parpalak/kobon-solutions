import unittest
from decimal import Decimal

from verification.quick_check import (
    compare_realization,
    count_triangles,
    parse_lines,
    quick_rationalize,
    replay_word,
)


class QuickCheckTests(unittest.TestCase):
    def test_exact_simple_arrangement(self):
        structure = replay_word("0 1 0", 3)
        lines = parse_lines(
            {"lines": [[Decimal("2"), Decimal("0")], [Decimal("1"), Decimal("-1")], [Decimal("0"), Decimal("0")]]},
            3,
        )
        self.assertEqual(compare_realization(lines, structure), (True, ""))
        self.assertEqual(count_triangles(structure.rows), 1)

    def test_quick_rationalization_repairs_a_triple(self):
        structure = replay_word("0*", 3)
        lines = parse_lines(
            {"lines": [[Decimal("2"), Decimal("0")], [Decimal("1"), Decimal("0.001")], [Decimal("0"), Decimal("0")]]},
            3,
        )
        self.assertFalse(compare_realization(lines, structure)[0])
        repaired = quick_rationalize(lines, structure)
        self.assertEqual(compare_realization(repaired, structure), (True, ""))
        self.assertEqual(count_triangles(structure.rows), 0)

    def test_exact_parallel_pair(self):
        structure = replay_word("1 0", 3)
        lines = parse_lines(
            {"lines": [[Decimal("1"), Decimal("0")], [Decimal("1"), Decimal("1")], [Decimal("0"), Decimal("0")]]},
            3,
        )
        self.assertEqual(structure.parallel_pairs, frozenset({(0, 1)}))
        self.assertEqual(compare_realization(lines, structure), (True, ""))

    def test_wrong_crossing_order_is_not_accepted(self):
        structure = replay_word("0 1 0 2 1 0", 4)
        lines = parse_lines(
            {
                "lines": [
                    [Decimal("3"), Decimal("0")],
                    [Decimal("2"), Decimal("1")],
                    [Decimal("1"), Decimal("6")],
                    [Decimal("0"), Decimal("10")],
                ]
            },
            4,
        )
        self.assertFalse(compare_realization(lines, structure)[0])
        repaired = quick_rationalize(lines, structure)
        self.assertFalse(compare_realization(repaired, structure)[0])


if __name__ == "__main__":
    unittest.main()

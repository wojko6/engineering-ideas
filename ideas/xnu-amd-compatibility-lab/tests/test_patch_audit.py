"""Synthetic unit tests: these fixtures contain no Apple code or hardware logs."""
import unittest
from pathlib import Path
import importlib.util

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "audit_patches.py"
SPEC = importlib.util.spec_from_file_location("audit_patches", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class TestSafePatchPrimitives(unittest.TestCase):
    def test_exact_search_and_overlapping_matches(self):
        self.assertEqual(audit.search_masked(b"aaaa", 0, 4, b"aa"), [0, 1, 2])

    def test_masked_search(self):
        self.assertEqual(
            audit.search_masked(bytes.fromhex("aa32bb aa45bb"), 0, 6,
                                bytes.fromhex("aa00bb"), bytes.fromhex("ff00ff")),
            [0, 3],
        )

    def test_search_bounds(self):
        self.assertEqual(audit.search_masked(b"xxxabcabc", 3, 6, b"abc"), [3])
        self.assertEqual(audit.search_masked(b"xxxabcabc", 3, 6, b"abcdef"), [])

    def test_all_wildcards_and_errors(self):
        self.assertEqual(audit.search_masked(b"xyz", 0, 3, b"ab", b"\0\0"), [0, 1])
        with self.assertRaises(ValueError):
            audit.search_masked(b"a", 0, 1, b"")
        with self.assertRaises(ValueError):
            audit.search_masked(b"ab", 0, 2, b"ab", b"\xff")

    def test_replace_masked(self):
        self.assertEqual(
            audit.replace_masked(bytes.fromhex("f055"), bytes.fromhex("aa00"), bytes.fromhex("0f00")),
            bytes.fromhex("fa55"),
        )
        with self.assertRaises(ValueError):
            audit.replace_masked(b"a", b"abc")

    def test_identity_changes_with_base(self):
        p = {"Identifier": "kernel", "Base": "_function", "Find": b"abc", "Count": 1}
        q = dict(p, Base="_function ")
        self.assertNotEqual(audit.patch_identity(p), audit.patch_identity(q))
        self.assertEqual(audit.patch_identity(p), audit.patch_identity(dict(p)))

    def test_expected_macho_rejects_random_bytes(self):
        with self.assertRaises(ValueError):
            audit.MachO(b"not a Mach-O")

    def test_darwin_25_scope(self):
        p = {"Enabled": True, "MinKernel": "25.0.0", "MaxKernel": "25.99.99"}
        self.assertTrue(audit.enabled_on_25_7(p))
        self.assertFalse(audit.enabled_on_25_7(dict(p, MaxKernel="24.99.99")))
        self.assertFalse(audit.enabled_on_25_7(dict(p, Enabled=False)))


if __name__ == "__main__":
    unittest.main()

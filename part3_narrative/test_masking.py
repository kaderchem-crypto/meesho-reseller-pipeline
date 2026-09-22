import unittest

from part3_narrative.masking import alias_for, assert_no_raw_names_leak


class MaskingTests(unittest.TestCase):
    def test_alias_generation(self):
        self.assertEqual(alias_for("RS019"), "ALIAS-19")
        self.assertEqual(alias_for("RS006"), "ALIAS-06")

    def test_raw_name_leak_detection(self):
        raw_names = ["Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6"]
        safe_text = "Top performance was driven by ALIAS-19 in the West region."
        unsafe_text = "Top performance was driven by Mumbai Reseller 1 in the West region."

        self.assertTrue(assert_no_raw_names_leak(safe_text, raw_names))
        self.assertFalse(assert_no_raw_names_leak(unsafe_text, raw_names))

if __name__ == "__main__":
    unittest.main()
import unittest
from pathlib import Path

from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GrowthEngineTests(unittest.TestCase):
	def test_mom_growth_and_threshold_boundary(self):
		self.assertEqual(mom_growth(100, 108), 8.0)
		self.assertEqual(is_flagged(8.0), "escalate_exact_boundary")
		self.assertEqual(is_flagged(-8.01), "flagged")

	def test_valid_fixture_is_accepted(self):
		valid, errors = validate_feed(
			str(PROJECT_ROOT / "part2_engine" / "fixtures" / "monthly_category_revenue.csv")
		)
		self.assertTrue(valid)
		self.assertEqual(errors, [])

	def test_corrupted_fixture_is_rejected(self):
		valid, errors = validate_feed(
			str(PROJECT_ROOT / "part2_engine" / "fixtures" / "corrupted_feed.csv")
		)
		self.assertFalse(valid)
		self.assertGreaterEqual(len(errors), 3)


if __name__ == "__main__":
	unittest.main()

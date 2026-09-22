import csv
import tempfile
import unittest
from pathlib import Path

from part4_agent.mock_agent_runner import run


class MockAgentRunnerTests(unittest.TestCase):
    def test_caps_flagged_categories_and_holds_drafts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            previous_path = temp_path / "previous.csv"
            current_path = temp_path / "current.csv"
            headers = ["month", "category", "revenue", "n_orders"]

            with previous_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                for category in "ABCDE":
                    writer.writerow(["April", category, 100, 10])

            with current_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                for category, revenue in zip("ABCDE", [120, 115, 110, 109, 108]):
                    writer.writerow(["May", category, revenue, 10])

            result = run("May", str(previous_path), str(current_path))

        self.assertEqual(result["validation_status"], "valid")
        self.assertEqual(result["action_taken"], "drafted_and_held_for_approval")
        self.assertEqual(len(result["flagged_categories"]), 3)
        self.assertEqual(result["suppressed_categories"], ["D"])
        self.assertEqual(result["escalated_categories"], ["E"])


if __name__ == "__main__":
    unittest.main()
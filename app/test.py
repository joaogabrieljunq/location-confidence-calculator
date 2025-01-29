import unittest
import pandas as pd
from datetime import datetime
from calculate_confidence import calculate_confidence_for_interval


class TestCalculateConfidenceForInterval(unittest.TestCase):

    def setUp(self):
        # Sample dataset for testing
        self.data = pd.DataFrame(
            {
                "Local Date & Time": pd.date_range(
                    start="2021-01-05 20:00:00", periods=10, freq="H"
                ),
                "State": [
                    "New York",
                    "New York",
                    "Connecticut",
                    "New York",
                    "New York",
                    "Connecticut",
                    "Connecticut",
                    "New York",
                    "New York",
                    "New York",
                ],
            }
        )
        self.data["Local Date & Time"] = pd.to_datetime(self.data["Local Date & Time"])

    def test_valid_interval(self):
        start_time = datetime(2021, 1, 5, 20, 0, 0)
        end_time = datetime(2021, 1, 5, 23, 0, 0)
        result = calculate_confidence_for_interval(self.data, start_time, end_time)
        self.assertEqual(result["Dominant State"].iloc[0], "New York")
        self.assertGreater(result["Confidence (%)"].iloc[0], 50)

    def test_empty_interval(self):
        start_time = datetime(2022, 1, 1, 0, 0, 0)
        end_time = datetime(2022, 1, 1, 1, 0, 0)
        result = calculate_confidence_for_interval(self.data, start_time, end_time)
        self.assertTrue(result.empty)

    def test_boundary_overlap(self):
        start_time = datetime(2021, 1, 5, 20, 0, 0)
        end_time = datetime(2021, 1, 5, 21, 0, 0)
        result = calculate_confidence_for_interval(self.data, start_time, end_time)
        self.assertEqual(result["Dominant State"].iloc[0], "New York")
        self.assertEqual(result["Confidence (%)"].iloc[0], 100)

    def test_mixed_states(self):
        start_time = datetime(2021, 1, 5, 20, 0, 0)
        end_time = datetime(2021, 1, 5, 22, 0, 0)
        result = calculate_confidence_for_interval(self.data, start_time, end_time)
        self.assertEqual(result["Dominant State"].iloc[0], "New York")
        self.assertLess(result["Confidence (%)"].iloc[0], 100)

    def test_no_mode(self):
        # Create a dataset with no mode
        no_mode_data = pd.DataFrame(
            {
                "Local Date & Time": pd.date_range(
                    start="2021-01-05 20:00:00", periods=4, freq="H"
                ),
                "State": ["NY", "CT", "NJ", "CO"],
            }
        )
        no_mode_data["Local Date & Time"] = pd.to_datetime(
            no_mode_data["Local Date & Time"]
        )

        start_time = datetime(2021, 1, 5, 20, 0, 0)
        end_time = datetime(2021, 1, 5, 23, 0, 0)
        result = calculate_confidence_for_interval(no_mode_data, start_time, end_time)
        self.assertEqual(result["Dominant State"].iloc[0], "Unknown")


if __name__ == "__main__":
    unittest.main()

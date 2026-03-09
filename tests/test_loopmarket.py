import unittest
from io import StringIO
import sys

import loopmarket


class TestLoopMarket(unittest.TestCase):

    def test_total_stock_empty(self):
        self.assertEqual(loopmarket.total_stock_value([]), 0)

    def test_total_stock_single(self):
        self.assertEqual(loopmarket.total_stock_value([42]), 42)

    def test_total_stock_typical(self):
        self.assertEqual(loopmarket.total_stock_value([5, 12, 8, 0, 3]), 28)


    def test_student_discount_empty(self):
        self.assertEqual(loopmarket.student_discount_prices([]), [])

    def test_student_discount_basic(self):
        result = loopmarket.student_discount_prices([100, 250, 75])
        expected = ["R 80", "R 200", "R 60"]
        self.assertEqual(result, expected)

    def test_student_discount_rounding(self):
        # 20% off 199 → 159.2 → should round to nearest rand
        result = loopmarket.student_discount_prices([199])
        self.assertEqual(result, ["R 159"])


    def test_unlock_first_try(self):
        correct = "2580"
        input_data = correct + "\n"
        output = self._capture_output(lambda: loopmarket.try_unlock_phone(correct), input_data)
        self.assertIn("Access granted", output)
        self.assertNotIn("Wrong", output)

    def test_unlock_second_try(self):
        correct = "1995"
        input_data = "0000\n" + correct + "\n"
        output = self._capture_output(lambda: loopmarket.try_unlock_phone(correct), input_data)
        self.assertEqual(output.count("Enter PIN:"), 2)
        self.assertIn("Wrong PIN", output)
        self.assertIn("Access granted", output)

    def test_sunny_streak_empty(self):
        self.assertEqual(loopmarket.longest_sunny_streak([]), 0)

    def test_sunny_streak_all_sunny(self):
        self.assertEqual(loopmarket.longest_sunny_streak(["SUNNY"]*7), 7)

    def test_sunny_streak_mixed(self):
        log = ["CLOUDY", "SUNNY", "SUNNY", "RAIN", "SUNNY", "SUNNY", "SUNNY", "SUNNY", "CLOUDY"]
        self.assertEqual(loopmarket.longest_sunny_streak(log), 4)

    def test_hot_days_no_peaks(self):
        self.assertEqual(loopmarket.find_hot_days([20,21,22,23,24]), [])

    def test_hot_days_classic(self):
        temps = [28, 31, 29, 34, 32, 36, 33]
        self.assertEqual(loopmarket.find_hot_days(temps), [31, 34, 36])


    def test_id_validation(self):
        ids = [
            "9205135289081",   # valid length & digits
            "920513-589081",   # has hyphen → invalid
            "92051abc89081",   # letters → invalid
            "1234567890123",   # valid format
        ]
        result = loopmarket.check_id_numbers(ids)
        self.assertEqual(len(result["valid"]), 2)
        self.assertEqual(len(result["invalid"]), 2)

    def test_airtime_exact(self):
        msg = loopmarket.airtime_balance_alert(50, [10, 15, 25])
        self.assertIn("lasts all week", msg)
        self.assertIn("Remaining: R 0", msg)

    def test_airtime_runs_out(self):
        msg = loopmarket.airtime_balance_alert(45, [10, 15, 25, 5])
        self.assertIn("finished on day 3", msg)

    def test_airtime_already_empty(self):
        self.assertEqual(
            loopmarket.airtime_balance_alert(0, [5,5]),
            "No airtime to start with."
        )


    def _capture_output(self, func, input_str=""):
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_str)
        sys.stdout = captured = StringIO()
        try:
            func()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
        return captured.getvalue()


if __name__ == '__main__':
    unittest.main(verbosity=2)

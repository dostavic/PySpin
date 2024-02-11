import random
import unittest
from unittest.mock import patch

from main import deposit, get_number_of_lines, MAX_LINES, MIN_BET, get_bet, MAX_BET, get_slot_machine_spin, \
    check_winnings


class TestDeposit(unittest.TestCase):
    @patch('builtins.input', return_value='100')
    def test_deposit_positive_number(self, mock_input):
        """
        Test deposit with a positive number.
        """
        self.assertEqual(deposit(), 100)

    @patch('builtins.input', side_effect=['0', '100'])
    def test_deposit_zero_then_positive(self, mock_input):
        """
        Test deposit first with a zero input, which should not be accepted,
        and then with a valid positive number.
        """
        self.assertEqual(deposit(), 100)

    @patch('builtins.input', side_effect=['-1', '100'])
    def test_deposit_negative_then_positive(self, mock_input):
        """
        Test deposit first with a negative input, which should not be accepted,
        and then with a valid positive number.
        """
        self.assertEqual(deposit(), 100)

    @patch('builtins.input', side_effect=['not a number', '100'])
    def test_deposit_not_numeric_then_positive(self, mock_input):
        """
        Test deposit first with a non-numeric input, which should not be accepted,
        and then with a valid positive number.
        """
        self.assertEqual(deposit(), 100)


class TestGetNumberOfLines(unittest.TestCase):
    @patch('builtins.input', return_value='3')
    def test_valid_input(self, mock_input):
        """
        Test get_get_number_of_lines function with a valid input
        """
        self.assertEqual(get_number_of_lines(), 3)

    @patch('builtins.input', side_effect=['0', str(MAX_LINES)])
    def test_input_below_range_then_valid(self, mock_input):
        """
        Test get_get_number_of_lines function with an input below valid range
        followed by a valid input
        """
        self.assertEqual(get_number_of_lines(), MAX_LINES)

    @patch('builtins.input', side_effect=[str(MAX_LINES + 1), '1'])
    def test_input_above_range_then_valid(self, mock_input):
        """
        Test get_get_number_of_lines function with an input above valid range
        followed by a valid input
        """
        self.assertEqual(get_number_of_lines(), 1)

    @patch('builtins.input', side_effect=['non a number', '2'])
    def test_non_numeric_input_then_valid(self, mock_input):
        """
        Test get_get_number_of_lines function with a non_numeric input
        followed by a valid input
        """
        self.assertEqual(get_number_of_lines(), 2)


class TestGetBet(unittest.TestCase):
    @patch('builtins.input', return_value=str(MIN_BET))
    def test_input_at_min_bet(self, mock_input):
        """
        Test get_bet function with an input at the minimum bet limit.
        """
        self.assertEqual(get_bet(), MIN_BET)

    @patch('builtins.input', return_value=str(MAX_BET))
    def test_input_at_max_bet(self, mock_input):
        """
        Test get_bet function with an input at the minimum bet limit.
        """
        self.assertEqual(get_bet(), MAX_BET)

    @patch('builtins.input', side_effect=[str(MIN_BET - 1), str(MIN_BET)])
    def test_input_below_min_bet_then_valid(self, mock_input):
        """
        Test get_bet function with an input below the minimum bet limit followed by a valid input at minimum bet.
        """
        self.assertEqual(get_bet(), MIN_BET)

    @patch('builtins.input', side_effect=[str(MAX_BET + 1), str(MAX_BET)])
    def test_input_above_max_bet_then_valid(self, mock_input):
        """
        Test get_bet function with an input above the maximum bet limit followed by a valid input at maximum bet.
        """
        self.assertEqual(get_bet(), MAX_BET)

    @patch('builtins.input', side_effect=['not a number', str(MIN_BET)])
    def test_non_numeric_input_then_valid(self, mock_input):
        """
        Test get_bet function with a non-numeric input followed by a valid input at minimum bet.
        """
        self.assertEqual(get_bet(), MIN_BET)


class TestGetSlotMachineSpin(unittest.TestCase):
    def setUp(self):
        """
        Setup context for tests.
        """
        random.seed(42)
        self.rows = 3
        self.cols = 3
        self.symbols = {
            "A": 2,
            "B": 4,
            "C": 6,
            "D": 8
        }

    def test_dimensions(self):
        """
        Test the dimensions of the slot machine spin result.
        """
        result = get_slot_machine_spin(self.rows, self.cols, self.symbols)
        self.assertEqual(len(result), self.cols)
        for column in result:
            self.assertEqual(len(column), self.rows)


class TestCheckWinnings(unittest.TestCase):
    def setUp(self):
        """
        Setup context for tests.
        """
        self.values = {
            "A": 5,
            "B": 4,
            "C": 3,
            "D": 2
        }
        self.bet = 10

    def test_no_winnings(self):
        """
        Test that no winnings are calculated correctly.
        """
        columns = [
            ["A", "B", "C"],
            ["A", "C", "B"],
            ["C", "A", "B"]
        ]
        lines = 3
        winnings, winning_lines = check_winnings(columns, lines, self.bet, self.values)
        self.assertEqual(winnings, 0)
        self.assertEqual(winning_lines, [])

    def test_single_line_winning(self):
        """
        Test that are calculated correctly for a single winning line.
        """
        columns = [
            ["A", "A", "A"],
            ["A", "B", "C"],
            ["A", "B", "C"]
        ]
        lines = 1
        winnings, winning_lines = check_winnings(columns, lines, self.bet, self.values)
        self.assertEqual(winnings, self.values["A"] * self.bet)
        self.assertEqual(winning_lines, [1])

    def test_multiple_lines_winning(self):
        """
        Test that winnings are calculated correctly for multiple winning lines.
        """
        columns = [
            ["A", "A", "A"],
            ["A", "A", "A"],
            ["A", "A", "A"]
        ]
        lines = 3
        winnings, winning_lines = check_winnings(columns, lines, self.bet, self.values)
        self.assertEqual(winnings, self.values["A"] * self.bet * lines)
        self.assertEqual(winning_lines, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()

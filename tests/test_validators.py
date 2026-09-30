"""
Test cases for Validators module.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from validators import Validator


class TestValidator(unittest.TestCase):
    """Test cases for Validator class."""
    
    def setUp(self):
        self.validator = Validator()
    
    # Amount validation tests
    def test_valid_amount_positive_integer(self):
        valid, amount, error = self.validator.validate_amount("500")
        self.assertTrue(valid)
        self.assertEqual(amount, 500.0)
        self.assertEqual(error, "")
    
    def test_valid_amount_float(self):
        valid, amount, error = self.validator.validate_amount("450.50")
        self.assertTrue(valid)
        self.assertEqual(amount, 450.50)
    
    def test_valid_amount_with_whitespace(self):
        valid, amount, error = self.validator.validate_amount("  1000  ")
        self.assertTrue(valid)
        self.assertEqual(amount, 1000.0)
    
    def test_invalid_amount_negative(self):
        valid, amount, error = self.validator.validate_amount("-500")
        self.assertFalse(valid)
        self.assertIsNone(amount)
        self.assertIn("greater than zero", error)
    
    def test_invalid_amount_zero(self):
        valid, amount, error = self.validator.validate_amount("0")
        self.assertFalse(valid)
        self.assertIsNone(amount)
        self.assertIn("greater than zero", error)
    
    def test_invalid_amount_string(self):
        valid, amount, error = self.validator.validate_amount("abc")
        self.assertFalse(valid)
        self.assertIsNone(amount)
        self.assertIn("valid number", error)
    
    def test_invalid_amount_empty(self):
        valid, amount, error = self.validator.validate_amount("")
        self.assertFalse(valid)
        self.assertIsNone(amount)
        self.assertIn("empty", error)
    
    # Date validation tests
    def test_valid_date_format(self):
        valid, date, error = self.validator.validate_date("2026-09-30")
        self.assertTrue(valid)
        self.assertEqual(date, "2026-09-30")
    
    def test_valid_date_with_whitespace(self):
        valid, date, error = self.validator.validate_date("  2026-01-15  ")
        self.assertTrue(valid)
        self.assertEqual(date, "2026-01-15")
    
    def test_invalid_date_format_wrong_order(self):
        valid, date, error = self.validator.validate_date("30-09-2026")
        self.assertFalse(valid)
        self.assertIsNone(date)
        self.assertIn("YYYY-MM-DD", error)
    
    def test_invalid_date_format_slash(self):
        valid, date, error = self.validator.validate_date("2026/09/30")
        self.assertFalse(valid)
        self.assertIsNone(date)
    
    def test_invalid_date_nonexistent(self):
        valid, date, error = self.validator.validate_date("2026-02-30")
        self.assertFalse(valid)
        self.assertIsNone(date)
        self.assertIn("Invalid date", error)
    
    def test_invalid_date_empty(self):
        valid, date, error = self.validator.validate_date("")
        self.assertFalse(valid)
        self.assertIsNone(date)
        self.assertIn("empty", error)
    
    # Category validation tests
    def test_valid_expense_category_exact(self):
        valid, cat, error = self.validator.validate_category("Food", "expense")
        self.assertTrue(valid)
        self.assertEqual(cat, "Food")
    
    def test_valid_expense_category_case_insensitive(self):
        valid, cat, error = self.validator.validate_category("food", "expense")
        self.assertTrue(valid)
        self.assertEqual(cat, "Food")
    
    def test_valid_income_category(self):
        valid, cat, error = self.validator.validate_category("Salary", "income")
        self.assertTrue(valid)
        self.assertEqual(cat, "Salary")
    
    def test_custom_category_allowed(self):
        valid, cat, error = self.validator.validate_category("CustomCategory", "expense")
        self.assertTrue(valid)
        self.assertEqual(cat, "CustomCategory")
        self.assertIn("not a standard category", error)
    
    def test_invalid_category_empty(self):
        valid, cat, error = self.validator.validate_category("", "expense")
        self.assertFalse(valid)
        self.assertEqual(cat, "")
        self.assertIn("empty", error)
    
    # Description validation tests
    def test_valid_description(self):
        valid, desc, error = self.validator.validate_description("Test description")
        self.assertTrue(valid)
        self.assertEqual(desc, "Test description")
    
    def test_valid_empty_description(self):
        valid, desc, error = self.validator.validate_description("")
        self.assertTrue(valid)
        self.assertEqual(desc, "")
    
    def test_valid_none_description(self):
        valid, desc, error = self.validator.validate_description(None)
        self.assertTrue(valid)
        self.assertEqual(desc, "")
    
    # Menu choice validation tests
    def test_valid_menu_choice(self):
        valid, choice, error = self.validator.validate_menu_choice("1", ["1", "2", "3"])
        self.assertTrue(valid)
        self.assertEqual(choice, "1")
    
    def test_invalid_menu_choice(self):
        valid, choice, error = self.validator.validate_menu_choice("5", ["1", "2", "3"])
        self.assertFalse(valid)
        self.assertIn("Invalid option", error)
    
    def test_empty_menu_choice(self):
        valid, choice, error = self.validator.validate_menu_choice("", ["1", "2"])
        self.assertFalse(valid)
        self.assertIn("enter a menu option", error)
    
    # Transaction ID validation tests
    def test_valid_transaction_id(self):
        transactions = [{'id': 'EXP001'}, {'id': 'EXP002'}]
        valid, tid, error = self.validator.validate_transaction_id("EXP001", transactions)
        self.assertTrue(valid)
        self.assertEqual(tid, "EXP001")
    
    def test_valid_transaction_id_case_insensitive(self):
        transactions = [{'id': 'EXP001'}]
        valid, tid, error = self.validator.validate_transaction_id("exp001", transactions)
        self.assertTrue(valid)
        self.assertEqual(tid, "EXP001")
    
    def test_invalid_transaction_id_not_found(self):
        transactions = [{'id': 'EXP001'}]
        valid, tid, error = self.validator.validate_transaction_id("EXP999", transactions)
        self.assertFalse(valid)
        self.assertIn("not found", error)
    
    def test_invalid_transaction_id_empty(self):
        transactions = [{'id': 'EXP001'}]
        valid, tid, error = self.validator.validate_transaction_id("", transactions)
        self.assertFalse(valid)
        self.assertIn("empty", error)
    
    # Month validation tests
    def test_valid_month_format(self):
        valid, month, error = self.validator.validate_month("2026-09")
        self.assertTrue(valid)
        self.assertEqual(month, "2026-09")
    
    def test_empty_month_returns_current(self):
        valid, month, error = self.validator.validate_month("")
        self.assertTrue(valid)
        self.assertIsNotNone(month)
        # Should be current month in YYYY-MM format
        self.assertRegex(month, r"^\d{4}-\d{2}$")
    
    def test_invalid_month_format(self):
        valid, month, error = self.validator.validate_month("09-2026")
        self.assertFalse(valid)
        self.assertIsNone(month)
        self.assertIn("YYYY-MM", error)
    
    # Confirmation tests
    def test_confirmation_yes(self):
        self.assertTrue(self.validator.validate_confirmation("y"))
        self.assertTrue(self.validator.validate_confirmation("Y"))
        self.assertTrue(self.validator.validate_confirmation("yes"))
        self.assertTrue(self.validator.validate_confirmation("YES"))
    
    def test_confirmation_no(self):
        self.assertFalse(self.validator.validate_confirmation("n"))
        self.assertFalse(self.validator.validate_confirmation("no"))
        self.assertFalse(self.validator.validate_confirmation(""))


if __name__ == '__main__':
    unittest.main()
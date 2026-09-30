"""
Test cases for Budget Manager.
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage import Storage
from transaction_manager import TransactionManager
from budget_manager import BudgetManager


class TestBudgetManager(unittest.TestCase):
    """Test cases for Budget Manager."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = Storage(self.test_dir)
        self.tm = TransactionManager(self.storage)
        self.budget_mgr = BudgetManager(self.storage, self.tm)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_set_budget(self):
        """Test setting a budget."""
        success = self.budget_mgr.set_budget("2026-09", 20000.0)
        self.assertTrue(success)
        
        budget = self.budget_mgr.get_budget("2026-09")
        self.assertIsNotNone(budget)
        self.assertEqual(budget['amount'], 20000.0)
    
    def test_update_budget(self):
        """Test updating an existing budget."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        success = self.budget_mgr.set_budget("2026-09", 25000.0)
        self.assertTrue(success)
        
        budget = self.budget_mgr.get_budget("2026-09")
        self.assertEqual(budget['amount'], 25000.0)
    
    def test_get_budget(self):
        """Test getting budget for a month."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        
        budget = self.budget_mgr.get_budget("2026-09")
        self.assertIsNotNone(budget)
        self.assertEqual(budget['month'], '2026-09')
        self.assertEqual(budget['amount'], 20000.0)
    
    def test_get_nonexistent_budget(self):
        """Test getting budget for month without budget."""
        budget = self.budget_mgr.get_budget("2026-09")
        self.assertIsNone(budget)
    
    def test_delete_budget(self):
        """Test deleting a budget."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        success = self.budget_mgr.delete_budget("2026-09")
        self.assertTrue(success)
        
        budget = self.budget_mgr.get_budget("2026-09")
        self.assertIsNone(budget)
    
    def test_delete_nonexistent_budget(self):
        """Test deleting non-existent budget."""
        success = self.budget_mgr.delete_budget("2026-09")
        self.assertFalse(success)
    
    def test_budget_status_within_budget(self):
        """Test budget status when within budget."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        self.tm.add_expense("2026-09-30", 5000.0, "Food", "Groceries")
        self.tm.add_expense("2026-09-29", 3000.0, "Travel", "Transport")
        
        status = self.budget_mgr.calculate_budget_status("2026-09")
        
        self.assertTrue(status['has_budget'])
        self.assertEqual(status['budget_amount'], 20000.0)
        self.assertEqual(status['total_expenses'], 8000.0)
        self.assertEqual(status['remaining'], 12000.0)
        self.assertEqual(status['percentage_used'], 40.0)
        self.assertEqual(status['status'], 'WITHIN_BUDGET')
    
    def test_budget_status_warning_threshold(self):
        """Test budget status at warning threshold (80%)."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        self.tm.add_expense("2026-09-30", 16000.0, "Food", "Big expense")
        
        status = self.budget_mgr.calculate_budget_status("2026-09")
        
        self.assertEqual(status['percentage_used'], 80.0)
        self.assertEqual(status['status'], 'WARNING')
    
    def test_budget_status_exceeded(self):
        """Test budget status when exceeded."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        self.tm.add_expense("2026-09-30", 22000.0, "Shopping", "Over budget")
        
        status = self.budget_mgr.calculate_budget_status("2026-09")
        
        self.assertEqual(status['total_expenses'], 22000.0)
        self.assertEqual(status['remaining'], -2000.0)
        self.assertAlmostEqual(status['percentage_used'], 110.0, places=1)
        self.assertEqual(status['status'], 'EXCEEDED')
    
    def test_budget_status_no_budget(self):
        """Test budget status when no budget set."""
        self.tm.add_expense("2026-09-30", 5000.0, "Food", "Groceries")
        
        status = self.budget_mgr.calculate_budget_status("2026-09")
        
        self.assertFalse(status['has_budget'])
        self.assertIn('No budget', status['message'])
    
    def test_budget_alert(self):
        """Test budget alert check."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        self.tm.add_expense("2026-09-30", 5000.0, "Food", "Groceries")
        
        alert = self.budget_mgr.check_budget_alert("2026-09")
        self.assertIsNone(alert)
        
        # Add more expenses to trigger warning
        self.tm.add_expense("2026-09-29", 12000.0, "Travel", "Trip")
        alert = self.budget_mgr.check_budget_alert("2026-09")
        self.assertIsNotNone(alert)
        self.assertIn('WARNING', alert)
    
    def test_multiple_months_independent(self):
        """Test that budgets for different months are independent."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        self.budget_mgr.set_budget("2026-10", 25000.0)
        
        budget_sep = self.budget_mgr.get_budget("2026-09")
        budget_oct = self.budget_mgr.get_budget("2026-10")
        
        self.assertEqual(budget_sep['amount'], 20000.0)
        self.assertEqual(budget_oct['amount'], 25000.0)
        
        # Expenses in September shouldn't affect October budget
        self.tm.add_expense("2026-09-30", 15000.0, "Food", "Sep expense")
        
        status_sep = self.budget_mgr.calculate_budget_status("2026-09")
        status_oct = self.budget_mgr.calculate_budget_status("2026-10")
        
        self.assertEqual(status_sep['total_expenses'], 15000.0)
        self.assertEqual(status_oct['total_expenses'], 0.0)


if __name__ == '__main__':
    unittest.main()
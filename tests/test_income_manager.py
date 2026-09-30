"""
Test cases for Income Manager.
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
from income_manager import IncomeManager


class TestIncomeManager(unittest.TestCase):
    """Test cases for Income Manager."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = Storage(self.test_dir)
        self.tm = TransactionManager(self.storage)
        self.income_mgr = IncomeManager(self.tm)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_add_income(self):
        """Test adding income through income manager."""
        income = self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        
        self.assertIsNotNone(income)
        self.assertEqual(income['type'], 'income')
        self.assertEqual(income['amount'], 25000.0)
        self.assertEqual(income['category'], 'Salary')
        self.assertTrue(income['id'].startswith('INC'))
    
    def test_view_income(self):
        """Test viewing income list."""
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project work")
        
        income_list = self.tm.get_income()
        self.assertEqual(len(income_list), 2)
    
    def test_update_income(self):
        """Test updating income."""
        income = self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        income_id = income['id']
        
        success = self.tm.update_transaction(income_id, amount=26000.0, category="Freelance")
        self.assertTrue(success)
        
        updated = self.tm.get_transaction_by_id(income_id)
        self.assertEqual(updated['amount'], 26000.0)
        self.assertEqual(updated['category'], 'Freelance')
    
    def test_delete_income(self):
        """Test deleting income."""
        income = self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        income_id = income['id']
        
        success = self.tm.delete_transaction(income_id)
        self.assertTrue(success)
        
        found = self.tm.get_transaction_by_id(income_id)
        self.assertIsNone(found)
    
    def test_income_calculations(self):
        """Test income calculations."""
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project work")
        self.tm.add_income("2026-09-28", 1000.0, "Investment", "Dividends")
        
        total_income = self.tm.calculate_total_income()
        self.assertEqual(total_income, 31000.0)
        
        # Category totals
        totals = self.tm.get_category_totals('income')
        self.assertEqual(totals['Salary'], 25000.0)
        self.assertEqual(totals['Freelance'], 5000.0)
        self.assertEqual(totals['Investment'], 1000.0)


if __name__ == '__main__':
    unittest.main()
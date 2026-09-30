"""
Test cases for Expense Manager and Transaction Manager.
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
from validators import Validator


class TestExpenseManager(unittest.TestCase):
    """Test cases for Expense/Transaction Manager."""
    
    def setUp(self):
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.storage = Storage(self.test_dir)
        self.tm = TransactionManager(self.storage)
        self.validator = Validator()
    
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_add_expense(self):
        """Test adding an expense."""
        expense = self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        
        self.assertIsNotNone(expense)
        self.assertEqual(expense['type'], 'expense')
        self.assertEqual(expense['amount'], 450.0)
        self.assertEqual(expense['category'], 'Food')
        self.assertEqual(expense['description'], 'Dinner')
        self.assertTrue(expense['id'].startswith('EXP'))
    
    def test_add_income(self):
        """Test adding income."""
        income = self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        
        self.assertIsNotNone(income)
        self.assertEqual(income['type'], 'income')
        self.assertEqual(income['amount'], 25000.0)
        self.assertEqual(income['category'], 'Salary')
        self.assertTrue(income['id'].startswith('INC'))
    
    def test_get_all_transactions(self):
        """Test retrieving all transactions."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        
        transactions = self.tm.get_all_transactions()
        self.assertEqual(len(transactions), 2)
    
    def test_get_expenses_only(self):
        """Test getting only expenses."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        
        expenses = self.tm.get_expenses()
        self.assertEqual(len(expenses), 2)
        for e in expenses:
            self.assertEqual(e['type'], 'expense')
    
    def test_get_income_only(self):
        """Test getting only income."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project work")
        
        income = self.tm.get_income()
        self.assertEqual(len(income), 2)
        for i in income:
            self.assertEqual(i['type'], 'income')
    
    def test_get_transaction_by_id(self):
        """Test retrieving transaction by ID."""
        expense = self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        expense_id = expense['id']
        
        found = self.tm.get_transaction_by_id(expense_id)
        self.assertIsNotNone(found)
        self.assertEqual(found['id'], expense_id)
        
        # Test non-existent ID
        not_found = self.tm.get_transaction_by_id("EXP999")
        self.assertIsNone(not_found)
    
    def test_update_transaction(self):
        """Test updating a transaction."""
        expense = self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        expense_id = expense['id']
        
        # Update amount and category
        success = self.tm.update_transaction(expense_id, amount=500.0, category="Travel")
        self.assertTrue(success)
        
        updated = self.tm.get_transaction_by_id(expense_id)
        self.assertEqual(updated['amount'], 500.0)
        self.assertEqual(updated['category'], 'Travel')
        self.assertEqual(updated['description'], 'Dinner')  # Unchanged
    
    def test_update_nonexistent_transaction(self):
        """Test updating non-existent transaction."""
        success = self.tm.update_transaction("EXP999", amount=100.0)
        self.assertFalse(success)
    
    def test_delete_transaction(self):
        """Test deleting a transaction."""
        expense = self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        expense_id = expense['id']
        
        success = self.tm.delete_transaction(expense_id)
        self.assertTrue(success)
        
        # Verify deleted
        found = self.tm.get_transaction_by_id(expense_id)
        self.assertIsNone(found)
    
    def test_delete_nonexistent_transaction(self):
        """Test deleting non-existent transaction."""
        success = self.tm.delete_transaction("EXP999")
        self.assertFalse(success)
    
    def test_filter_by_type(self):
        """Test filtering by transaction type."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        
        expenses = self.tm.filter_transactions(transaction_type='expense')
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]['type'], 'expense')
        
        income = self.tm.filter_transactions(transaction_type='income')
        self.assertEqual(len(income), 1)
        self.assertEqual(income[0]['type'], 'income')
    
    def test_filter_by_category(self):
        """Test filtering by category."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_expense("2026-09-28", 200.0, "Food", "Lunch")
        
        food_expenses = self.tm.filter_transactions(transaction_type='expense', category='Food')
        self.assertEqual(len(food_expenses), 2)
        for e in food_expenses:
            self.assertEqual(e['category'], 'Food')
    
    def test_filter_by_date_range(self):
        """Test filtering by date range."""
        self.tm.add_expense("2026-09-01", 100.0, "Food", "Early month")
        self.tm.add_expense("2026-09-15", 200.0, "Food", "Mid month")
        self.tm.add_expense("2026-09-30", 300.0, "Food", "End month")
        
        # Filter for mid-month onwards
        filtered = self.tm.filter_transactions(
            transaction_type='expense',
            start_date='2026-09-15',
            end_date='2026-09-30'
        )
        self.assertEqual(len(filtered), 2)
    
    def test_filter_by_amount_range(self):
        """Test filtering by amount range."""
        self.tm.add_expense("2026-09-30", 100.0, "Food", "Small")
        self.tm.add_expense("2026-09-29", 500.0, "Travel", "Medium")
        self.tm.add_expense("2026-09-28", 1000.0, "Shopping", "Large")
        
        # Filter between 200 and 800
        filtered = self.tm.filter_transactions(
            transaction_type='expense',
            min_amount=200,
            max_amount=800
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['amount'], 500.0)
    
    def test_search_by_keyword(self):
        """Test searching by keyword in description."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner with friends")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare to work")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        
        results = self.tm.search_transactions("dinner")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['description'], 'Dinner with friends')
        
        # Case insensitive
        results = self.tm.search_transactions("DINNER")
        self.assertEqual(len(results), 1)
    
    def test_calculate_totals(self):
        """Test total calculations."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project")
        
        total_expenses = self.tm.calculate_total_expenses()
        self.assertEqual(total_expenses, 750.0)
        
        total_income = self.tm.calculate_total_income()
        self.assertEqual(total_income, 30000.0)
        
        balance = self.tm.calculate_balance()
        self.assertEqual(balance, 29250.0)
    
    def test_category_totals(self):
        """Test category-wise totals."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_expense("2026-09-28", 200.0, "Food", "Lunch")
        
        totals = self.tm.get_category_totals('expense')
        self.assertEqual(totals['Food'], 650.0)
        self.assertEqual(totals['Travel'], 300.0)
    
    def test_monthly_summary(self):
        """Test monthly summary."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        # Different month
        self.tm.add_expense("2026-08-15", 100.0, "Food", "Old expense")
        
        summary = self.tm.get_monthly_summary("2026-09")
        self.assertEqual(summary['month'], '2026-09')
        self.assertEqual(summary['total_income'], 25000.0)
        self.assertEqual(summary['total_expenses'], 750.0)
        self.assertEqual(summary['balance'], 24250.0)
        self.assertEqual(summary['transaction_count'], 3)
        self.assertEqual(summary['expense_count'], 2)
        self.assertEqual(summary['income_count'], 1)
    
    def test_unique_id_generation(self):
        """Test that IDs are unique and sequential."""
        exp1 = self.tm.add_expense("2026-09-30", 100.0, "Food", "Test 1")
        exp2 = self.tm.add_expense("2026-09-30", 200.0, "Food", "Test 2")
        exp3 = self.tm.add_expense("2026-09-30", 300.0, "Food", "Test 3")
        
        self.assertEqual(exp1['id'], 'EXP001')
        self.assertEqual(exp2['id'], 'EXP002')
        self.assertEqual(exp3['id'], 'EXP003')
        
        inc1 = self.tm.add_income("2026-09-30", 1000.0, "Salary", "Test 1")
        inc2 = self.tm.add_income("2026-09-30", 2000.0, "Salary", "Test 2")
        
        self.assertEqual(inc1['id'], 'INC001')
        self.assertEqual(inc2['id'], 'INC002')
    
    def test_id_persistence_across_instances(self):
        """Test that ID counter persists across TransactionManager instances."""
        self.tm.add_expense("2026-09-30", 100.0, "Food", "Test 1")
        self.tm.add_expense("2026-09-30", 200.0, "Food", "Test 2")
        
        # Create new instance with same storage
        tm2 = TransactionManager(self.storage)
        exp3 = tm2.add_expense("2026-09-30", 300.0, "Food", "Test 3")
        
        self.assertEqual(exp3['id'], 'EXP003')


if __name__ == '__main__':
    unittest.main()
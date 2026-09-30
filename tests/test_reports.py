"""
Test cases for Report Manager.
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
from report_manager import ReportManager


class TestReportManager(unittest.TestCase):
    """Test cases for Report Manager."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = Storage(self.test_dir)
        self.tm = TransactionManager(self.storage)
        self.budget_mgr = BudgetManager(self.storage, self.tm)
        self.report_mgr = ReportManager(self.tm, self.budget_mgr)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_overall_summary(self):
        """Test overall financial summary."""
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project")
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        
        summary = self.report_mgr.get_overall_summary()
        
        self.assertEqual(summary['total_income'], 30000.0)
        self.assertEqual(summary['total_expenses'], 750.0)
        self.assertEqual(summary['balance'], 29250.0)
        self.assertEqual(summary['transaction_count'], 4)
        self.assertEqual(summary['expense_count'], 2)
        self.assertEqual(summary['income_count'], 2)
    
    def test_category_report_expense(self):
        """Test category-wise expense report."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_expense("2026-09-28", 200.0, "Food", "Lunch")
        
        report = self.report_mgr.get_category_report('expense')
        
        self.assertEqual(report['type'], 'expense')
        self.assertEqual(report['total'], 950.0)
        self.assertEqual(report['category_count'], 2)
        
        # Check categories sorted by amount descending
        categories = report['categories']
        self.assertEqual(categories[0]['category'], 'Food')
        self.assertEqual(categories[0]['amount'], 650.0)
        self.assertEqual(categories[1]['category'], 'Travel')
        self.assertEqual(categories[1]['amount'], 300.0)
        
        # Check percentages
        self.assertAlmostEqual(categories[0]['percentage'], 68.42, places=1)
        self.assertAlmostEqual(categories[1]['percentage'], 31.58, places=1)
    
    def test_category_report_income(self):
        """Test category-wise income report."""
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project")
        
        report = self.report_mgr.get_category_report('income')
        
        self.assertEqual(report['total'], 30000.0)
        self.assertEqual(report['category_count'], 2)
    
    def test_category_report_empty(self):
        """Test category report with no data."""
        report = self.report_mgr.get_category_report('expense')
        
        self.assertEqual(report['total'], 0.0)
        self.assertEqual(report['category_count'], 0)
        self.assertEqual(len(report['categories']), 0)
    
    def test_monthly_report(self):
        """Test detailed monthly report."""
        self.budget_mgr.set_budget("2026-09", 20000.0)
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        
        report = self.report_mgr.get_monthly_report("2026-09")
        
        self.assertEqual(report['month'], '2026-09')
        self.assertEqual(report['summary']['total_income'], 25000.0)
        self.assertEqual(report['summary']['total_expenses'], 750.0)
        self.assertEqual(report['summary']['balance'], 24250.0)
        
        # Check expense categories
        self.assertEqual(report['expense_categories']['Food'], 450.0)
        self.assertEqual(report['expense_categories']['Travel'], 300.0)
        
        # Check budget status
        self.assertTrue(report['budget_status']['has_budget'])
        self.assertEqual(report['budget_status']['budget_amount'], 20000.0)
        self.assertEqual(report['budget_status']['percentage_used'], 3.75)
    
    def test_highest_spending_category(self):
        """Test getting highest spending category."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_expense("2026-09-28", 200.0, "Food", "Lunch")
        
        highest = self.report_mgr.get_highest_spending_category()
        
        self.assertIsNotNone(highest)
        self.assertEqual(highest['category'], 'Food')
        self.assertEqual(highest['amount'], 650.0)
    
    def test_highest_spending_category_empty(self):
        """Test highest spending category with no expenses."""
        highest = self.report_mgr.get_highest_spending_category()
        self.assertIsNone(highest)
    
    def test_average_expense(self):
        """Test average expense calculation."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_expense("2026-09-28", 250.0, "Food", "Lunch")
        
        avg = self.report_mgr.get_average_expense()
        self.assertEqual(avg, 1000.0 / 3)
    
    def test_average_expense_empty(self):
        """Test average expense with no expenses."""
        avg = self.report_mgr.get_average_expense()
        self.assertEqual(avg, 0.0)
    
    def test_largest_transaction(self):
        """Test largest transaction."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 1000.0, "Shopping", "New phone")
        self.tm.add_expense("2026-09-28", 300.0, "Travel", "Bus fare")
        
        largest = self.report_mgr.get_largest_transaction('expense')
        
        self.assertIsNotNone(largest)
        self.assertEqual(largest['amount'], 1000.0)
        self.assertEqual(largest['category'], 'Shopping')
    
    def test_largest_income(self):
        """Test largest income transaction."""
        self.tm.add_income("2026-09-30", 25000.0, "Salary", "Monthly salary")
        self.tm.add_income("2026-09-29", 5000.0, "Freelance", "Project")
        
        largest = self.report_mgr.get_largest_transaction('income')
        
        self.assertIsNotNone(largest)
        self.assertEqual(largest['amount'], 25000.0)
        self.assertEqual(largest['category'], 'Salary')
    
    def test_expense_distribution(self):
        """Test expense distribution percentages."""
        self.tm.add_expense("2026-09-30", 450.0, "Food", "Dinner")
        self.tm.add_expense("2026-09-29", 300.0, "Travel", "Bus fare")
        self.tm.add_expense("2026-09-28", 250.0, "Food", "Lunch")
        
        dist = self.report_mgr.get_expense_distribution()
        
        self.assertEqual(len(dist), 2)
        # Should be sorted by percentage descending
        self.assertEqual(dist[0]['category'], 'Food')
        self.assertGreater(dist[0]['percentage'], dist[1]['percentage'])
    
    def test_format_currency(self):
        """Test currency formatting."""
        self.assertEqual(self.report_mgr.format_currency(1000), "Rs.1,000.00")
        self.assertEqual(self.report_mgr.format_currency(1000.5), "Rs.1,000.50")
        self.assertEqual(self.report_mgr.format_currency(0), "Rs.0.00")
        self.assertEqual(self.report_mgr.format_currency(1234567.89), "Rs.1,234,567.89")


if __name__ == '__main__':
    unittest.main()
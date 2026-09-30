"""
Report Manager Module - Financial reports and analytics.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from transaction_manager import TransactionManager
from budget_manager import BudgetManager


class ReportManager:
    """Generates financial reports and analytics."""
    
    def __init__(self, transaction_manager: TransactionManager, budget_manager: BudgetManager):
        self.tm = transaction_manager
        self.bm = budget_manager
    
    def get_overall_summary(self) -> Dict[str, Any]:
        """Get overall financial summary."""
        total_income = self.tm.calculate_total_income()
        total_expenses = self.tm.calculate_total_expenses()
        balance = total_income - total_expenses
        all_transactions = self.tm.get_all_transactions()
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance,
            'transaction_count': len(all_transactions),
            'expense_count': len(self.tm.get_expenses()),
            'income_count': len(self.tm.get_income())
        }
    
    def get_category_report(self, transaction_type: str = 'expense') -> Dict[str, Any]:
        """Get category-wise spending report."""
        totals = self.tm.get_category_totals(transaction_type)
        transactions = self.tm.get_expenses() if transaction_type == 'expense' else self.tm.get_income()
        
        # Sort by amount descending
        sorted_categories = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate percentages
        total_amount = sum(totals.values())
        categories_with_pct = []
        for cat, amount in sorted_categories:
            pct = (amount / total_amount * 100) if total_amount > 0 else 0
            categories_with_pct.append({
                'category': cat,
                'amount': amount,
                'percentage': pct
            })
        
        return {
            'type': transaction_type,
            'categories': categories_with_pct,
            'total': total_amount,
            'category_count': len(categories_with_pct)
        }
    
    def get_monthly_report(self, month: str) -> Dict[str, Any]:
        """Get detailed monthly report."""
        summary = self.tm.get_monthly_summary(month)
        expenses = self.tm.get_expenses_by_month(month)
        income = self.tm.get_income_by_month(month)
        
        # Category breakdown for expenses
        expense_categories = {}
        for e in expenses:
            cat = e.get('category', 'Other')
            expense_categories[cat] = expense_categories.get(cat, 0) + e.get('amount', 0)
        
        # Category breakdown for income
        income_categories = {}
        for i in income:
            cat = i.get('category', 'Other')
            income_categories[cat] = income_categories.get(cat, 0) + i.get('amount', 0)
        
        # Budget status
        budget_status = self.bm.calculate_budget_status(month)
        
        return {
            'month': month,
            'summary': summary,
            'expense_categories': expense_categories,
            'income_categories': income_categories,
            'budget_status': budget_status,
            'expenses': expenses,
            'income': income
        }
    
    def get_highest_spending_category(self) -> Optional[Dict[str, Any]]:
        """Get the category with highest spending."""
        report = self.get_category_report('expense')
        if report['categories']:
            top = report['categories'][0]
            return {
                'category': top['category'],
                'amount': top['amount'],
                'percentage': top['percentage']
            }
        return None
    
    def get_average_expense(self) -> float:
        """Calculate average expense amount."""
        expenses = self.tm.get_expenses()
        if not expenses:
            return 0.0
        total = sum(e.get('amount', 0) for e in expenses)
        return total / len(expenses)
    
    def get_largest_transaction(self, transaction_type: str = 'expense') -> Optional[Dict[str, Any]]:
        """Get the largest single transaction."""
        transactions = self.tm.get_expenses() if transaction_type == 'expense' else self.tm.get_income()
        if not transactions:
            return None
        return max(transactions, key=lambda x: x.get('amount', 0))
    
    def get_expense_distribution(self) -> List[Dict[str, Any]]:
        """Get expense distribution as percentages."""
        report = self.get_category_report('expense')
        return report['categories']
    
    def get_monthly_trends(self, months: int = 6) -> List[Dict[str, Any]]:
        """Get monthly trends for the last N months."""
        from datetime import datetime, timedelta
        
        trends = []
        current = datetime.now()
        
        for i in range(months):
            month_str = (current.replace(day=1) - timedelta(days=i*30)).strftime("%Y-%m")
            # Adjust for month boundaries properly
            if i == 0:
                month_date = current.replace(day=1)
            else:
                # Go back i months
                year = current.year
                month = current.month - i
                while month <= 0:
                    month += 12
                    year -= 1
                month_date = datetime(year, month, 1)
            month_str = month_date.strftime("%Y-%m")
            
            summary = self.tm.get_monthly_summary(month_str)
            trends.append(summary)
        
        # Reverse to show oldest first
        trends.reverse()
        return trends
    
    def format_currency(self, amount: float) -> str:
        """Format amount as Indian Rupees."""
        return f"Rs.{amount:,.2f}"
    
    def print_financial_summary(self) -> None:
        """Print formatted financial summary to console."""
        summary = self.get_overall_summary()
        
        print("\n" + "=" * 50)
        print("           FINANCIAL SUMMARY")
        print("=" * 50)
        print(f"\nTotal Income      : {self.format_currency(summary['total_income'])}")
        print(f"Total Expenses    : {self.format_currency(summary['total_expenses'])}")
        print(f"Current Balance   : {self.format_currency(summary['balance'])}")
        print(f"Total Transactions: {summary['transaction_count']}")
        print(f"  - Expenses      : {summary['expense_count']}")
        print(f"  - Income        : {summary['income_count']}")
        print("=" * 50)
    
    def print_category_report(self, transaction_type: str = 'expense') -> None:
        """Print formatted category report to console."""
        report = self.get_category_report(transaction_type)
        type_label = "EXPENSES" if transaction_type == 'expense' else "INCOME"
        
        print("\n" + "=" * 50)
        print(f"       CATEGORY-WISE {type_label}")
        print("=" * 50)
        
        if not report['categories']:
            print(f"\nNo {transaction_type.lower()} records found.")
        else:
            print()
            for cat_data in report['categories']:
                cat = cat_data['category']
                amount = cat_data['amount']
                pct = cat_data['percentage']
                print(f"{cat:<20} {self.format_currency(amount):>12} ({pct:.1f}%)")
            
            print(f"\n{'Total':<20} {self.format_currency(report['total']):>12}")
        
        print("=" * 50)
    
    def print_monthly_report(self, month: str) -> None:
        """Print formatted monthly report to console."""
        report = self.get_monthly_report(month)
        summary = report['summary']
        budget_status = report['budget_status']
        
        print("\n" + "=" * 50)
        print(f"       MONTHLY REPORT - {month}")
        print("=" * 50)
        
        print(f"\nMonthly Income    : {self.format_currency(summary['total_income'])}")
        print(f"Monthly Expenses  : {self.format_currency(summary['total_expenses'])}")
        print(f"Monthly Balance   : {self.format_currency(summary['balance'])}")
        print(f"Transactions      : {summary['transaction_count']}")
        
        # Budget info
        if budget_status.get('has_budget'):
            print(f"\nBudget            : {self.format_currency(budget_status['budget_amount'])}")
            print(f"Spent             : {self.format_currency(budget_status['total_expenses'])}")
            print(f"Remaining         : {self.format_currency(budget_status['remaining'])}")
            print(f"Budget Used       : {budget_status['percentage_used']:.1f}%")
            print(f"Status            : {budget_status['status']}")
        else:
            print(f"\n{budget_status['message']}")
        
        # Expense categories
        if report['expense_categories']:
            print("\n  Expense Breakdown:")
            for cat, amt in sorted(report['expense_categories'].items(), key=lambda x: x[1], reverse=True):
                print(f"    {cat:<20} {self.format_currency(amt)}")
        
        print("=" * 50)
    
    def print_analytics(self) -> None:
        """Print analytics: highest category, average, largest transaction."""
        print("\n" + "=" * 50)
        print("           SPENDING ANALYTICS")
        print("=" * 50)
        
        # Highest spending category
        highest = self.get_highest_spending_category()
        if highest:
            print(f"\nHighest Spending Category:")
            print(f"  {highest['category']} - {self.format_currency(highest['amount'])} ({highest['percentage']:.1f}%)")
        else:
            print("\nNo expense data available.")
        
        # Average expense
        avg = self.get_average_expense()
        print(f"\nAverage Expense   : {self.format_currency(avg)}")
        
        # Largest expense
        largest_expense = self.get_largest_transaction('expense')
        if largest_expense:
            print(f"\nLargest Expense:")
            print(f"  {largest_expense['id']} - {largest_expense['date']} - {largest_expense['category']}")
            print(f"  Amount: {self.format_currency(largest_expense['amount'])}")
            if largest_expense.get('description'):
                print(f"  Description: {largest_expense['description']}")
        
        # Largest income
        largest_income = self.get_largest_transaction('income')
        if largest_income:
            print(f"\nLargest Income:")
            print(f"  {largest_income['id']} - {largest_income['date']} - {largest_income['category']}")
            print(f"  Amount: {self.format_currency(largest_income['amount'])}")
            if largest_income.get('description'):
                print(f"  Description: {largest_income['description']}")
        
        # Distribution
        print("\nExpense Distribution:")
        dist = self.get_expense_distribution()
        if dist:
            for d in dist:
                bar = "█" * int(d['percentage'] / 5)
                print(f"  {d['category']:<20} {d['percentage']:>5.1f}% {bar}")
        else:
            print("  No expense data.")
        
        print("=" * 50)
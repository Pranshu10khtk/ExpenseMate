"""
Expense Manager Module - Expense-specific operations and CLI handling.
"""

from typing import List, Dict, Any, Optional
from transaction_manager import TransactionManager
from validators import Validator
from utils import CLIUtils


class ExpenseManager:
    """Handles expense-specific operations and user interaction."""
    
    def __init__(self, transaction_manager: TransactionManager):
        self.tm = transaction_manager
        self.validator = Validator()
        self.cli = CLIUtils()
    
    def add_expense_interactive(self) -> Optional[Dict[str, Any]]:
        """Interactive expense addition."""
        self.cli.print_header("Add Expense")
        
        # Date
        while True:
            date_input = self.cli.get_input("Date (YYYY-MM-DD)", "")
            if not date_input:
                from utils import get_current_month
                date_input = datetime.now().strftime("%Y-%m-%d")
            
            valid, date, error = self.validator.validate_date(date_input)
            if valid:
                break
            print(f"Error: {error}")
        
        # Amount
        while True:
            amount_input = self.cli.get_input("Amount", "")
            valid, amount, error = self.validator.validate_amount(amount_input)
            if valid:
                break
            print(f"Error: {error}")
        
        # Category
        print("\nAvailable categories:")
        categories = self.validator.get_category_choices('expense')
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        print(f"  {len(categories)+1}. Custom category")
        
        while True:
            cat_input = self.cli.get_input("Select category (number or name)", "")
            if cat_input.isdigit():
                idx = int(cat_input) - 1
                if 0 <= idx < len(categories):
                    category = categories[idx]
                    break
                elif idx == len(categories):
                    category = self.cli.get_input("Enter custom category", "")
                    if category:
                        break
                    print("Category cannot be empty.")
                else:
                    print("Invalid selection.")
            else:
                valid, category, error = self.validator.validate_category(cat_input, 'expense')
                if valid:
                    break
                print(f"Error: {error}")
        
        # Description (optional)
        description = self.cli.get_input("Description (optional)", "")
        
        # Add expense
        expense = self.tm.add_expense(date, amount, category, description)
        print(f"\n✓ Expense added successfully! (ID: {expense['id']})")
        return expense
    
    def view_expenses(self, expenses: Optional[List[Dict[str, Any]]] = None) -> None:
        """View expenses in a formatted table."""
        if expenses is None:
            expenses = self.tm.get_expenses()
        
        self.cli.print_header("Expenses")
        
        if not expenses:
            print("\nNo expenses found.")
            return
        
        # Prepare table data
        headers = ['ID', 'Date', 'Amount', 'Category', 'Description']
        rows = []
        for e in expenses:
            rows.append([
                e.get('id', ''),
                e.get('date', ''),
                format_currency(e.get('amount', 0)),
                e.get('category', ''),
                e.get('description', '')[:30]  # Truncate long descriptions
            ])
        
        self.cli.print_table(headers, rows)
        print(f"\nTotal: {len(expenses)} expense(s) - {format_currency(sum(e.get('amount', 0) for e in expenses))}")
    
    def view_expense_detail(self, transaction_id: str) -> bool:
        """View detailed expense by ID."""
        expense = self.tm.get_transaction_by_id(transaction_id)
        
        if not expense or expense.get('type') != 'expense':
            print(f"Expense with ID '{transaction_id}' not found.")
            return False
        
        self.cli.print_header(f"Expense Details - {expense['id']}")
        print(f"\nID          : {expense['id']}")
        print(f"Date        : {expense['date']}")
        print(f"Amount      : {format_currency(expense['amount'])}")
        print(f"Category    : {expense['category']}")
        print(f"Description : {expense.get('description', 'N/A')}")
        print(f"Type        : {expense['type']}")
        return True
    
    def update_expense_interactive(self) -> bool:
        """Interactive expense update."""
        self.cli.print_header("Update Expense")
        
        expenses = self.tm.get_expenses()
        if not expenses:
            print("No expenses to update.")
            return False
        
        # Show expenses
        self.view_expenses(expenses)
        
        # Get ID
        transaction_id = self.cli.get_input("Enter Expense ID to update", "").upper()
        valid, tid, error = self.validator.validate_transaction_id(transaction_id, expenses)
        if not valid:
            print(f"Error: {error}")
            return False
        
        expense = self.tm.get_transaction_by_id(tid)
        print(f"\nCurrent values:")
        print(f"  Date: {expense['date']}")
        print(f"  Amount: {format_currency(expense['amount'])}")
        print(f"  Category: {expense['category']}")
        print(f"  Description: {expense.get('description', 'N/A')}")
        
        # Get new values (empty = keep current)
        print("\nEnter new values (press Enter to keep current):")
        
        # Date
        new_date = self.cli.get_input("Date (YYYY-MM-DD)", expense['date'])
        if new_date != expense['date']:
            valid, date, error = self.validator.validate_date(new_date)
            if not valid:
                print(f"Error: {error}")
                return False
            new_date = date
        else:
            new_date = None
        
        # Amount
        new_amount = self.cli.get_input("Amount", str(expense['amount']))
        if new_amount != str(expense['amount']):
            valid, amount, error = self.validator.validate_amount(new_amount)
            if not valid:
                print(f"Error: {error}")
                return False
            new_amount = amount
        else:
            new_amount = None
        
        # Category
        new_category = self.cli.get_input("Category", expense['category'])
        if new_category != expense['category']:
            valid, cat, error = self.validator.validate_category(new_category, 'expense')
            if not valid:
                print(f"Error: {error}")
                return False
            new_category = cat
        else:
            new_category = None
        
        # Description
        new_desc = self.cli.get_input("Description", expense.get('description', ''))
        if new_desc != expense.get('description', ''):
            new_desc = new_desc
        else:
            new_desc = None
        
        # Update
        success = self.tm.update_transaction(
            tid,
            date=new_date,
            amount=new_amount,
            category=new_category,
            description=new_desc
        )
        
        if success:
            print("\n✓ Expense updated successfully!")
            return True
        else:
            print("\nError: Failed to update expense.")
            return False
    
    def delete_expense_interactive(self) -> bool:
        """Interactive expense deletion."""
        self.cli.print_header("Delete Expense")
        
        expenses = self.tm.get_expenses()
        if not expenses:
            print("No expenses to delete.")
            return False
        
        self.view_expenses(expenses)
        
        transaction_id = self.cli.get_input("Enter Expense ID to delete", "").upper()
        valid, tid, error = self.validator.validate_transaction_id(transaction_id, expenses)
        if not valid:
            print(f"Error: {error}")
            return False
        
        expense = self.tm.get_transaction_by_id(tid)
        print(f"\nSelected: {expense['id']} - {expense['date']} - {format_currency(expense['amount'])} - {expense['category']}")
        
        if not self.cli.confirm("Are you sure you want to delete this expense?"):
            print("Deletion cancelled.")
            return False
        
        success = self.tm.delete_transaction(tid)
        if success:
            print("\n✓ Expense deleted successfully!")
            return True
        else:
            print("\nError: Failed to delete expense.")
            return False
    
    def filter_expenses_interactive(self) -> List[Dict[str, Any]]:
        """Interactive expense filtering."""
        self.cli.print_header("Filter Expenses")
        
        print("Available filters (press Enter to skip):")
        
        # Category filter
        print("\nCategories:")
        categories = self.validator.get_category_choices('expense')
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        
        cat_input = self.cli.get_input("Filter by category (number/name or Enter to skip)", "")
        category = None
        if cat_input:
            if cat_input.isdigit():
                idx = int(cat_input) - 1
                if 0 <= idx < len(categories):
                    category = categories[idx]
            else:
                category = cat_input
        
        # Date range
        start_date = None
        end_date = None
        
        start_input = self.cli.get_input("Start date (YYYY-MM-DD)", "")
        if start_input:
            valid, date, error = self.validator.validate_date(start_input)
            if valid:
                start_date = date
            else:
                print(f"Warning: {error} - ignoring filter")
        
        end_input = self.cli.get_input("End date (YYYY-MM-DD)", "")
        if end_input:
            valid, date, error = self.validator.validate_date(end_input)
            if valid:
                end_date = date
            else:
                print(f"Warning: {error} - ignoring filter")
        
        # Amount range
        min_amount = None
        max_amount = None
        
        min_input = self.cli.get_input("Minimum amount", "")
        if min_input:
            valid, amt, error = self.validator.validate_amount(min_input)
            if valid:
                min_amount = amt
            else:
                print(f"Warning: {error} - ignoring filter")
        
        max_input = self.cli.get_input("Maximum amount", "")
        if max_input:
            valid, amt, error = self.validator.validate_amount(max_input)
            if valid:
                max_amount = amt
            else:
                print(f"Warning: {error} - ignoring filter")
        
        # Apply filters
        filtered = self.tm.filter_transactions(
            transaction_type='expense',
            category=category,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount
        )
        
        self.view_expenses(filtered)
        return filtered


from utils import format_currency
from datetime import datetime
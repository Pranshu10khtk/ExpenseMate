"""
Income Manager Module - Income-specific operations and CLI handling.
"""

from typing import List, Dict, Any, Optional
from transaction_manager import TransactionManager
from validators import Validator
from utils import CLIUtils, format_currency
from datetime import datetime


class IncomeManager:
    """Handles income-specific operations and user interaction."""
    
    def __init__(self, transaction_manager: TransactionManager):
        self.tm = transaction_manager
        self.validator = Validator()
        self.cli = CLIUtils()
    
    def add_income_interactive(self) -> Optional[Dict[str, Any]]:
        """Interactive income addition."""
        self.cli.print_header("Add Income")
        
        # Date
        while True:
            date_input = self.cli.get_input("Date (YYYY-MM-DD)", "")
            if not date_input:
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
        categories = self.validator.get_category_choices('income')
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
                valid, category, error = self.validator.validate_category(cat_input, 'income')
                if valid:
                    break
                print(f"Error: {error}")
        
        # Description (optional)
        description = self.cli.get_input("Description (optional)", "")
        
        # Add income
        income = self.tm.add_income(date, amount, category, description)
        print(f"\n✓ Income added successfully! (ID: {income['id']})")
        return income
    
    def view_income(self, income_list: Optional[List[Dict[str, Any]]] = None) -> None:
        """View income in a formatted table."""
        if income_list is None:
            income_list = self.tm.get_income()
        
        self.cli.print_header("Income")
        
        if not income_list:
            print("\nNo income records found.")
            return
        
        # Prepare table data
        headers = ['ID', 'Date', 'Amount', 'Source', 'Description']
        rows = []
        for inc in income_list:
            rows.append([
                inc.get('id', ''),
                inc.get('date', ''),
                format_currency(inc.get('amount', 0)),
                inc.get('category', ''),
                inc.get('description', '')[:30]
            ])
        
        self.cli.print_table(headers, rows)
        print(f"\nTotal: {len(income_list)} income record(s) - {format_currency(sum(i.get('amount', 0) for i in income_list))}")
    
    def view_income_detail(self, transaction_id: str) -> bool:
        """View detailed income by ID."""
        income = self.tm.get_transaction_by_id(transaction_id)
        
        if not income or income.get('type') != 'income':
            print(f"Income with ID '{transaction_id}' not found.")
            return False
        
        self.cli.print_header(f"Income Details - {income['id']}")
        print(f"\nID          : {income['id']}")
        print(f"Date        : {income['date']}")
        print(f"Amount      : {format_currency(income['amount'])}")
        print(f"Source      : {income['category']}")
        print(f"Description : {income.get('description', 'N/A')}")
        print(f"Type        : {income['type']}")
        return True
    
    def update_income_interactive(self) -> bool:
        """Interactive income update."""
        self.cli.print_header("Update Income")
        
        income_list = self.tm.get_income()
        if not income_list:
            print("No income records to update.")
            return False
        
        # Show income
        self.view_income(income_list)
        
        # Get ID
        transaction_id = self.cli.get_input("Enter Income ID to update", "").upper()
        valid, tid, error = self.validator.validate_transaction_id(transaction_id, income_list)
        if not valid:
            print(f"Error: {error}")
            return False
        
        income = self.tm.get_transaction_by_id(tid)
        print(f"\nCurrent values:")
        print(f"  Date: {income['date']}")
        print(f"  Amount: {format_currency(income['amount'])}")
        print(f"  Source: {income['category']}")
        print(f"  Description: {income.get('description', 'N/A')}")
        
        # Get new values (empty = keep current)
        print("\nEnter new values (press Enter to keep current):")
        
        # Date
        new_date = self.cli.get_input("Date (YYYY-MM-DD)", income['date'])
        if new_date != income['date']:
            valid, date, error = self.validator.validate_date(new_date)
            if not valid:
                print(f"Error: {error}")
                return False
            new_date = date
        else:
            new_date = None
        
        # Amount
        new_amount = self.cli.get_input("Amount", str(income['amount']))
        if new_amount != str(income['amount']):
            valid, amount, error = self.validator.validate_amount(new_amount)
            if not valid:
                print(f"Error: {error}")
                return False
            new_amount = amount
        else:
            new_amount = None
        
        # Category
        new_category = self.cli.get_input("Source/Category", income['category'])
        if new_category != income['category']:
            valid, cat, error = self.validator.validate_category(new_category, 'income')
            if not valid:
                print(f"Error: {error}")
                return False
            new_category = cat
        else:
            new_category = None
        
        # Description
        new_desc = self.cli.get_input("Description", income.get('description', ''))
        if new_desc != income.get('description', ''):
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
            print("\n✓ Income updated successfully!")
            return True
        else:
            print("\nError: Failed to update income.")
            return False
    
    def delete_income_interactive(self) -> bool:
        """Interactive income deletion."""
        self.cli.print_header("Delete Income")
        
        income_list = self.tm.get_income()
        if not income_list:
            print("No income records to delete.")
            return False
        
        self.view_income(income_list)
        
        transaction_id = self.cli.get_input("Enter Income ID to delete", "").upper()
        valid, tid, error = self.validator.validate_transaction_id(transaction_id, income_list)
        if not valid:
            print(f"Error: {error}")
            return False
        
        income = self.tm.get_transaction_by_id(tid)
        print(f"\nSelected: {income['id']} - {income['date']} - {format_currency(income['amount'])} - {income['category']}")
        
        if not self.cli.confirm("Are you sure you want to delete this income record?"):
            print("Deletion cancelled.")
            return False
        
        success = self.tm.delete_transaction(tid)
        if success:
            print("\n✓ Income deleted successfully!")
            return True
        else:
            print("\nError: Failed to delete income.")
            return False
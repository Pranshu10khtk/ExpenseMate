"""
ExpenseMate - Main Application Entry Point
Personal Expense Management System
"""

import sys
from storage import Storage
from transaction_manager import TransactionManager
from expense_manager import ExpenseManager
from income_manager import IncomeManager
from budget_manager import BudgetManager
from report_manager import ReportManager
from utils import CLIUtils, ExportManager, get_current_month, parse_month_input
from validators import Validator


class ExpenseMateApp:
    """Main application class for ExpenseMate."""
    
    def __init__(self):
        # Initialize core components
        self.storage = Storage()
        self.tm = TransactionManager(self.storage)
        self.expense_mgr = ExpenseManager(self.tm)
        self.income_mgr = IncomeManager(self.tm)
        self.budget_mgr = BudgetManager(self.storage, self.tm)
        self.report_mgr = ReportManager(self.tm, self.budget_mgr)
        self.export_mgr = ExportManager(self.tm)
        self.cli = CLIUtils()
        self.validator = Validator()
    
    def run(self) -> None:
        """Main application loop."""
        self.cli.clear_screen()
        self.print_welcome()
        
        while True:
            self.print_main_menu()
            choice = self.cli.get_input("Enter your choice")
            
            try:
                self.handle_main_menu(choice)
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                self.cli.pause()
    
    def print_welcome(self) -> None:
        """Print welcome banner."""
        print("=" * 50)
        print("        EXPENSEMATE")
        print("   Personal Expense Management System")
        print("=" * 50)
    
    def print_main_menu(self) -> None:
        """Print main menu options."""
        options = [
            "Add Expense",
            "View Expenses",
            "Update Expense",
            "Delete Expense",
            "Add Income",
            "View Income",
            "Update Income",
            "Delete Income",
            "Manage Budget",
            "Financial Summary",
            "Reports & Analytics",
            "Search / Filter Transactions",
            "Export Data",
            "Help"
        ]
        self.cli.print_menu(options, "MAIN MENU")
    
    def handle_main_menu(self, choice: str) -> None:
        """Handle main menu selection."""
        menu_actions = {
            '1': self.add_expense,
            '2': self.view_expenses,
            '3': self.update_expense,
            '4': self.delete_expense,
            '5': self.add_income,
            '6': self.view_income,
            '7': self.update_income,
            '8': self.delete_income,
            '9': self.manage_budget,
            '10': self.show_financial_summary,
            '11': self.show_reports_menu,
            '12': self.search_filter_menu,
            '13': self.export_menu,
            '14': self.show_help,
            '0': self.exit_app
        }
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please try again.")
    
    # Expense operations
    def add_expense(self) -> None:
        self.expense_mgr.add_expense_interactive()
        self.cli.pause()
    
    def view_expenses(self) -> None:
        self.expense_mgr.view_expenses()
        self.cli.pause()
    
    def update_expense(self) -> None:
        self.expense_mgr.update_expense_interactive()
        self.cli.pause()
    
    def delete_expense(self) -> None:
        self.expense_mgr.delete_expense_interactive()
        self.cli.pause()
    
    # Income operations
    def add_income(self) -> None:
        self.income_mgr.add_income_interactive()
        self.cli.pause()
    
    def view_income(self) -> None:
        self.income_mgr.view_income()
        self.cli.pause()
    
    def update_income(self) -> None:
        self.income_mgr.update_income_interactive()
        self.cli.pause()
    
    def delete_income(self) -> None:
        self.income_mgr.delete_income_interactive()
        self.cli.pause()
    
    # Budget operations
    def manage_budget(self) -> None:
        while True:
            self.cli.print_header("Budget Management")
            
            current_month = get_current_month()
            budget_status = self.budget_mgr.get_budget_summary(current_month)
            
            if budget_status.get('has_budget'):
                print(f"\nCurrent Month: {current_month}")
                print(f"Budget: {self.report_mgr.format_currency(budget_status['budget_amount'])}")
                print(f"Expenses: {self.report_mgr.format_currency(budget_status['total_expenses'])}")
                print(f"Remaining: {self.report_mgr.format_currency(budget_status['remaining'])}")
                print(f"Used: {budget_status['percentage_used']:.1f}%")
                print(f"Status: {budget_status['status']}")
            else:
                print(f"\n{current_month}: {budget_status['message']}")
            
            print("\nOptions:")
            print("1. Set/Update Budget")
            print("2. View Budget Status")
            print("3. Delete Budget")
            print("0. Back")
            
            choice = self.cli.get_input("Enter choice")
            
            if choice == '1':
                self.set_budget()
            elif choice == '2':
                self.view_budget_status()
            elif choice == '3':
                self.delete_budget()
            elif choice == '0':
                break
            else:
                print("Invalid option.")
            
            self.cli.pause()
    
    def set_budget(self) -> None:
        """Set or update budget."""
        month_input = self.cli.get_input("Month (YYYY-MM) [current]", "")
        month = parse_month_input(month_input)
        
        while True:
            amount_input = self.cli.get_input("Budget Amount", "")
            valid, amount, error = self.validator.validate_amount(amount_input)
            if valid:
                break
            print(f"Error: {error}")
        
        if self.budget_mgr.set_budget(month, amount):
            print(f"\n✓ Budget set for {month}: {self.report_mgr.format_currency(amount)}")
        else:
            print("\nError: Failed to set budget.")
    
    def view_budget_status(self) -> None:
        """View detailed budget status."""
        month_input = self.cli.get_input("Month (YYYY-MM) [current]", "")
        month = parse_month_input(month_input)
        
        status = self.budget_mgr.get_budget_summary(month)
        
        self.cli.print_header(f"Budget Status - {month}")
        
        if not status.get('has_budget'):
            print(f"\n{status['message']}")
        else:
            print(f"\nBudget Amount    : {self.report_mgr.format_currency(status['budget_amount'])}")
            print(f"Total Expenses   : {self.report_mgr.format_currency(status['total_expenses'])}")
            print(f"Remaining        : {self.report_mgr.format_currency(status['remaining'])}")
            print(f"Budget Used      : {status['percentage_used']:.1f}%")
            print(f"Status           : {status['status']}")
            print(f"Transactions     : {status['transaction_count']}")
            
            if status['status'] == 'EXCEEDED':
                print(f"\n⚠ WARNING: Budget exceeded by {self.report_mgr.format_currency(abs(status['remaining']))}!")
            elif status['status'] == 'WARNING':
                print(f"\n⚠ WARNING: Approaching budget limit ({status['percentage_used']:.1f}% used)")
    
    def delete_budget(self) -> None:
        """Delete budget for a month."""
        month_input = self.cli.get_input("Month (YYYY-MM) [current]", "")
        month = parse_month_input(month_input)
        
        if self.cli.confirm(f"Delete budget for {month}?"):
            if self.budget_mgr.delete_budget(month):
                print(f"\n✓ Budget for {month} deleted.")
            else:
                print(f"\nNo budget found for {month}.")
    
    # Reports
    def show_financial_summary(self) -> None:
        self.report_mgr.print_financial_summary()
        self.cli.pause()
    
    def show_reports_menu(self) -> None:
        while True:
            self.cli.print_header("Reports & Analytics")
            
            options = [
                "Category-wise Expense Report",
                "Category-wise Income Report",
                "Monthly Report",
                "Spending Analytics",
                "Monthly Trends (Last 6 Months)"
            ]
            self.cli.print_menu(options, "REPORTS")
            
            choice = self.cli.get_input("Enter choice")
            
            if choice == '1':
                self.report_mgr.print_category_report('expense')
                self.cli.pause()
            elif choice == '2':
                self.report_mgr.print_category_report('income')
                self.cli.pause()
            elif choice == '3':
                month_input = self.cli.get_input("Month (YYYY-MM) [current]", "")
                month = parse_month_input(month_input)
                self.report_mgr.print_monthly_report(month)
                self.cli.pause()
            elif choice == '4':
                self.report_mgr.print_analytics()
                self.cli.pause()
            elif choice == '5':
                self.show_monthly_trends()
                self.cli.pause()
            elif choice == '0':
                break
            else:
                print("Invalid option.")
    
    def show_monthly_trends(self) -> None:
        """Show monthly trends."""
        self.cli.print_header("Monthly Trends (Last 6 Months)")
        
        trends = self.report_mgr.get_monthly_trends(6)
        
        if not trends:
            print("No data available.")
            return
        
        headers = ['Month', 'Income', 'Expenses', 'Balance', 'Transactions']
        rows = []
        for t in trends:
            rows.append([
                t['month'],
                self.report_mgr.format_currency(t['total_income']),
                self.report_mgr.format_currency(t['total_expenses']),
                self.report_mgr.format_currency(t['balance']),
                str(t['transaction_count'])
            ])
        
        self.cli.print_table(headers, rows)
    
    # Search/Filter
    def search_filter_menu(self) -> None:
        while True:
            self.cli.print_header("Search / Filter Transactions")
            
            options = [
                "Filter Expenses",
                "Filter Income",
                "Search by Keyword",
                "View by Month",
                "View All Transactions"
            ]
            self.cli.print_menu(options, "SEARCH / FILTER")
            
            choice = self.cli.get_input("Enter choice")
            
            if choice == '1':
                self.expense_mgr.filter_expenses_interactive()
                self.cli.pause()
            elif choice == '2':
                self.filter_income_interactive()
                self.cli.pause()
            elif choice == '3':
                self.search_by_keyword()
                self.cli.pause()
            elif choice == '4':
                self.view_by_month()
                self.cli.pause()
            elif choice == '5':
                self.view_all_transactions()
                self.cli.pause()
            elif choice == '0':
                break
            else:
                print("Invalid option.")
    
    def filter_income_interactive(self) -> None:
        """Interactive income filtering."""
        self.cli.print_header("Filter Income")
        
        categories = self.validator.get_category_choices('income')
        print("\nCategories:")
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
        
        start_date = self.cli.get_input("Start date (YYYY-MM-DD)", "")
        if start_date:
            valid, date, error = self.validator.validate_date(start_date)
            if not valid:
                print(f"Warning: {error}")
                start_date = None
            else:
                start_date = date
        
        end_date = self.cli.get_input("End date (YYYY-MM-DD)", "")
        if end_date:
            valid, date, error = self.validator.validate_date(end_date)
            if not valid:
                print(f"Warning: {error}")
                end_date = None
            else:
                end_date = date
        
        filtered = self.tm.filter_transactions(
            transaction_type='income',
            category=category,
            start_date=start_date,
            end_date=end_date
        )
        
        self.income_mgr.view_income(filtered)
    
    def search_by_keyword(self) -> None:
        """Search transactions by keyword."""
        self.cli.print_header("Search Transactions")
        
        keyword = self.cli.get_input("Enter keyword to search in description/category")
        if not keyword:
            print("Keyword cannot be empty.")
            return
        
        results = self.tm.search_transactions(keyword)
        
        if not results:
            print(f"\nNo transactions found matching '{keyword}'.")
            return
        
        print(f"\nFound {len(results)} transaction(s):")
        headers = ['ID', 'Date', 'Amount', 'Category', 'Description', 'Type']
        rows = []
        for t in results:
            rows.append([
                t.get('id', ''),
                t.get('date', ''),
                format_currency(t.get('amount', 0)),
                t.get('category', ''),
                t.get('description', '')[:30],
                t.get('type', '')
            ])
        self.cli.print_table(headers, rows)
    
    def view_by_month(self) -> None:
        """View transactions for a specific month."""
        month_input = self.cli.get_input("Month (YYYY-MM) [current]", "")
        month = parse_month_input(month_input)
        
        transactions = self.tm.get_transactions_by_month(month)
        
        self.cli.print_header(f"Transactions - {month}")
        
        if not transactions:
            print(f"\nNo transactions found for {month}.")
            return
        
        headers = ['ID', 'Date', 'Amount', 'Category', 'Description', 'Type']
        rows = []
        for t in transactions:
            rows.append([
                t.get('id', ''),
                t.get('date', ''),
                format_currency(t.get('amount', 0)),
                t.get('category', ''),
                t.get('description', '')[:30],
                t.get('type', '')
            ])
        self.cli.print_table(headers, rows)
        
        # Summary for month
        summary = self.tm.get_monthly_summary(month)
        print(f"\nMonthly Summary:")
        print(f"  Income: {format_currency(summary['total_income'])}")
        print(f"  Expenses: {format_currency(summary['total_expenses'])}")
        print(f"  Balance: {format_currency(summary['balance'])}")
    
    def view_all_transactions(self) -> None:
        """View all transactions."""
        transactions = self.tm.get_all_transactions()
        
        self.cli.print_header("All Transactions")
        
        if not transactions:
            print("\nNo transactions found.")
            return
        
        headers = ['ID', 'Date', 'Amount', 'Category', 'Description', 'Type']
        rows = []
        for t in transactions:
            rows.append([
                t.get('id', ''),
                t.get('date', ''),
                format_currency(t.get('amount', 0)),
                t.get('category', ''),
                t.get('description', '')[:30],
                t.get('type', '')
            ])
        self.cli.print_table(headers, rows)
    
    # Export
    def export_menu(self) -> None:
        while True:
            self.cli.print_header("Export Data")
            
            options = [
                "Export All Transactions",
                "Export Expenses Only",
                "Export Income Only",
                "Export by Month",
                "List Previous Exports"
            ]
            self.cli.print_menu(options, "EXPORT")
            
            choice = self.cli.get_input("Enter choice")
            
            if choice == '1':
                self.export_mgr.export_all_transactions()
                self.cli.pause()
            elif choice == '2':
                self.export_mgr.export_transactions_by_type('expense')
                self.cli.pause()
            elif choice == '3':
                self.export_mgr.export_transactions_by_type('income')
                self.cli.pause()
            elif choice == '4':
                month_input = self.cli.get_input("Month (YYYY-MM) [current]", "")
                month = parse_month_input(month_input)
                self.export_mgr.export_transactions_by_month(month)
                self.cli.pause()
            elif choice == '5':
                self.list_exports()
                self.cli.pause()
            elif choice == '0':
                break
            else:
                print("Invalid option.")
    
    def list_exports(self) -> None:
        """List previous exports."""
        exports = self.export_mgr.list_exports()
        
        self.cli.print_header("Previous Exports")
        
        if not exports:
            print("\nNo previous exports found.")
            return
        
        for i, f in enumerate(exports, 1):
            print(f"  {i}. {f}")
    
    # Help
    def show_help(self) -> None:
        self.cli.print_header("Help")
        
        help_text = """
EXPENSEMATE - Personal Expense Management System

MAIN FEATURES:
1. Add Expense      - Record a new expense with date, amount, category, description
2. View Expenses    - List all expenses in a formatted table
3. Update Expense   - Modify existing expense details
4. Delete Expense   - Remove an expense (with confirmation)
5. Add Income       - Record income with source, amount, date
6. View Income      - List all income records
7. Update Income    - Modify existing income record
8. Delete Income    - Remove an income record (with confirmation)
9. Manage Budget    - Set monthly budgets, track spending, get warnings
10. Financial Summary - Overall totals: income, expenses, balance
11. Reports & Analytics:
    - Category-wise reports (expenses & income)
    - Monthly detailed reports with budget status
    - Spending analytics (highest category, average, largest transaction)
    - Monthly trends over 6 months
12. Search/Filter   - Filter by category, date range, amount range, keyword
13. Export Data     - Export transactions to CSV files
14. Help            - Show this help screen

VALIDATION RULES:
- Amount: Must be a positive number (> 0)
- Date: Must be in YYYY-MM-DD format
- Category: Select from predefined list or enter custom
- Budget: Monthly limit in YYYY-MM format

DATA STORAGE:
- All data stored locally in JSON files (data/transactions.json, data/budgets.json)
- Automatic file creation if missing
- Corrupted JSON handled gracefully

EXPORT:
- CSV files saved to exports/ directory
- Format: ID,Date,Amount,Category,Description,Type

TIPS:
- Use Tab completion for menu numbers
- Press Enter at date prompts to use today's date
- All destructive actions require confirmation
- Budget warnings appear at 80% usage
"""
        print(help_text)
        self.cli.pause()
    
    def exit_app(self) -> None:
        """Exit the application."""
        print("\nThank you for using ExpenseMate!")
        print("Your financial data has been saved.")
        sys.exit(0)


def main():
    """Application entry point."""
    app = ExpenseMateApp()
    app.run()


if __name__ == "__main__":
    main()
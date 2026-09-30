"""
Utils Module - Utility functions for CLI, formatting, and export.
"""

import csv
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from transaction_manager import TransactionManager


class CLIUtils:
    """Utility functions for CLI interaction."""
    
    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str) -> None:
        """Print a formatted header."""
        width = 50
        print("\n" + "=" * width)
        print(f"       {title.upper()}")
        print("=" * width)
    
    @staticmethod
    def print_menu(options: List[str], title: str = "MENU") -> None:
        """Print a numbered menu."""
        CLIUtils.print_header(title)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        print("0. Back / Exit")
        print("-" * 50)
    
    @staticmethod
    def get_input(prompt: str, default: str = "") -> str:
        """Get user input with optional default."""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        return input(prompt).strip()
    
    @staticmethod
    def confirm(prompt: str) -> bool:
        """Get yes/no confirmation."""
        response = input(f"{prompt} (y/n): ").strip().lower()
        return response in ['y', 'yes']
    
    @staticmethod
    def pause() -> None:
        """Pause for user to read output."""
        input("\nPress Enter to continue...")
    
    @staticmethod
    def print_table(headers: List[str], rows: List[List[str]], col_widths: Optional[List[int]] = None) -> None:
        """Print a formatted table."""
        if not rows:
            print("No data to display.")
            return
        
        if col_widths is None:
            # Calculate column widths
            col_widths = [len(h) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_row)
        print("-" * len(header_row))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)))


class ExportManager:
    """Handles exporting transactions to CSV."""
    
    def __init__(self, transaction_manager: TransactionManager, export_dir: str = "exports"):
        self.tm = transaction_manager
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def export_all_transactions(self, filename: Optional[str] = None) -> Optional[str]:
        """Export all transactions to CSV."""
        transactions = self.tm.get_all_transactions()
        return self._export_transactions(transactions, filename)
    
    def export_transactions_by_type(self, transaction_type: str, filename: Optional[str] = None) -> Optional[str]:
        """Export transactions filtered by type."""
        if transaction_type == 'expense':
            transactions = self.tm.get_expenses()
        elif transaction_type == 'income':
            transactions = self.tm.get_income()
        else:
            transactions = self.tm.get_all_transactions()
        return self._export_transactions(transactions, filename)
    
    def export_transactions_by_month(self, month: str, filename: Optional[str] = None) -> Optional[str]:
        """Export transactions for a specific month."""
        transactions = self.tm.get_transactions_by_month(month)
        return self._export_transactions(transactions, filename)
    
    def _export_transactions(self, transactions: List[Dict[str, Any]], filename: Optional[str] = None) -> Optional[str]:
        """Internal method to export transactions to CSV."""
        if not transactions:
            print("No transactions to export.")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"transactions_{timestamp}.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = self.export_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow(['ID', 'Date', 'Amount', 'Category', 'Description', 'Type'])
                # Data
                for t in transactions:
                    writer.writerow([
                        t.get('id', ''),
                        t.get('date', ''),
                        t.get('amount', 0),
                        t.get('category', ''),
                        t.get('description', ''),
                        t.get('type', '')
                    ])
            
            print(f"\nExported {len(transactions)} transactions to: {filepath}")
            return str(filepath)
        
        except PermissionError:
            print(f"Error: Permission denied writing to {filepath}")
            return None
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    def list_exports(self) -> List[str]:
        """List all exported files."""
        try:
            files = list(self.export_dir.glob("*.csv"))
            return [f.name for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)]
        except Exception:
            return []


def format_currency(amount: float) -> str:
    """Format amount as Indian Rupees."""
    return f"Rs.{amount:,.2f}"


def get_current_month() -> str:
    """Get current month in YYYY-MM format."""
    return datetime.now().strftime("%Y-%m")


def parse_month_input(month_str: str) -> str:
    """Parse and validate month input, default to current month."""
    if not month_str or not month_str.strip():
        return get_current_month()
    
    month_str = month_str.strip()
    # If only year-month provided, use as is
    if len(month_str) == 7 and month_str[4] == '-':
        return month_str
    
    # Try to parse various formats
    try:
        # Try YYYY-MM
        dt = datetime.strptime(month_str, "%Y-%m")
        return dt.strftime("%Y-%m")
    except ValueError:
        pass
    
    try:
        # Try MM-YYYY
        dt = datetime.strptime(month_str, "%m-%Y")
        return dt.strftime("%Y-%m")
    except ValueError:
        pass
    
    # Default to current month
    return get_current_month()


def sort_transactions(transactions: List[Dict[str, Any]], 
                      key: str = 'date', 
                      reverse: bool = True) -> List[Dict[str, Any]]:
    """Sort transactions by key."""
    return sorted(transactions, key=lambda x: x.get(key, ''), reverse=reverse)
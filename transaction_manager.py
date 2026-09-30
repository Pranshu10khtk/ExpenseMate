"""
Transaction Manager Module - Core transaction logic and ID generation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from storage import Storage
from validators import Validator


class TransactionManager:
    """Manages transaction operations - adding, updating, deleting, filtering."""
    
    def __init__(self, storage: Storage):
        self.storage = storage
        self.validator = Validator()
        self._expense_counter = 0
        self._income_counter = 0
        self._initialize_counters()
    
    def _initialize_counters(self) -> None:
        """Initialize ID counters based on existing transactions."""
        transactions = self.storage.get_all_transactions()
        max_expense = 0
        max_income = 0
        
        for t in transactions:
            tid = t.get('id', '')
            if tid.startswith('EXP'):
                try:
                    num = int(tid[3:])
                    max_expense = max(max_expense, num)
                except ValueError:
                    pass
            elif tid.startswith('INC'):
                try:
                    num = int(tid[3:])
                    max_income = max(max_income, num)
                except ValueError:
                    pass
        
        self._expense_counter = max_expense
        self._income_counter = max_income
    
    def _generate_expense_id(self) -> str:
        """Generate unique expense ID."""
        self._expense_counter += 1
        return f"EXP{self._expense_counter:03d}"
    
    def _generate_income_id(self) -> str:
        """Generate unique income ID."""
        self._income_counter += 1
        return f"INC{self._income_counter:03d}"
    
    def add_expense(self, date: str, amount: float, category: str, description: str = "") -> Dict[str, Any]:
        """Add a new expense transaction."""
        transaction = {
            'id': self._generate_expense_id(),
            'date': date,
            'amount': amount,
            'category': category,
            'description': description,
            'type': 'expense'
        }
        self.storage.add_transaction(transaction)
        return transaction
    
    def add_income(self, date: str, amount: float, category: str, description: str = "") -> Dict[str, Any]:
        """Add a new income transaction."""
        transaction = {
            'id': self._generate_income_id(),
            'date': date,
            'amount': amount,
            'category': category,
            'description': description,
            'type': 'income'
        }
        self.storage.add_transaction(transaction)
        return transaction
    
    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """Get all transactions."""
        return self.storage.get_all_transactions()
    
    def get_expenses(self) -> List[Dict[str, Any]]:
        """Get all expense transactions."""
        transactions = self.get_all_transactions()
        return [t for t in transactions if t.get('type') == 'expense']
    
    def get_income(self) -> List[Dict[str, Any]]:
        """Get all income transactions."""
        transactions = self.get_all_transactions()
        return [t for t in transactions if t.get('type') == 'income']
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get a transaction by ID."""
        return self.storage.get_transaction_by_id(transaction_id)
    
    def update_transaction(self, transaction_id: str, **kwargs) -> bool:
        """Update a transaction."""
        # Filter valid fields
        valid_fields = ['date', 'amount', 'category', 'description']
        update_data = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
        
        if not update_data:
            return False
        
        return self.storage.update_transaction(transaction_id, update_data)
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction."""
        return self.storage.delete_transaction(transaction_id)
    
    def filter_transactions(self, 
                           transaction_type: Optional[str] = None,
                           category: Optional[str] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           min_amount: Optional[float] = None,
                           max_amount: Optional[float] = None,
                           keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Filter transactions based on multiple criteria.
        All filters are optional and combined with AND logic.
        """
        transactions = self.get_all_transactions()
        filtered = []
        
        for t in transactions:
            # Type filter
            if transaction_type and t.get('type') != transaction_type:
                continue
            
            # Category filter (case-insensitive)
            if category and t.get('category', '').lower() != category.lower():
                continue
            
            # Date range filter
            t_date = t.get('date', '')
            if start_date and t_date < start_date:
                continue
            if end_date and t_date > end_date:
                continue
            
            # Amount range filter
            t_amount = t.get('amount', 0)
            if min_amount is not None and t_amount < min_amount:
                continue
            if max_amount is not None and t_amount > max_amount:
                continue
            
            # Keyword search in description
            if keyword and keyword.lower() not in t.get('description', '').lower():
                continue
            
            filtered.append(t)
        
        # Sort by date descending (newest first)
        filtered.sort(key=lambda x: x.get('date', ''), reverse=True)
        return filtered
    
    def search_transactions(self, keyword: str) -> List[Dict[str, Any]]:
        """Search transactions by keyword in description or category."""
        return self.filter_transactions(keyword=keyword)
    
    def get_transactions_by_month(self, month: str) -> List[Dict[str, Any]]:
        """Get all transactions for a specific month (YYYY-MM)."""
        transactions = self.get_all_transactions()
        return [t for t in transactions if t.get('date', '').startswith(month)]
    
    def get_expenses_by_month(self, month: str) -> List[Dict[str, Any]]:
        """Get expenses for a specific month."""
        return [t for t in self.get_transactions_by_month(month) if t.get('type') == 'expense']
    
    def get_income_by_month(self, month: str) -> List[Dict[str, Any]]:
        """Get income for a specific month."""
        return [t for t in self.get_transactions_by_month(month) if t.get('type') == 'income']
    
    def calculate_total_expenses(self, transactions: Optional[List[Dict[str, Any]]] = None) -> float:
        """Calculate total expenses from a list of transactions."""
        if transactions is None:
            transactions = self.get_expenses()
        return sum(t.get('amount', 0) for t in transactions)
    
    def calculate_total_income(self, transactions: Optional[List[Dict[str, Any]]] = None) -> float:
        """Calculate total income from a list of transactions."""
        if transactions is None:
            transactions = self.get_income()
        return sum(t.get('amount', 0) for t in transactions)
    
    def calculate_balance(self) -> float:
        """Calculate current balance (income - expenses)."""
        return self.calculate_total_income() - self.calculate_total_expenses()
    
    def get_category_totals(self, transaction_type: str = 'expense') -> Dict[str, float]:
        """Get spending totals by category."""
        transactions = self.get_expenses() if transaction_type == 'expense' else self.get_income()
        totals = {}
        for t in transactions:
            cat = t.get('category', 'Other')
            totals[cat] = totals.get(cat, 0) + t.get('amount', 0)
        return totals
    
    def get_monthly_summary(self, month: str) -> Dict[str, Any]:
        """Get financial summary for a specific month."""
        expenses = self.get_expenses_by_month(month)
        income = self.get_income_by_month(month)
        
        total_expenses = sum(t.get('amount', 0) for t in expenses)
        total_income = sum(t.get('amount', 0) for t in income)
        
        return {
            'month': month,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses,
            'transaction_count': len(expenses) + len(income),
            'expense_count': len(expenses),
            'income_count': len(income)
        }
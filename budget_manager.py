"""
Budget Manager Module - Monthly budget management and tracking.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from storage import Storage
from transaction_manager import TransactionManager
from validators import Validator


class BudgetManager:
    """Manages monthly budgets and tracks spending against them."""
    
    def __init__(self, storage: Storage, transaction_manager: TransactionManager):
        self.storage = storage
        self.transaction_manager = transaction_manager
        self.validator = Validator()
        # Budget threshold for warnings (percentage)
        self.warning_threshold = 80.0
    
    def set_budget(self, month: str, amount: float) -> bool:
        """Set or update budget for a month."""
        return self.storage.add_or_update_budget(month, amount)
    
    def get_budget(self, month: str) -> Optional[Dict[str, Any]]:
        """Get budget for a month."""
        return self.storage.get_budget(month)
    
    def get_current_month_budget(self) -> Optional[Dict[str, Any]]:
        """Get budget for current month."""
        current_month = datetime.now().strftime("%Y-%m")
        return self.get_budget(current_month)
    
    def delete_budget(self, month: str) -> bool:
        """Delete budget for a month."""
        return self.storage.delete_budget(month)
    
    def get_all_budgets(self) -> List[Dict[str, Any]]:
        """Get all budgets."""
        return self.storage.get_all_budgets()
    
    def calculate_budget_status(self, month: str) -> Dict[str, Any]:
        """
        Calculate budget usage status for a month.
        Returns dict with budget info, expenses, remaining, percentage, status.
        """
        budget_data = self.get_budget(month)
        if not budget_data:
            return {
                'has_budget': False,
                'month': month,
                'message': 'No budget has been configured for this month.'
            }
        
        budget_amount = budget_data.get('amount', 0)
        expenses = self.transaction_manager.get_expenses_by_month(month)
        total_expenses = sum(e.get('amount', 0) for e in expenses)
        remaining = budget_amount - total_expenses
        
        if budget_amount > 0:
            percentage_used = (total_expenses / budget_amount) * 100
        else:
            percentage_used = 0
        
        # Determine status
        if total_expenses > budget_amount:
            status = "EXCEEDED"
            message = f"WARNING: Monthly budget exceeded!\nBudget: ₹{budget_amount:,.2f}\nExpenses: ₹{total_expenses:,.2f}\nExceeded By: ₹{abs(remaining):,.2f}"
        elif percentage_used >= self.warning_threshold:
            status = "WARNING"
            message = f"WARNING: Budget usage at {percentage_used:.1f}% (threshold: {self.warning_threshold}%)"
        else:
            status = "WITHIN_BUDGET"
            message = f"Status: Within Budget ({percentage_used:.1f}% used)"
        
        return {
            'has_budget': True,
            'month': month,
            'budget_amount': budget_amount,
            'total_expenses': total_expenses,
            'remaining': remaining,
            'percentage_used': percentage_used,
            'status': status,
            'message': message,
            'transaction_count': len(expenses)
        }
    
    def get_budget_summary(self, month: Optional[str] = None) -> Dict[str, Any]:
        """Get formatted budget summary for display."""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        status = self.calculate_budget_status(month)
        return status
    
    def check_budget_alert(self, month: Optional[str] = None) -> Optional[str]:
        """Check if budget alert should be shown."""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        status = self.calculate_budget_status(month)
        if status.get('has_budget') and status.get('status') in ['WARNING', 'EXCEEDED']:
            return status.get('message')
        return None
"""
Validators Module - Input validation for amounts, dates, categories, and menu choices.
"""

import re
from datetime import datetime
from typing import Optional, List, Tuple


class Validator:
    """Handles all input validation for the application."""
    
    # Predefined categories
    EXPENSE_CATEGORIES = [
        "Food", "Travel", "Shopping", "Education", "Health",
        "Entertainment", "Bills", "Rent", "Transportation", "Other"
    ]
    
    INCOME_CATEGORIES = [
        "Salary", "Freelance", "Investment", "Gift", "Refund", "Other"
    ]
    
    ALL_CATEGORIES = EXPENSE_CATEGORIES + INCOME_CATEGORIES
    
    @staticmethod
    def validate_amount(amount_str: str) -> Tuple[bool, Optional[float], str]:
        """
        Validate amount input.
        Returns: (is_valid, amount_value, error_message)
        """
        if not amount_str or not amount_str.strip():
            return False, None, "Amount cannot be empty."
        
        try:
            amount = float(amount_str.strip())
        except ValueError:
            return False, None, "Amount must be a valid number."
        
        if amount <= 0:
            return False, None, "Amount must be greater than zero."
        
        return True, amount, ""
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, Optional[str], str]:
        """
        Validate date in YYYY-MM-DD format.
        Returns: (is_valid, normalized_date, error_message)
        """
        if not date_str or not date_str.strip():
            return False, None, "Date cannot be empty."
        
        date_str = date_str.strip()
        
        # Check format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return False, None, "Date must be in YYYY-MM-DD format."
        
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            # Return normalized date string
            return True, parsed_date.strftime("%Y-%m-%d"), ""
        except ValueError:
            return False, None, "Invalid date. Please enter a valid date in YYYY-MM-DD format."
    
    @staticmethod
    def validate_category(category: str, transaction_type: str = "expense") -> Tuple[bool, str, str]:
        """
        Validate category.
        Returns: (is_valid, normalized_category, error_message)
        """
        if not category or not category.strip():
            return False, "", "Category cannot be empty."
        
        category = category.strip()
        
        # Get valid categories based on transaction type
        if transaction_type == "income":
            valid_categories = Validator.INCOME_CATEGORIES
        else:
            valid_categories = Validator.EXPENSE_CATEGORIES
        
        # Case-insensitive match
        for valid_cat in valid_categories:
            if category.lower() == valid_cat.lower():
                return True, valid_cat, ""
        
        # If not in predefined list, allow custom but warn
        valid_list = ", ".join(valid_categories)
        return True, category, f"Note: '{category}' is not a standard category. Standard categories: {valid_list}"
    
    @staticmethod
    def validate_description(description: str) -> Tuple[bool, str, str]:
        """
        Validate description (optional).
        Returns: (is_valid, normalized_description, error_message)
        """
        if description is None:
            return True, "", ""
        return True, description.strip(), ""
    
    @staticmethod
    def validate_menu_choice(choice: str, valid_choices: List[str]) -> Tuple[bool, str, str]:
        """
        Validate menu choice.
        Returns: (is_valid, choice, error_message)
        """
        if not choice or not choice.strip():
            return False, "", "Please enter a menu option."
        
        choice = choice.strip()
        
        if choice not in valid_choices:
            return False, "", f"Invalid option. Please choose from: {', '.join(valid_choices)}"
        
        return True, choice, ""
    
    @staticmethod
    def validate_transaction_id(transaction_id: str, transactions: List[dict]) -> Tuple[bool, str, str]:
        """
        Validate transaction ID exists.
        Returns: (is_valid, transaction_id, error_message)
        """
        if not transaction_id or not transaction_id.strip():
            return False, "", "Transaction ID cannot be empty."
        
        transaction_id = transaction_id.strip().upper()
        
        for t in transactions:
            if t.get('id', '').upper() == transaction_id:
                return True, transaction_id, ""
        
        return False, "", f"Transaction with ID '{transaction_id}' not found."
    
    @staticmethod
    def validate_month(month_str: str) -> Tuple[bool, Optional[str], str]:
        """
        Validate month in YYYY-MM format.
        Returns: (is_valid, normalized_month, error_message)
        """
        if not month_str or not month_str.strip():
            # Default to current month
            current_month = datetime.now().strftime("%Y-%m")
            return True, current_month, ""
        
        month_str = month_str.strip()
        
        if not re.match(r'^\d{4}-\d{2}$', month_str):
            return False, None, "Month must be in YYYY-MM format."
        
        try:
            parsed = datetime.strptime(month_str, "%Y-%m")
            return True, parsed.strftime("%Y-%m"), ""
        except ValueError:
            return False, None, "Invalid month."
    
    @staticmethod
    def validate_confirmation(confirm: str) -> bool:
        """Validate yes/no confirmation."""
        return confirm.strip().lower() in ['y', 'yes']
    
    @staticmethod
    def get_category_choices(transaction_type: str = "expense") -> List[str]:
        """Get list of valid categories for display."""
        if transaction_type == "income":
            return Validator.INCOME_CATEGORIES
        return Validator.EXPENSE_CATEGORIES
"""
Storage Module - Handles JSON file persistence for transactions and budgets.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class Storage:
    """Handles reading and writing data to JSON files."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.transactions_file = self.data_dir / "transactions.json"
        self.budgets_file = self.data_dir / "budgets.json"
        self._ensure_data_files()
    
    def _ensure_data_files(self) -> None:
        """Create data directory and files if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.transactions_file.exists():
            self._write_json(self.transactions_file, [])
        
        if not self.budgets_file.exists():
            self._write_json(self.budgets_file, [])
    
    def _read_json(self, file_path: Path) -> List[Dict[Any, Any]]:
        """Read JSON file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Warning: Corrupted JSON in {file_path.name}. Starting fresh. Error: {e}")
            return []
        except PermissionError:
            print(f"Error: Permission denied reading {file_path.name}")
            return []
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
            return []
    
    def _write_json(self, file_path: Path, data: List[Dict[Any, Any]]) -> bool:
        """Write JSON file with error handling."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: Permission denied writing to {file_path.name}")
            return False
        except Exception as e:
            print(f"Error writing to {file_path.name}: {e}")
            return False
    
    # Transaction methods
    def get_all_transactions(self) -> List[Dict[Any, Any]]:
        """Get all transactions from storage."""
        return self._read_json(self.transactions_file)
    
    def save_transactions(self, transactions: List[Dict[Any, Any]]) -> bool:
        """Save all transactions to storage."""
        return self._write_json(self.transactions_file, transactions)
    
    def add_transaction(self, transaction: Dict[Any, Any]) -> bool:
        """Add a single transaction."""
        transactions = self.get_all_transactions()
        transactions.append(transaction)
        return self.save_transactions(transactions)
    
    def update_transaction(self, transaction_id: str, updated_data: Dict[Any, Any]) -> bool:
        """Update a transaction by ID."""
        transactions = self.get_all_transactions()
        for i, t in enumerate(transactions):
            if t.get('id') == transaction_id:
                transactions[i].update(updated_data)
                return self.save_transactions(transactions)
        return False
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction by ID."""
        transactions = self.get_all_transactions()
        original_len = len(transactions)
        transactions = [t for t in transactions if t.get('id') != transaction_id]
        if len(transactions) < original_len:
            return self.save_transactions(transactions)
        return False
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict[Any, Any]]:
        """Get a single transaction by ID."""
        transactions = self.get_all_transactions()
        for t in transactions:
            if t.get('id') == transaction_id:
                return t
        return None
    
    # Budget methods
    def get_all_budgets(self) -> List[Dict[Any, Any]]:
        """Get all budgets from storage."""
        return self._read_json(self.budgets_file)
    
    def save_budgets(self, budgets: List[Dict[Any, Any]]) -> bool:
        """Save all budgets to storage."""
        return self._write_json(self.budgets_file, budgets)
    
    def add_or_update_budget(self, month: str, amount: float) -> bool:
        """Add or update budget for a month."""
        budgets = self.get_all_budgets()
        for b in budgets:
            if b.get('month') == month:
                b['amount'] = amount
                return self.save_budgets(budgets)
        budgets.append({'month': month, 'amount': amount})
        return self.save_budgets(budgets)
    
    def get_budget(self, month: str) -> Optional[Dict[Any, Any]]:
        """Get budget for a specific month."""
        budgets = self.get_all_budgets()
        for b in budgets:
            if b.get('month') == month:
                return b
        return None
    
    def delete_budget(self, month: str) -> bool:
        """Delete budget for a month."""
        budgets = self.get_all_budgets()
        original_len = len(budgets)
        budgets = [b for b in budgets if b.get('month') != month]
        if len(budgets) < original_len:
            return self.save_budgets(budgets)
        return False
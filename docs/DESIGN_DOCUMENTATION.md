# ExpenseMate - Design Documentation

This document provides an overview of all design diagrams and their correspondence to the actual implementation.

---

## Diagram Inventory

| # | Diagram | Source File | Format | Description |
|---|---------|-------------|--------|-------------|
| 1 | System Architecture | `architecture.mmd` | Mermaid | Layered architecture, data flows |
| 2 | Workflow | `workflow.mmd` | Mermaid | Application workflows (startup, CRUD, budget, reports, search, export) |
| 3 | Use Case | `use_case.mmd` | Mermaid | User interactions (15 use cases) |
| 4 | Class Diagram | `class_diagram.mmd` | Mermaid | 12 classes, 5 layers, relationships |
| 5 | Sequence (Add Expense) | `sequence_add_expense.mmd` | Mermaid | Detailed interaction for adding expense |
| 6 | Storage/Schema | `storage_schema.mmd` | Mermaid | JSON structures, ID generation, relationships |

---

## Correspondence to Code

### Architecture Diagram → Code Structure

| Layer | Diagram Component | Actual File/Class |
|-------|-------------------|-------------------|
| Presentation | CLI Interface | `main.py` |
| Presentation | CLI Utilities | `utils.CLIUtils` |
| Controller | ExpenseMateApp | `main.ExpenseMateApp` |
| Business | ExpenseManager | `expense_manager.ExpenseManager` |
| Business | IncomeManager | `income_manager.IncomeManager` |
| Business | BudgetManager | `budget_manager.BudgetManager` |
| Business | ReportManager | `report_manager.ReportManager` |
| Core | TransactionManager | `transaction_manager.TransactionManager` |
| Validation | Validator | `validators.Validator` |
| Data Access | Storage | `storage.Storage` |
| Persistence | transactions.json | `data/transactions.json` |
| Persistence | budgets.json | `data/budgets.json` |
| Export | ExportManager | `utils.ExportManager` |
| Export | exports/*.csv | `exports/` directory |

### Workflow Diagram → Menu Options

| Menu Option | Workflow Subgraph | Handler Method |
|-------------|-------------------|----------------|
| 1. Add Expense | AddExp | `app.add_expense()` → `expense_mgr.add_expense_interactive()` |
| 2. View Expenses | ViewExp | `app.view_expenses()` → `expense_mgr.view_expenses()` |
| 3. Update Expense | UpdExp | `app.update_expense()` → `expense_mgr.update_expense_interactive()` |
| 4. Delete Expense | DelExp | `app.delete_expense()` → `expense_mgr.delete_expense_interactive()` |
| 5. Add Income | AddInc | `app.add_income()` → `income_mgr.add_income_interactive()` |
| 6. View Income | ViewInc | `app.view_income()` → `income_mgr.view_income()` |
| 7. Update Income | UpdInc | `app.update_income()` → `income_mgr.update_income_interactive()` |
| 8. Delete Income | DelInc | `app.delete_income()` → `income_mgr.delete_income_interactive()` |
| 9. Manage Budget | Bud | `app.manage_budget()` |
| 10. Financial Summary | Sum | `app.show_financial_summary()` → `report_mgr.print_financial_summary()` |
| 11. Reports & Analytics | Rep | `app.show_reports_menu()` |
| 12. Search/Filter | Search | `app.search_filter_menu()` |
| 13. Export Data | Exp | `app.export_menu()` |
| 14. Help | Help | `app.show_help()` |
| 0. Exit | Exit | `app.exit_app()` |

### Use Case Diagram → Menu Mapping

| Use Case | Menu Option | Implemented In |
|----------|-------------|----------------|
| Add Expense | 1 | `ExpenseManager.add_expense_interactive()` |
| View Expenses | 2 | `ExpenseManager.view_expenses()` |
| Update Expense | 3 | `ExpenseManager.update_expense_interactive()` |
| Delete Expense | 4 | `ExpenseManager.delete_expense_interactive()` |
| Add Income | 5 | `IncomeManager.add_income_interactive()` |
| View Income | 6 | `IncomeManager.view_income()` |
| Update Income | 7 | `IncomeManager.update_income_interactive()` |
| Delete Income | 8 | `IncomeManager.delete_income_interactive()` |
| Manage Budget | 9 | `BudgetManager` + `app.manage_budget()` |
| Financial Summary | 10 | `ReportManager.print_financial_summary()` |
| Generate Reports | 11 | `ReportManager` (5 report types) |
| Search/Filter | 12 | `TransactionManager.filter_transactions()` + `app.search_filter_menu()` |
| Export Data | 13 | `ExportManager` + `app.export_menu()` |
| View Help | 14 | `app.show_help()` |
| Exit Application | 0 | `app.exit_app()` |

### Class Diagram → Actual Classes

| Class | File | Key Methods (subset) |
|-------|------|---------------------|
| ExpenseMateApp | `main.py` | `run()`, `handle_main_menu()`, 15+ handlers |
| CLIUtils | `utils.py` | `print_header()`, `print_menu()`, `get_input()`, `print_table()` |
| ExpenseManager | `expense_manager.py` | `add_expense_interactive()`, `view_expenses()`, `update_expense_interactive()`, `delete_expense_interactive()`, `filter_expenses_interactive()` |
| IncomeManager | `income_manager.py` | `add_income_interactive()`, `view_income()`, `update_income_interactive()`, `delete_income_interactive()` |
| BudgetManager | `budget_manager.py` | `set_budget()`, `calculate_budget_status()`, `check_budget_alert()` |
| ReportManager | `report_manager.py` | `get_overall_summary()`, `get_category_report()`, `get_monthly_report()`, `print_analytics()` |
| TransactionManager | `transaction_manager.py` | `add_expense()`, `add_income()`, `filter_transactions()`, `calculate_total_expenses()`, `_generate_expense_id()` |
| Storage | `storage.py` | `get_all_transactions()`, `add_transaction()`, `_read_json()`, `_write_json()` |
| Validator | `validators.py` | `validate_amount()`, `validate_date()`, `validate_category()`, `validate_transaction_id()` |
| ExportManager | `utils.py` | `export_all_transactions()`, `export_transactions_by_type()`, `export_transactions_by_month()` |

### Sequence Diagram → Add Expense Code Path

| Sequence Step | Code Location |
|---------------|---------------|
| User selects "1. Add Expense" | `main.py:80` `menu_actions['1']` → `app.add_expense()` |
| CLI → ExpenseManager | `main.py:105` `app.expense_mgr.add_expense_interactive()` |
| Prompt Date | `expense_manager.py:25` `cli.get_input("Date (YYYY-MM-DD)")` |
| Validate Date | `expense_manager.py:30` `validator.validate_date()` |
| Prompt Amount | `expense_manager.py:37` `cli.get_input("Amount")` |
| Validate Amount | `expense_manager.py:38` `validator.validate_amount()` |
| Show Categories | `expense_manager.py:44-48` `validator.get_category_choices('expense')` |
| Prompt Category | `expense_manager.py:51` `cli.get_input("Select category")` |
| Validate Category | `expense_manager.py:65` `validator.validate_category(cat, 'expense')` |
| Prompt Description | `expense_manager.py:71` `cli.get_input("Description")` |
| Generate ID + Save | `expense_manager.py:74` `tm.add_expense(date, amount, category, description)` |
| TransactionManager.add_expense | `transaction_manager.py:49` creates dict, calls `storage.add_transaction()` |
| Storage.add_transaction | `storage.py:47` reads file, appends, writes back |
| Success Message | `expense_manager.py:75` prints ID |

### Storage Schema → JSON Files

| Schema Entity | JSON File | Actual Structure |
|---------------|-----------|------------------|
| TRANSACTION | `data/transactions.json` | Array of objects with id, date, amount, category, description, type |
| BUDGET | `data/budgets.json` | Array of objects with month, amount |

**Sample Data from Code:**
```python
# Expense (transaction_manager.py:49-57)
{
    'id': 'EXP001',
    'date': '2026-09-30',
    'amount': 450.0,
    'category': 'Food',
    'description': 'Dinner',
    'type': 'expense'
}

# Income (transaction_manager.py:60-68)
{
    'id': 'INC001',
    'date': '2026-09-30',
    'amount': 25000.0,
    'category': 'Salary',
    'description': 'Monthly income',
    'type': 'income'
}

# Budget (storage.py:63-66)
{
    'month': '2026-09',
    'amount': 20000.0
}
```

---

## How to View Diagrams

### VS Code
1. Install "Markdown Preview Mermaid Support" extension
2. Open `.mmd` files or this documentation
3. Press `Ctrl+Shift+V` for preview

### GitHub/GitLab
- Mermaid renders natively in Markdown files
- Just push `.mmd` files or include in Markdown

### Mermaid CLI
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i architecture.mmd -o architecture.png
```

### Online
- https://mermaid.live - Paste Mermaid code for instant preview

---

## Validation Checklist

- [x] All diagrams use only classes/modules that exist in code
- [x] No invented relationships or methods
- [x] Method names match actual implementation
- [x] File names match actual project structure
- [x] Data structures match actual JSON format
- [x] Menu options correspond to actual main menu
- [x] Error handling flows match validation logic
- [x] ID generation logic matches TransactionManager

---

## Maintenance

When modifying code:
1. Update corresponding diagram(s)
2. Keep diagram filenames consistent
3. Run `python -m unittest discover` to ensure code still works
4. Verify diagrams still render correctly

Diagrams are in `docs/diagrams/` as `.mmd` (Mermaid) files.
Original PlantUML files (`.puml`) preserved for reference.
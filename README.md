# ExpenseMate – Personal Expense Management System

## Overview

**ExpenseMate** is a command-line personal finance management system developed using Python. It helps users record income and expenses, manage budgets, track financial balances, and generate spending reports using locally stored data.

This project demonstrates core Python programming concepts including file handling, JSON serialization, exception handling, modular design, and object-oriented programming.

---

## Problem Statement

Manually tracking personal expenses and budgets is error-prone, time-consuming, and makes it difficult to analyze spending patterns. People often lose track of where their money goes, overspend without realizing it, and lack clear visibility into their financial health. ExpenseMate solves this by providing a structured, persistent, and easy-to-use system for managing personal finances.

---

## Objectives

- ✅ Manage income and expense records with full CRUD operations
- ✅ Track monthly budgets with real-time spending alerts
- ✅ Generate comprehensive financial reports and analytics
- ✅ Provide flexible search and filter capabilities
- ✅ Maintain persistent local data storage using JSON
- ✅ Export data to CSV for external analysis
- ✅ Implement robust input validation and error handling
- ✅ Follow modular, clean code architecture suitable for learning

---

## Features

### Expense Management
- Add, view, update, delete expenses
- View expense details by ID
- Filter by category, date range, amount range
- Search by keyword in description

### Income Management
- Add, view, update, delete income records
- Filter by source/category, date range
- Track multiple income sources

### Budget Management
- Set monthly budget limits
- Real-time budget tracking with percentage used
- Warning at 80% threshold
- Alert when budget exceeded

### Reports & Analytics
- Overall financial summary (income, expenses, balance)
- Category-wise spending reports with percentages
- Monthly detailed reports with budget status
- Highest spending category identification
- Average expense calculation
- Largest transaction detection
- Expense distribution visualization
- 6-month trend analysis

### Search & Filter
- Filter by transaction type (income/expense)
- Filter by category
- Filter by date range
- Filter by amount range
- Keyword search in descriptions

### Data Export
- Export all transactions to CSV
- Export filtered views (expenses only, income only, by month)
- Automatic exports directory management

### Data Persistence
- JSON-based local storage
- Automatic file/directory creation
- Corrupted JSON handling
- Graceful error recovery

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core programming language |
| JSON | Data persistence |
| CSV | Data export |
| unittest | Unit testing |
| datetime | Date/time handling |
| pathlib | Cross-platform file paths |

No external dependencies required – uses only Python standard library.

---

## Project Structure

```
ExpenseMate/
├── main.py                 # Application entry point
├── storage.py              # JSON file persistence layer
├── transaction_manager.py  # Core transaction logic
├── expense_manager.py      # Expense-specific operations
├── income_manager.py       # Income-specific operations
├── budget_manager.py       # Budget tracking & alerts
├── report_manager.py       # Reports & analytics
├── validators.py           # Input validation
├── utils.py                # CLI utilities & export
├── requirements.txt        # Python version requirement
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # This file
├── statement.md            # Project statement
├── data/
│   ├── transactions.json   # Transaction storage
│   └── budgets.json        # Budget storage
├── exports/                # Generated CSV exports
├── tests/
│   ├── __init__.py
│   ├── test_validators.py
│   ├── test_expense_manager.py
│   ├── test_income_manager.py
│   ├── test_budget_manager.py
│   └── test_reports.py
└── docs/
    ├── architecture.md
    ├── workflow.md
    ├── diagrams/
    ├── PROJECT_REPORT_CONTENT.md
    ├── SCREENSHOT_CHECKLIST.md
    └── DEMO_FLOW.md
```

---

## Requirements

- **Python 3.9 or higher** (uses f-strings, pathlib, type hints)

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ExpenseMate

# (Optional) Create virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux/macOS:
python3 -m venv venv
source venv/bin/activate
```

---

## Running the Application

```bash
python main.py
```

The application will start and display the main menu. Navigate using number keys.

---

## Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test module
python -m unittest tests.test_validators
python -m unittest tests.test_expense_manager
python -m unittest tests.test_budget_manager
python -m unittest tests.test_reports

# Run with verbose output
python -m unittest discover -v
```

---

## Data Storage

ExpenseMate uses local JSON files for persistence:

- **data/transactions.json** – All income and expense records
- **data/budgets.json** – Monthly budget limits

Files are automatically created on first run. The application handles:
- Missing files (creates empty arrays)
- Empty files (treats as empty arrays)
- Corrupted JSON (shows warning, starts fresh)

---

## Export

Export transactions to CSV format:

```
ID,Date,Amount,Category,Description,Type
EXP001,2026-09-01,1200.0,Food,Monthly groceries,expense
INC001,2026-09-01,25000.0,Salary,Monthly salary,income
```

Files are saved to `exports/transactions_YYYY-MM-DD.csv`

---

## Example Usage

```text
==================================================
        EXPENSEMATE
   Personal Expense Management System
==================================================

1. Add Expense
2. View Expenses
3. Update Expense
4. Delete Expense
5. Add Income
6. View Income
7. Update Income
8. Delete Income
9. Manage Budget
10. Financial Summary
11. Reports & Analytics
12. Search / Filter Transactions
13. Export Data
14. Help
0. Exit

Enter your choice: 1

==================================================
          ADD EXPENSE
==================================================

Date (YYYY-MM-DD) [2026-09-30]: 
Amount: 450
Select category (number or name):
  1. Food
  2. Travel
  ...
  11. Custom category
Category: 1
Description (optional): Lunch with friends

✓ Expense added successfully! (ID: EXP011)
```

---

## Error Handling

ExpenseMate implements comprehensive error handling:

| Error Type | Handling |
|------------|----------|
| Invalid amount (negative, zero, non-numeric) | Clear message, re-prompt |
| Invalid date format | Format guidance, re-prompt |
| Empty required fields | Validation message, re-prompt |
| Missing transaction ID | Not found message |
| Corrupted JSON files | Warning + fresh start |
| Permission errors | User-friendly message |
| Keyboard interrupt | Clean exit |

The application never crashes due to normal user input errors.

---

## Future Enhancements

- [ ] SQLite database backend
- [ ] Graphical user interface (tkinter/PyQt)
- [ ] Web version with Flask/FastAPI
- [ ] User authentication & multi-user support
- [ ] Recurring expenses/income
- [ ] Advanced analytics & charts (matplotlib)
- [ ] Cloud synchronization
- [ ] Mobile application
- [ ] Multiple currency support
- [ ] Automated monthly report emails
- [ ] Expense categorization via ML
- [ ] Receipt scanning (OCR)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Academic Context

This project was developed as part of a **Python Essentials college course project**. It demonstrates:

- Modular Python architecture (8+ modules)
- Object-oriented design with separation of concerns
- File I/O with JSON and CSV
- Exception handling and input validation
- Unit testing with unittest
- CLI application design
- Documentation and design artifacts

---

## Author

Developed as a Python Essentials course project.
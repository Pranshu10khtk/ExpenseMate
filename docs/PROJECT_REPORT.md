# ExpenseMate – Project Report

## Personal Expense Management System

---

## 1. Executive Summary

**ExpenseMate** is a command-line personal finance management system developed in Python as part of a Python Essentials college course project. The application enables users to track income and expenses, manage monthly budgets, generate detailed financial reports, and export data for external analysis—all with persistent local storage using JSON files.

### Key Highlights
- **Zero external dependencies** – Built entirely with Python standard library
- **Modular architecture** – 8+ modules following separation of concerns
- **Comprehensive testing** – 5 test modules with 60+ unit tests
- **Robust error handling** – Graceful degradation for all user inputs
- **Full CRUD operations** – Create, Read, Update, Delete for all entities

---

## 2. Problem Statement

Manually tracking personal expenses and budgets is error-prone, time-consuming, and makes it difficult to analyze spending patterns. People often lose track of where their money goes, overspend without realizing it, and lack clear visibility into their financial health.

**ExpenseMate solves this by providing:**
- Structured transaction recording with validation
- Real-time budget tracking with threshold alerts
- Comprehensive analytics and reporting
- Persistent local storage with corruption recovery
- Export capabilities for external analysis

---

## 3. Objectives & Achievements

| Objective | Status | Implementation |
|-----------|--------|----------------|
| Manage income/expense records with full CRUD | ✅ Complete | `ExpenseManager`, `IncomeManager`, `TransactionManager` |
| Track monthly budgets with real-time alerts | ✅ Complete | `BudgetManager` with 80% warning, 100% exceeded |
| Generate comprehensive financial reports | ✅ Complete | `ReportManager` with 5 report types |
| Flexible search and filter capabilities | ✅ Complete | `TransactionManager.filter_transactions()` |
| Persistent local JSON storage | ✅ Complete | `Storage` class with error recovery |
| Export data to CSV | ✅ Complete | `ExportManager` with multiple export options |
| Robust input validation | ✅ Complete | `Validator` class with 10+ validation methods |
| Modular, clean code architecture | ✅ Complete | 8 modules, dependency injection, SRP |

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────┐
│    USER     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CLI MENU   │  (main.py)
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  APPLICATION CTRL   │  (ExpenseMateApp)
└───────────┬─────────┘
            │
    ┌───────┼───────┬──────────┐
    ▼       ▼       ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│Expense │ │Income│ │Budget  │ │Report  │
│Manager │ │Manager│ │Manager │ │Manager │
└───┬────┘ └──┬───┘ └────┬───┘ └────┬───┘
    │         │          │          │
    └─────────┼──────────┼──────────┘
              ▼
     ┌─────────────────┐
     │TransactionManager│
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │    STORAGE      │  (JSON files)
     └────────┬────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌─────────┐         ┌─────────┐
│transactions│       │budgets  │
│.json    │         │.json    │
└─────────┘         └─────────┘
```

### 4.2 Module Responsibilities

| Layer | Module | File | Responsibility |
|-------|--------|------|----------------|
| **Presentation** | CLI Interface | `main.py` | Entry point, menu navigation, app loop |
| **Presentation** | CLI Utilities | `utils.CLIUtils` | Screen clearing, menus, input, tables |
| **Controller** | ExpenseMateApp | `main.py` | Orchestrates all managers, routes requests |
| **Business** | ExpenseManager | `expense_manager.py` | Expense CRUD, interactive prompts |
| **Business** | IncomeManager | `income_manager.py` | Income CRUD, interactive prompts |
| **Business** | BudgetManager | `budget_manager.py` | Budget CRUD, threshold calculations |
| **Business** | ReportManager | `report_manager.py` | Reports, analytics, formatting |
| **Core** | TransactionManager | `transaction_manager.py` | Core logic, filtering, ID generation |
| **Validation** | Validator | `validators.py` | All input validation |
| **Data Access** | Storage | `storage.py` | JSON read/write, error handling |
| **Utility** | ExportManager | `utils.py` | CSV export functionality |
| **Utility** | Helpers | `utils.py` | Currency formatting, date parsing |

### 4.3 Design Patterns Applied

1. **Single Responsibility Principle** – Each class has one clear purpose
2. **Dependency Injection** – Managers receive dependencies via constructor
3. **Separation of Concerns** – Validation, storage, business logic isolated
4. **Factory Pattern** – `TransactionManager` generates sequential IDs
5. **Repository Pattern** – `Storage` abstracts file operations

---

## 5. Features Implemented

### 5.1 Expense Management
- ✅ Add expense with date, amount, category, description
- ✅ View all expenses in formatted table
- ✅ Update expense (partial or full)
- ✅ Delete expense with confirmation
- ✅ Filter by category, date range, amount range
- ✅ 10 predefined categories + custom categories

### 5.2 Income Management
- ✅ Add income with date, amount, source, description
- ✅ View all income records
- ✅ Update income records
- ✅ Delete income with confirmation
- ✅ Filter by source, date range
- ✅ 6 predefined income categories + custom

### 5.3 Budget Management
- ✅ Set monthly budget limits (YYYY-MM format)
- ✅ Real-time spending calculation
- ✅ Warning at 80% threshold
- ✅ Alert when budget exceeded
- ✅ View detailed budget status
- ✅ Delete budgets

### 5.4 Reports & Analytics
| Report | Description |
|--------|-------------|
| Financial Summary | Overall totals: income, expenses, balance |
| Category-wise Expense | Spending by category with percentages |
| Category-wise Income | Income by source with percentages |
| Monthly Report | Detailed month view with budget status |
| Spending Analytics | Highest category, average, largest transactions, distribution |
| Monthly Trends | 6-month trend analysis table |

### 5.5 Search & Filter
- Filter by transaction type (income/expense)
- Filter by category (case-insensitive)
- Filter by date range (start/end)
- Filter by amount range (min/max)
- Keyword search in descriptions
- View by specific month
- View all transactions

### 5.6 Data Export
- Export all transactions to CSV
- Export expenses only
- Export income only
- Export by month
- Auto-generated filenames with timestamps
- List previous exports

### 5.7 Data Persistence
- JSON-based local storage (`data/transactions.json`, `data/budgets.json`)
- Automatic directory/file creation
- Corrupted JSON handling with warnings
- Empty file handling
- Permission error handling

---

## 6. Technical Specifications

### 6.1 Technology Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Core language (f-strings, pathlib, type hints) |
| JSON | Standard | Data persistence |
| CSV | Standard | Data export |
| unittest | Standard | Unit testing |
| datetime | Standard | Date/time handling |
| pathlib | Standard | Cross-platform file paths |
| re | Standard | Regex validation |

### 6.2 Data Structures

#### Transaction Object
```json
{
  "id": "EXP001",
  "date": "2026-09-30",
  "amount": 450.0,
  "category": "Food",
  "description": "Dinner with friends",
  "type": "expense"
}
```

#### Budget Object
```json
{
  "month": "2026-09",
  "amount": 20000.0
}
```

#### CSV Export Format
```csv
ID,Date,Amount,Category,Description,Type
EXP001,2026-09-30,450.0,Food,Dinner with friends,expense
INC001,2026-09-30,25000.0,Salary,Monthly salary,income
```

### 6.3 ID Generation
- Expenses: `EXP001`, `EXP002`, ... (sequential, persisted)
- Income: `INC001`, `INC002`, ... (sequential, persisted)
- Counters initialized from existing data on startup

---

## 7. Validation Rules

| Field | Rules |
|-------|-------|
| Amount | Positive number (> 0), numeric only |
| Date | YYYY-MM-DD format, valid calendar date |
| Category | Predefined list or custom (with warning) |
| Month | YYYY-MM format |
| Transaction ID | Must exist in current dataset |
| Menu Choice | Must be from valid options |
| Confirmation | 'y'/'yes' for yes, 'n'/'no' for no |

---

## 8. Testing

### 8.1 Test Coverage
| Test Module | Test Cases | Coverage |
|-------------|------------|----------|
| `test_validators.py` | 25 | Amount, date, category, menu, ID, month, confirmation |
| `test_expense_manager.py` | 20 | CRUD, filtering, totals, ID generation, persistence |
| `test_budget_manager.py` | 13 | CRUD, status calculation, thresholds, alerts |
| `test_income_manager.py` | 6 | CRUD, calculations |
| `test_reports.py` | 14 | Summary, categories, monthly, analytics, formatting |

**Total: 78 test cases**

### 8.2 Running Tests
```bash
# All tests
python -m unittest discover

# Verbose
python -m unittest discover -v

# Specific module
python -m unittest tests.test_validators
python -m unittest tests.test_expense_manager
python -m unittest tests.test_budget_manager
python -m unittest tests.test_income_manager
python -m unittest tests.test_reports
```

---

## 9. Project Structure

```
ExpenseMate/
├── main.py                 # Application entry point (576 lines)
├── storage.py              # JSON persistence layer (139 lines)
├── transaction_manager.py  # Core transaction logic (220 lines)
├── expense_manager.py      # Expense operations (315 lines)
├── income_manager.py       # Income operations (236 lines)
├── budget_manager.py       # Budget tracking (105 lines)
├── report_manager.py       # Reports & analytics (273 lines)
├── validators.py           # Input validation (167 lines)
├── utils.py                # CLI utils & export (204 lines)
├── requirements.txt        # Python version requirement
├── LICENSE                 # MIT License
├── README.md               # Documentation
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
    ├── DESIGN_DOCUMENTATION.md
    ├── SCREENSHOT_CHECKLIST.md
    ├── DEMO_FLOW.md
    └── diagrams/
        ├── architecture.mmd
        ├── workflow.mmd
        ├── use_case.mmd
        ├── class_diagram.mmd
        ├── sequence_add_expense.mmd
        └── storage_schema.mmd
```

**Total: ~2,235 lines of Python code (excluding tests and docs)**

---

## 10. Error Handling Strategy

| Error Type | Handling Approach |
|------------|-------------------|
| Invalid amount | Clear message, re-prompt until valid |
| Invalid date format | Format guidance, re-prompt |
| Empty required fields | Validation message, re-prompt |
| Missing transaction ID | "Not found" message, return to menu |
| Corrupted JSON files | Warning + fresh start with empty array |
| Permission errors | User-friendly message, continue |
| Keyboard interrupt | Clean exit with goodbye message |
| Unexpected exceptions | Caught, logged, return to menu |

**The application never crashes due to normal user input errors.**

---

## 11. User Interface

### 11.1 Main Menu
```
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

Enter your choice: 
```

### 11.2 Sample Output – Financial Summary
```
==================================================
           FINANCIAL SUMMARY
==================================================

Total Income      : Rs.30,000.00
Total Expenses    : Rs.750.00
Current Balance   : Rs.29,250.00
Total Transactions: 4
  - Expenses      : 2
  - Income        : 2
==================================================
```

### 11.3 Sample Output – Category Report
```
==================================================
       CATEGORY-WISE EXPENSES
==================================================

Food                Rs.650.00 (68.4%)
Travel              Rs.300.00 (31.6%)

Total              Rs.950.00
==================================================
```

---

## 12. Future Enhancements

| Priority | Feature | Description |
|----------|---------|-------------|
| High | SQLite Backend | Replace JSON with SQLite for better performance |
| High | GUI | Tkinter/PyQt desktop interface |
| Medium | Web Version | Flask/FastAPI REST API + frontend |
| Medium | Recurring Transactions | Automatic monthly expense/income |
| Medium | Advanced Charts | Matplotlib visualizations |
| Low | Multi-user | Authentication & user isolation |
| Low | Cloud Sync | Backup/sync to cloud storage |
| Low | Multi-currency | Support for multiple currencies |
| Low | ML Categorization | Auto-categorize from descriptions |
| Low | OCR Receipt Scanning | Extract data from receipt images |

---

## 13. Academic Context

This project was developed as part of a **Python Essentials college course**. It demonstrates proficiency in:

- ✅ **Modular Python Architecture** – 8+ modules with clean imports
- ✅ **Object-Oriented Design** – Classes with encapsulation, dependency injection
- ✅ **File I/O** – JSON serialization, CSV export, pathlib usage
- ✅ **Exception Handling** – Try/except, custom error messages, graceful degradation
- ✅ **Input Validation** – Regex, type checking, boundary validation
- ✅ **Unit Testing** – unittest framework, test isolation with temp directories
- ✅ **CLI Application Design** – Menu systems, interactive prompts, table formatting
- ✅ **Documentation** – README, architecture docs, design docs, diagrams
- ✅ **Design Patterns** – Repository, Factory, Dependency Injection, SRP
- ✅ **Version Control** – Git with meaningful commit structure

---

## 14. Installation & Usage

### 14.1 Requirements
- Python 3.9 or higher

### 14.2 Installation
```bash
git clone <repository-url>
cd ExpenseMate

# Optional: Virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 14.3 Running
```bash
python main.py
```

### 14.4 Testing
```bash
python -m unittest discover -v
```

---

## 15. Conclusion

ExpenseMate successfully delivers a fully functional personal expense management system with:

- **Complete feature set** covering all stated objectives
- **Production-quality code** with comprehensive error handling
- **Thorough testing** ensuring reliability
- **Clean architecture** enabling future extensibility
- **Zero dependencies** ensuring easy deployment
- **Excellent documentation** for maintainability

The project demonstrates mastery of core Python concepts and software engineering principles appropriate for a college-level Python Essentials course.

---

## 16. Appendix

### 16.1 File Line Counts
| File | Lines |
|------|-------|
| main.py | 576 |
| transaction_manager.py | 220 |
| expense_manager.py | 315 |
| income_manager.py | 236 |
| budget_manager.py | 105 |
| report_manager.py | 273 |
| storage.py | 139 |
| validators.py | 167 |
| utils.py | 204 |
| **Total (Core)** | **2,235** |
| Tests | ~930 |
| Documentation | ~1,500 |

### 16.2 License
MIT License – See [LICENSE](../LICENSE) file for details.

### 16.3 Author
Developed as a Python Essentials course project.

---

*Report generated on September 30, 2026*
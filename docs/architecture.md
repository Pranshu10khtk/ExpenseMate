# System Architecture Documentation

## Overview

ExpenseMate follows a modular, layered architecture with clear separation of concerns. The system is organized into distinct modules, each responsible for a specific domain functionality.

## Architecture Diagram

```
                 ┌─────────────┐
                 │    USER     │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  CLI MENU   │
                 │ (main.py)   │
                 └──────┬──────┘
                        │
                        ▼
            ┌───────────┴───────────┐
            │  APPLICATION CONTROLLER│
            │    (ExpenseMateApp)    │
            └───────────┬───────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌───────────────┐ ┌─────────────┐ ┌──────────────┐
│ EXPENSE MGR   │ │ INCOME MGR  │ │ BUDGET MGR   │
│ (ExpenseMgr)  │ │ (IncomeMgr) │ │ (BudgetMgr)  │
└───────┬───────┘ └──────┬──────┘ └──────┬───────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  TRANSACTION MGR    │
              │ (TransactionManager)│
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    STORAGE LAYER    │
              │     (Storage)       │
              └──────────┬──────────┘
                         │
           ┌─────────────┴─────────────┐
           ▼                           ▼
    ┌─────────────┐             ┌─────────────┐
    │transactions.│             │ budgets.json│
    │    json     │             │             │
    └─────────────┘             └─────────────┘
```

## Module Responsibilities

### 1. Presentation Layer
- **main.py**: Entry point, main menu loop, navigation controller
- **utils.CLIUtils**: Screen clearing, menu printing, input handling, table formatting

### 2. Business Logic Layer
- **ExpenseManager**: Expense-specific operations, interactive prompts
- **IncomeManager**: Income-specific operations, interactive prompts
- **BudgetManager**: Budget CRUD, threshold calculations, alerts
- **ReportManager**: Report generation, analytics, formatting
- **TransactionManager**: Core transaction logic, filtering, ID generation, calculations

### 3. Data Access Layer
- **Storage**: JSON file read/write, error handling, file creation

### 4. Validation Layer
- **Validator**: Amount, date, category, menu choice, ID validation

### 5. Utility Layer
- **ExportManager**: CSV export functionality
- **utils**: Currency formatting, date parsing, sorting helpers

## Data Flow

### Adding an Expense
```
User Input → CLI → ExpenseManager → Validator → TransactionManager → Storage → JSON File
                                                    ↓
                                              Updates ID counter
                                                    ↓
                                              Returns success → CLI → User
```

### Generating a Report
```
User Request → CLI → ReportManager → TransactionManager → Storage → JSON File
                                                    ↓
                                              Returns data → ReportManager → Formatted Output → CLI → User
```

## Design Patterns Used

1. **Single Responsibility Principle**: Each class has one clear purpose
2. **Dependency Injection**: Managers receive dependencies via constructor
3. **Separation of Concerns**: Validation, storage, business logic separated
4. **Factory Pattern**: TransactionManager generates IDs
5. **Repository Pattern**: Storage abstracts file operations

## Scalability Considerations

The architecture allows easy replacement of:
- **Storage Layer**: Swap JSON for SQLite/PostgreSQL by implementing Storage interface
- **Presentation Layer**: Add GUI/Web by creating new controllers using same managers
- **Validation Layer**: Extend validation rules without modifying business logic

## Technology Stack

- **Language**: Python 3.9+
- **Storage**: JSON (local files)
- **Export**: CSV (standard library)
- **Testing**: unittest (standard library)
- **Date/Time**: datetime (standard library)
- **File Paths**: pathlib (standard library)
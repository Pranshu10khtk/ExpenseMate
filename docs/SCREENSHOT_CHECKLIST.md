# Screenshot Checklist for Project Report

Capture these screenshots during demo for the final project report.

---

## Required Screenshots

### 1. Main Menu
- **Description**: Full main menu showing all 14 options + Exit
- **Command**: `python main.py` → Don't enter anything
- **Filename**: `01_main_menu.png`

### 2. Add Expense
- **Description**: Add Expense screen with category selection visible
- **Steps**: Select 1 → Enter amount → Show category list
- **Filename**: `02_add_expense.png`

### 3. View Expenses
- **Description**: Formatted table showing expenses with totals
- **Steps**: Select 2 (with some expenses added)
- **Filename**: `03_view_expenses.png`

### 4. Add Income
- **Description**: Add Income screen with income categories
- **Steps**: Select 5 → Enter amount → Show category list
- **Filename**: `04_add_income.png`

### 5. View Income
- **Description**: Formatted table showing income records with total
- **Steps**: Select 6
- **Filename**: `05_view_income.png`

### 6. Budget Management
- **Description**: Budget submenu with Set/View/Delete options
- **Steps**: Select 9
- **Filename**: `06_budget_menu.png`

### 7. Budget Status
- **Description**: Budget status showing amount, expenses, remaining, percentage, status
- **Steps**: Select 9 → 2 (after setting budget and adding expenses)
- **Filename**: `07_budget_status.png`

### 8. Financial Summary
- **Description**: Financial summary with Income, Expenses, Balance, Transaction counts
- **Steps**: Select 10
- **Filename**: `08_financial_summary.png`

### 9. Category Report
- **Description**: Category-wise expense report with percentages
- **Steps**: Select 11 → 1
- **Filename**: `09_category_report.png`

### 10. Spending Analytics
- **Description**: Analytics screen with highest category, average, largest, distribution
- **Steps**: Select 11 → 4
- **Filename**: `10_spending_analytics.png`

### 11. Monthly Report
- **Description**: Monthly report with budget status and expense breakdown
- **Steps**: Select 11 → 3 → Enter month
- **Filename**: `11_monthly_report.png`

### 12. Search/Filter Menu
- **Description**: Search/Filter submenu with all filter options
- **Steps**: Select 12
- **Filename**: `12_search_filter_menu.png`

### 13. Filter Results
- **Description**: Filtered results (e.g., by category or amount range)
- **Steps**: Select 12 → 1 → Enter filter criteria
- **Filename**: `13_filter_results.png`

### 14. Export Menu
- **Description**: Export submenu with all export options
- **Steps**: Select 13
- **Filename**: `14_export_menu.png`

### 15. Export Success
- **Description**: Success message with file path after export
- **Steps**: Select 13 → 1
- **Filename**: `15_export_success.png`

### 16. CSV File Content
- **Description**: Open exported CSV file showing header and data rows
- **Steps**: Open `exports/transactions_YYYY-MM-DD.csv` in Notepad/Excel
- **Filename**: `16_csv_content.png`

### 17. Validation Error - Invalid Amount
- **Description**: Error message when entering negative/zero amount
- **Steps**: Select 1 → Enter `-100` as amount
- **Filename**: `17_validation_amount.png`

### 18. Validation Error - Invalid Date
- **Description**: Error message when entering invalid date format
- **Steps**: Select 1 → Enter `30-09-2026` as date
- **Filename**: `18_validation_date.png`

### 19. Confirmation Prompt
- **Description**: Delete confirmation prompt (y/n)
- **Steps**: Select 4 → Enter valid ID
- **Filename**: `19_delete_confirmation.png`

### 20. Test Execution
- **Description**: Terminal showing `python -m unittest discover` with all tests passing
- **Command**: `python -m unittest discover`
- **Filename**: `20_test_execution.png`

### 21. Project Folder Structure
- **Description**: File explorer showing ExpenseMate folder structure
- **Steps**: Open folder in VS Code/File Explorer
- **Filename**: `21_folder_structure.png`

### 22. JSON Data Files
- **Description**: Content of `data/transactions.json` and `data/budgets.json`
- **Steps**: Open both files in text editor
- **Filename**: `22_json_files.png`

### 23. Help Screen
- **Description**: Help screen showing all features
- **Steps**: Select 14
- **Filename**: `23_help_screen.png`

### 24. Monthly Trends Report
- **Description**: 6-month trend table
- **Steps**: Select 11 → 5
- **Filename**: `24_monthly_trends.png`

---

## Tips for Good Screenshots
- Use consistent terminal size (e.g., 120x40)
- Use dark theme or default terminal colors
- Capture full terminal window including title bar
- Use PNG format for crisp text
- Name files sequentially as listed above

---

## Total: 24 screenshots
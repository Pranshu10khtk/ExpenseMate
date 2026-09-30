# Demo Flow - ExpenseMate

## 5-10 Minute Demonstration Sequence

### Setup (Before Demo)
1. Ensure `python main.py` runs without errors
2. Have sample data in `data/transactions.json` (or start fresh)
3. Clear `exports/` directory for clean export demo

---

### Demo Steps

#### 1. Launch Application (30 seconds)
```bash
python main.py
```
- Show welcome banner and main menu
- Explain this is a CLI-based personal finance manager

#### 2. Add Income (1 minute)
- Select **5. Add Income**
- Enter date (or press Enter for today)
- Enter amount: `25000`
- Select category: **1. Salary**
- Description: `Monthly salary`
- Show success message with ID (e.g., INC004)

#### 3. Add 3 Expenses (2 minutes)
- Select **1. Add Expense**
- **Expense 1**: Date: today, Amount: `450`, Category: **1. Food**, Desc: `Lunch`
- **Expense 2**: Date: today, Amount: `1200`, Category: **3. Shopping**, Desc: `New shoes`
- **Expense 3**: Date: today, Amount: `300`, Category: **2. Travel**, Desc: `Bus fare`
- Show each success with IDs (EXP011, EXP012, EXP013)

#### 4. View Transactions (1 minute)
- Select **2. View Expenses** - Show table with 3 new expenses
- Select **6. View Income** - Show income records
- Point out formatted table with totals

#### 5. Set Budget (1 minute)
- Select **9. Manage Budget**
- Select **1. Set/Update Budget**
- Enter month (or press Enter for current): `2026-09`
- Enter budget amount: `20000`
- Select **2. View Budget Status** - Show budget, expenses, remaining, percentage
- Explain 80% warning threshold

#### 6. Display Financial Summary (30 seconds)
- Select **10. Financial Summary**
- Show: Total Income, Total Expenses, Balance, Transaction counts

#### 7. Display Category Report (1 minute)
- Select **11. Reports & Analytics**
- Select **1. Category-wise Expense Report**
- Show categories with amounts and percentages
- Select **4. Spending Analytics**
- Show: Highest category, Average expense, Largest transactions, Distribution bars

#### 8. Search/Filter Transaction (1 minute)
- Select **12. Search / Filter Transactions**
- Select **1. Filter Expenses**
- Filter by category: **Food** → Show only food expenses
- Filter by amount range: Min `500`, Max `1500` → Show matching
- Select **3. Search by Keyword** → Enter `shoe` → Show matching

#### 9. Export CSV (30 seconds)
- Select **13. Export Data**
- Select **1. Export All Transactions**
- Show success message with file path
- Open `exports/transactions_YYYY-MM-DD.csv` to verify content

#### 10. Run Tests (30 seconds)
```bash
python -m unittest discover
```
- Show all 83 tests pass

---

### Key Points to Highlight
- **Modular architecture** - 8+ Python modules
- **Input validation** - Try entering invalid amount/date to show error handling
- **Persistence** - Restart app, show data remains
- **JSON storage** - Open `data/transactions.json` to show structure
- **CSV export** - Open exported file in Excel/Notepad
- **Tests** - All 83 tests pass, no external dependencies

---

### Optional: Error Handling Demo
- Try adding expense with amount `-100` → Shows "Amount must be greater than zero"
- Try date `30-09-2026` → Shows "Date must be in YYYY-MM-DD format"
- Try invalid menu option `99` → Shows "Invalid option"

---

### Total Time: ~7-8 minutes
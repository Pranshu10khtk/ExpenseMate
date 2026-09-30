# Workflow Documentation

## Application Startup Flow

```mermaid
flowchart TD
    A[Start Application] --> B[Initialize Storage]
    B --> C[Load Transaction Manager]
    C --> D[Load Expense Manager]
    D --> E[Load Income Manager]
    E --> F[Load Budget Manager]
    F --> G[Load Report Manager]
    G --> H[Load Export Manager]
    H --> I[Display Welcome Banner]
    I --> J[Show Main Menu]
    J --> K{User Input}
```

## Main Menu Navigation

```mermaid
flowchart TD
    A[Main Menu] --> B{User Choice}
    B -->|1| C[Add Expense]
    B -->|2| D[View Expenses]
    B -->|3| E[Update Expense]
    B -->|4| F[Delete Expense]
    B -->|5| G[Add Income]
    B -->|6| H[View Income]
    B -->|7| I[Update Income]
    B -->|8| J[Delete Income]
    B -->|9| K[Manage Budget]
    B -->|10| L[Financial Summary]
    B -->|11| M[Reports & Analytics]
    B -->|12| N[Search/Filter]
    B -->|13| O[Export Data]
    B -->|14| P[Help]
    B -->|0| Q[Exit Application]
    
    C --> R[Return to Main Menu]
    D --> R
    E --> R
    F --> R
    G --> R
    H --> R
    I --> R
    J --> R
    K --> R
    L --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> S[Save & Exit]
```

## Add Expense Workflow

```mermaid
flowchart TD
    A[Select Add Expense] --> B[Prompt for Date]
    B --> C{Valid Date?}
    C -->|No| B
    C -->|Yes| D[Prompt for Amount]
    D --> E{Valid Amount?}
    E -->|No| D
    E -->|Yes| F[Show Categories]
    F --> G[Prompt for Category]
    G --> H{Valid Category?}
    H -->|No| G
    H -->|Yes| I[Prompt for Description]
    I --> J[Generate Transaction ID]
    J --> K[Create Transaction Object]
    K --> L[Save to Storage]
    L --> M{Save Success?}
    M -->|No| N[Show Error]
    M -->|Yes| O[Show Success Message]
    N --> P[Return to Menu]
    O --> P
```

## Add Income Workflow

```mermaid
flowchart TD
    A[Select Add Income] --> B[Prompt for Date]
    B --> C{Valid Date?}
    C -->|No| B
    C -->|Yes| D[Prompt for Amount]
    D --> E{Valid Amount?}
    E -->|No| D
    E -->|Yes| F[Show Income Categories]
    F --> G[Prompt for Category]
    G --> H{Valid Category?}
    H -->|No| G
    H -->|Yes| I[Prompt for Description]
    I --> J[Generate Transaction ID]
    J --> K[Create Transaction Object]
    K --> L[Save to Storage]
    L --> M{Save Success?}
    M -->|No| N[Show Error]
    M -->|Yes| O[Show Success Message]
    N --> P[Return to Menu]
    O --> P
```

## Budget Management Workflow

```mermaid
flowchart TD
    A[Select Manage Budget] --> B[Show Current Budget Status]
    B --> C{User Choice}
    C -->|1| D[Set/Update Budget]
    C -->|2| E[View Budget Details]
    C -->|3| F[Delete Budget]
    C -->|0| G[Return to Main Menu]
    
    D --> H[Prompt for Month]
    H --> I[Prompt for Amount]
    I --> J{Valid Amount?}
    J -->|No| I
    J -->|Yes| K[Save Budget]
    K --> L[Show Confirmation]
    L --> B
    
    E --> M[Calculate Budget Status]
    M --> N[Display Details]
    N --> B
    
    F --> O[Confirm Deletion]
    O --> P{Confirmed?}
    P -->|Yes| Q[Delete Budget]
    P -->|No| B
    Q --> B
```

## Reports & Analytics Workflow

```mermaid
flowchart TD
    A[Select Reports] --> B{Report Type}
    B -->|1| C[Category-wise Expense Report]
    B -->|2| D[Category-wise Income Report]
    B -->|3| E[Monthly Report]
    B -->|4| F[Spending Analytics]
    B -->|5| G[Monthly Trends]
    B -->|0| H[Return to Main Menu]
    
    C --> I[Calculate Category Totals]
    I --> J[Calculate Percentages]
    J --> K[Display Formatted Table]
    K --> H
    
    D --> L[Calculate Income Categories]
    L --> M[Display Formatted Table]
    M --> H
    
    E --> N[Prompt for Month]
    N --> O[Get Monthly Summary]
    O --> P[Get Budget Status]
    P --> Q[Display Complete Report]
    Q --> H
    
    F --> R[Get Highest Category]
    R --> S[Get Average Expense]
    S --> T[Get Largest Transactions]
    T --> U[Get Distribution]
    U --> V[Display Analytics]
    V --> H
    
    G --> W[Calculate 6-Month Trends]
    W --> X[Display Trend Table]
    X --> H
```

## Search & Filter Workflow

```mermaid
flowchart TD
    A[Select Search/Filter] --> B{Filter Type}
    B -->|1| C[Filter Expenses]
    B -->|2| D[Filter Income]
    B -->|3| E[Search by Keyword]
    B -->|4| F[View by Month]
    B -->|5| G[View All Transactions]
    B -->|0| H[Return to Main Menu]
    
    C --> I[Show Filter Options]
    I --> J[Prompt for Category]
    J --> K[Prompt for Date Range]
    K --> L[Prompt for Amount Range]
    L --> M[Apply Filters]
    M --> N[Display Results]
    N --> H
    
    D --> O[Show Filter Options]
    O --> P[Apply Filters]
    P --> Q[Display Results]
    Q --> H
    
    E --> R[Prompt for Keyword]
    R --> S[Search Descriptions]
    S --> T[Display Results]
    T --> H
    
    F --> U[Prompt for Month]
    U --> V[Get Month Transactions]
    V --> W[Display with Summary]
    W --> H
    
    G --> X[Get All Transactions]
    X --> Y[Display All]
    Y --> H
```

## Export Data Workflow

```mermaid
flowchart TD
    A[Select Export] --> B{Export Type}
    B -->|1| C[Export All Transactions]
    B -->|2| D[Export Expenses Only]
    B -->|3| E[Export Income Only]
    B -->|4| F[Export by Month]
    B -->|5| G[List Previous Exports]
    B -->|0| H[Return to Main Menu]
    
    C --> I[Generate Filename]
    I --> J[Write CSV]
    J --> K{Write Success?}
    K -->|No| L[Show Error]
    K -->|Yes| M[Show Success + Path]
    L --> H
    M --> H
    
    D --> N[Filter Expenses]
    N --> I
    
    E --> O[Filter Income]
    O --> I
    
    F --> P[Prompt for Month]
    P --> Q[Filter by Month]
    Q --> I
    
    G --> R[List Export Directory]
    R --> S[Display Files]
    S --> H
```

## Data Persistence Workflow

```mermaid
flowchart TD
    A[Application Start] --> B[Storage Init]
    B --> C{Data Dir Exists?}
    C -->|No| D[Create Data Directory]
    C -->|Yes| E[Check Files]
    D --> E
    E --> F{transactions.json Exists?}
    F -->|No| G[Create Empty Array]
    F -->|Yes| H[Read & Validate JSON]
    G --> I{Valid JSON?}
    H --> I
    I -->|No| J[Log Warning + Use Empty]
    I -->|Yes| K[Load Transactions]
    J --> K
    K --> L{budgets.json Exists?}
    L -->|No| M[Create Empty Array]
    L -->|Yes| N[Read & Validate JSON]
    M --> O{Valid JSON?}
    N --> O
    O -->|No| P[Log Warning + Use Empty]
    O -->|Yes| Q[Load Budgets]
    P --> Q
    Q --> R[Initialize ID Counters]
    R --> S[Ready for Operations]
    
    S --> T[User Operations]
    T --> U[Modify Data]
    U --> V[Write to JSON]
    V --> W{Write Success?}
    W -->|No| X[Show Error - Data in Memory]
    W -->|Yes| Y[Confirm Persistence]
    X --> T
    Y --> T
```

## Error Handling Flow

```mermaid
flowchart TD
    A[User Input] --> B{Input Valid?}
    B -->|No| C[Show Specific Error]
    C --> D[Re-prompt User]
    D --> A
    B -->|Yes| E[Process Operation]
    E --> F{Operation Success?}
    F -->|No| G[Show Operation Error]
    G --> H{Recoverable?}
    H -->|Yes| D
    H -->|No| I[Log Error + Continue]
    F -->|Yes| J[Show Success]
    I --> J
    J --> K[Return to Menu]
```

## Key Workflow Principles

1. **Validation First**: All inputs validated before processing
2. **Graceful Degradation**: Errors don't crash the app; user returns to menu
3. **Confirmation for Destructive Actions**: Delete operations require explicit confirmation
4. **Immediate Feedback**: Success/error messages shown after every operation
5. **Persistent State**: Data saved after every successful operation
6. **Clean Navigation**: Consistent return to previous menu after operations
7. **Empty State Handling**: Clear messages when no data exists
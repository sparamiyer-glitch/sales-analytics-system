# Sales Analytics System

**Student Name:** Parameswaran Sivaramakrishnan
**Student ID:** bitsom_ba_25071771
**Email:** s.param.iyer@gmail.com
**Date:** 18th January 2026
**Course:** Business Analytics with Generative & Agentic AI
**Module:** Module 3: Python Programming

---

## Project Overview

A comprehensive Python application that processes sales transaction data, performs sophisticated analysis across multiple dimensions, and generates detailed reports. The system handles data quality issues through validation and cleaning, integrates with external APIs for product enrichment, and provides interactive filtering capabilities for targeted analysis. Built as part of the Masai School Module 3 assignment to demonstrate proficiency in file handling, data structures, API integration, and application architecture.

---

## Repository Structure

```
sales-analytics-system/
├── README.md                          # Project documentation and setup guide
├── main.py                            # Main application entry point
├── requirements.txt                   # Python package dependencies
│
├── utils/                             # Utility modules for specific functions
│   ├── __init__.py                    # Makes utils a Python package
│   ├── file_handler.py                # File reading, parsing, validation
│   ├── data_processor.py              # Data analysis and processing
│   ├── api_handler.py                 # API integration and enrichment
│   └── report_handler.py              # Report generation
│
├── data/                              # Input data folder
│   ├── sales_data.txt                 # Raw sales transactions (pipe-delimited)
│   └── enriched_sales_data.txt        # Generated enriched transaction data
│
└── output/                            # Generated output files (auto-created)
    └── sales_report.txt               # Comprehensive sales report
```

---

## Technologies Used

- **Python 3.14+** - Core programming language
- **Requests Library** - HTTP library for API calls
- **Standard Library Modules:**
  - `csv` - CSV file handling
  - `json` - JSON data processing
  - `datetime` - Date and time operations
  - `collections` - Advanced data structures (defaultdict)
  - `os` - File system operations
  - `sys` - System-level operations

- **External API:** DummyJSON API (https://dummyjson.com/products)
- **Development Environment:** Visual Studio Code with Python virtual environment
- **Version Control:** Git

---

## Setup Instructions

### Prerequisites

- **Operating System:** Windows 11
- **Python:** Version 3.14 or higher
- **RAM:** Minimum 4 GB
- **Storage:** 500 MB free space
- **Internet:** Required for API calls

### Step 1: Create Project Directory

```powershell
cd D:\Python_Class_BitSOM
mkdir sales-analytics-system
cd sales-analytics-system
```

### Step 2: Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# You should see (venv) at the beginning of your terminal line
```

### Step 3: Install Dependencies

```powershell
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 4: Create Project Structure

```powershell
# Create necessary folders
mkdir utils
mkdir data
mkdir output

# Create __init__.py for utils package
echo $null > utils/__init__.py
```

### Step 5: Download Sales Data

1. Download `sales_data.txt` from the [Google Drive link](https://drive.google.com/file/d/1BoXu46cKxHeB0qHJ0yN4bwL3ZkbQ2Y0Y/view?usp=sharing)
2. Place the file in: `D:\Python_Class_BitSOM\sales-analytics-system\data\sales_data.txt`
3. Verify file location: Check that the file exists at the correct path

### Step 6: Verify Installation

```powershell
# Test if application can be imported
python -c "from utils.file_handler import read_sales_data; print('Import successful')"
```

---

## Running the Application

### From Visual Studio Code

1. **Open Project Folder:**
   - Launch VS Code
   - File → Open Folder
   - Navigate to: `D:\Python_Class_BitSOM\sales-analytics-system`

2. **Open Terminal:**
   - Press: `Ctrl + `` (backtick)
   - Or: View → Terminal

3. **Activate Virtual Environment:**
   ```powershell
   venv\Scripts\activate
   ```

4. **Run Application:**
   ```powershell
   python main.py
   ```

5. **Follow Interactive Prompts:**
   - Choose to filter data (y/n)
   - Select region if filtering
   - Enter amount range if filtering
   - Wait for process to complete

### From Command Prompt

```powershell
cd D:\Python_Class_BitSOM\sales-analytics-system
venv\Scripts\activate
python main.py
```

### Expected Output

The application will display progress through 13 steps:
- Reading and parsing data
- Validation summary
- Analysis completion
- API data fetching
- Data enrichment status
- Report generation confirmation

---

## Project Components

### Part 1: File Handling & Preprocessing (utils/file_handler.py)

**Functions:**
- `read_sales_data(filename)` - Reads file with automatic encoding detection
- `parse_transactions(raw_lines)` - Converts raw data to structured format
- `validate_and_filter(transactions, region, min_amount, max_amount)` - Validates and filters records

**Key Features:**
- Handles UTF-8, Latin-1, and CP1252 encodings
- Removes data quality issues (commas, formatting)
- Implements flexible filtering
- Displays available options to user

### Part 2: Data Processing & Analysis (utils/data_processor.py)

**Functions:**
- `calculate_total_revenue()` - Total revenue calculation
- `region_wise_sales()` - Regional performance analysis
- `top_selling_products()` - Product performance ranking
- `customer_analysis()` - Customer spending patterns
- `daily_sales_trend()` - Time-series sales analysis
- `find_peak_sales_day()` - Best performing day identification
- `low_performing_products()` - Underperforming product detection

**Key Features:**
- Multi-dimensional analysis
- Percentage calculations
- Unique entity counting
- Sorted results for easy interpretation

### Part 3: API Integration (utils/api_handler.py)

**Functions:**
- `fetch_all_products()` - Retrieves products from DummyJSON API
- `create_product_mapping()` - Organizes API data structure
- `enrich_sales_data()` - Adds API information to transactions
- `save_enriched_data()` - Writes enriched data to file

**Key Features:**
- Error handling for API calls (timeouts, connection errors)
- Product ID extraction and matching
- Graceful handling of unmatched products
- CSV writing with proper formatting

**Important Note on API Enrichment:**

The DummyJSON API contains products with numeric IDs **1-100**, while the sales dataset uses internal ProductIDs in format **P101, P102, P103**, etc. (extracting to numeric IDs **101+**). This creates an intentional mismatch that demonstrates real-world API integration challenges. The system gracefully handles this scenario:

- API data is successfully fetched (100 products retrieved)
- Enrichment logic attempts to match each ProductID
- When ProductID 101 doesn't exist in API data (which ends at 100), API_Match is set to False
- Original transaction data is preserved regardless of match status
- System continues without crashing, demonstrating robust error handling

### Part 4: Report Generation (utils/report_handler.py)

**Functions:**
- `generate_sales_report()` - Creates 8-section comprehensive report

**Report Sections:**
1. Header with metadata and generation timestamp
2. Overall summary statistics (revenue, transactions, average order value, date range)
3. Region-wise performance (sales, percentages, transaction counts)
4. Top 5 products by quantity sold
5. Top 5 customers by total spending
6. Daily sales trends (date, revenue, transactions, unique customers)
7. Product performance analysis (best day, low performers, regional averages)
8. API enrichment summary (success rate, unmatched products list)

### Part 5: Main Application (main.py)

**Main Function:**
- `main()` - Orchestrates complete 13-step workflow

**Workflow:**
1. Display welcome message
2. Read sales data with encoding handling
3. Parse transactions
4. Show filter options to user
5. Apply optional filters
6. Validate data
7. Perform analysis
8. Fetch API data
9. Enrich transactions
10. Save enriched data
11. Generate report
12. Display summary statistics
13. Completion message

---

## Data Specifications

### Input Data (sales_data.txt)

**Format:** Pipe-delimited (`|`)  
**Encoding:** Non-UTF-8 (handled by application)  
**Total Records:** ~80 transactions  
**Expected Valid After Cleaning:** ~70 records  
**Invalid Records:** ~10 records

**Fields:**
- TransactionID (format: T### - must start with 'T')
- Date (format: YYYY-MM-DD)
- ProductID (format: P### - must start with 'P')
- ProductName (text field)
- Quantity (numeric, must be > 0)
- UnitPrice (numeric, must be > 0)
- CustomerID (format: C### - must start with 'C')
- Region (text: North, South, East, West)

### Output Data

**enriched_sales_data.txt:**
- All original fields plus API-enriched columns
- Location: `data/enriched_sales_data.txt`
- Fields: TransactionID, Date, ProductID, ProductName, Quantity, UnitPrice, CustomerID, Region, API_Category, API_Brand, API_Rating, API_Match

**sales_report.txt:**
- 8-section comprehensive report
- Location: `output/sales_report.txt`
- Currency formatted as Rs. with comma separators
- Professional table-based layout

---

## Data Validation Rules

### Records Removed (Invalid):

- Quantity ≤ 0
- UnitPrice ≤ 0
- TransactionID doesn't start with 'T'
- ProductID doesn't start with 'P'
- CustomerID doesn't start with 'C'
- Missing CustomerID or Region

### Records Cleaned But Kept (Valid):

- Commas in ProductName → removed
- Commas in numeric fields → removed, converted to int/float
- Empty lines → skipped
- Extra whitespace → trimmed

---

## Understanding ProductID Mismatch & Enrichment Rate

### The Issue Explained

When you run the application and see enrichment results showing **0.0% match rate** (e.g., "Enriched 0/18 transactions (0.0%)"), this is **expected and not an error**. Here's why:

**Your Sales Data ProductIDs:**
- Format: P101, P102, P103, P104, etc.
- Range: P101 onwards (numeric ID 101+)
- Source: Internal e-commerce system

**DummyJSON API ProductIDs:**
- Format: Numeric IDs only (1, 2, 3, ... 100)
- Range: 1 to 100
- Source: Third-party public API

**The Mismatch:**
When the enrichment function extracts the numeric part from "P101", it gets 101. However, the API only contains products with IDs 1-100. Therefore, product 101 does not exist in the API data, and the enrichment attempt fails gracefully.

### Why This Happens

1. Your sales data has internal ProductIDs starting at P101
2. The DummyJSON API has products numbered 1-100
3. There is a mismatch in ID ranges between the two systems
4. This is realistic in real-world scenarios where internal IDs don't align with external systems
5. The system is designed to handle such mismatches without crashing

### Impact on Output Files

**enriched_sales_data.txt:**
- Contains all original transaction fields
- API enrichment columns (API_Category, API_Brand, API_Rating) are empty
- API_Match field shows `False` for all rows
- File is still successfully created with complete original data

Example:
```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
T001|2024-12-02|P101|Laptop|10|29820.0|C001|North|||False
T002|2024-12-03|P102|Monitor|5|8850.0|C002|North|||False
```

**sales_report.txt:**
- All sections are complete and functional
- Analysis is based on transaction data (not API data)
- API Enrichment Summary section shows:
  - Total Products Enriched: 0 / 18
  - Success Rate: 0.00%
  - Products Not Matched: Lists all ProductIDs

### This Is Not a Problem

The system is functioning correctly. The 0% enrichment rate indicates:
- ✓ File reading works
- ✓ Data parsing works
- ✓ API integration works (successfully fetched 100 products)
- ✓ Enrichment logic works (gracefully handles mismatches)
- ✓ Error handling works (no crash, continues processing)

### Real-World Applicability

In actual business scenarios:
- Internal ProductIDs rarely align with external API IDs
- Systems gracefully handle mismatches
- Data enrichment may have partial success rates (some products match, others don't)
- The ability to continue despite mismatches is a feature, not a bug

### What This Demonstrates

This behavior showcases:
1. Robust error handling and exception management
2. Graceful degradation (system doesn't crash on mismatches)
3. Data preservation (original data is kept even if enrichment fails)
4. Realistic business logic (handling real-world ID mismatches)
5. API integration best practices (trying to match, handling failures)

---

## Key Learnings

Through this project, I learned:

1. **File Handling with Encoding:** Practical experience with handling non-standard file encodings and implementing fallback mechanisms for robust file reading across different systems.

2. **Data Validation Patterns:** Importance of comprehensive data validation rules and the distinction between data that should be rejected versus data that can be cleaned and recovered.

3. **API Integration:** Real-world API consumption with error handling for network issues, timeouts, and malformed responses. Understanding how to gracefully handle API failures without crashing the application.

4. **Multi-dimensional Data Analysis:** Building analysis functions that provide different perspectives on data (temporal, categorical, hierarchical) and how to aggregate data across multiple dimensions efficiently.

5. **Application Architecture:** Structuring applications into modular, reusable components with clear separation of concerns. Each module has a single responsibility, making the code maintainable and testable.

6. **Interactive User Experience:** Implementing user prompts and dynamic filtering options to make the application interactive rather than purely automated.

7. **Realistic Data Challenges:** Handling real-world scenarios like ID mismatches between systems, demonstrating that not all enrichment attempts will succeed but the system should continue processing.

---

## Challenges Faced

### Challenge 1: Encoding Handling in File Reading

**Problem:** The sales_data.txt file uses non-UTF-8 encoding, which would cause a UnicodeDecodeError if read directly. The exact encoding was unknown beforehand.

**Solution:** Implemented a try-except loop that attempts multiple common encodings (UTF-8, Latin-1, CP1252) in order. Once an encoding successfully reads the file, it returns the data. This approach is robust and doesn't require knowing the encoding in advance.

```python
for encoding in ['utf-8', 'latin-1', 'cp1252']:
    try:
        with open(filename, 'r', encoding=encoding) as file:
            lines = file.readlines()
        return raw_lines  # Success
    except UnicodeDecodeError:
        continue  # Try next encoding
```

### Challenge 2: Data Quality Issues Mixed Within Fields

**Problem:** The dataset contained commas in multiple places: within ProductName fields (e.g., "Mouse,Wireless") and within numeric fields (e.g., "1,500" for price). Simple splitting on delimiters would break these records.

**Solution:** Used field-by-field cleaning after parsing. For ProductName, removed all commas. For numeric fields, removed commas before converting to int/float. This allows the system to recover data that would otherwise be rejected.

### Challenge 3: Product ID Matching Across Systems

**Problem:** Enriching sales data required matching ProductID from transactions with product IDs from the API. The transaction ProductIDs are in format P101 (with prefix), while API products have numeric IDs 1-100. Direct matching would fail completely.

**Solution:** Implemented numeric ID extraction logic that removes the non-numeric prefix and attempts to match. For mismatches, the system gracefully sets API_Match to False and continues processing rather than crashing.

### Challenge 4: API Failure Resilience

**Problem:** Network requests can fail due to connection issues, timeouts, or server errors. The application needed to handle these gracefully without crashing and losing the user's progress.

**Solution:** Wrapped API calls in comprehensive try-except blocks that catch specific errors (ConnectionError, Timeout) and generic exceptions. The application displays user-friendly error messages but continues processing with whatever data was available.

### Challenge 5: Handling Empty or Sparse Data

**Problem:** When no transactions exist for certain regions or time periods, calculations like daily averages could produce errors or divide by zero.

**Solution:** Added conditional checks before performing division operations. For example, `avg_order = total / count if count > 0 else 0` prevents division errors and provides sensible defaults for empty datasets.

### Challenge 6: User Input Validation

**Problem:** User-provided filter values (region names, amount ranges) needed to be validated without crashing if invalid input was provided.

**Solution:** Used try-except blocks around type conversions (e.g., converting string to float). Invalid inputs are caught, a message is displayed, and the filter is skipped, allowing the user to try again or proceed without that filter.

---

## Testing Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed via `pip install -r requirements.txt`
- [ ] sales_data.txt exists in `data/` folder
- [ ] Project structure matches the specified layout
- [ ] Python files have no syntax errors
- [ ] Application starts without import errors
- [ ] File reading works (no encoding errors)
- [ ] Data parsing produces transactions
- [ ] Validation correctly identifies invalid records
- [ ] Filtering works with user input
- [ ] Data analysis functions produce results
- [ ] API fetching completes successfully
- [ ] Enrichment file is generated
- [ ] Report file is generated with all 8 sections
- [ ] No hardcoded file paths (all relative paths)
- [ ] Application completes all 13 steps
- [ ] Output files contain expected data

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError: requests | Run `pip install requests` with virtual environment activated |
| FileNotFoundError: sales_data.txt | Download file from Google Drive and place in `data/` folder |
| SyntaxError in Python files | Check for copy-paste errors, ensure indentation is consistent |
| Application hangs at API step | Check internet connection, wait for timeout (usually 30 seconds) |
| Enrichment shows 0% match rate | This can happen if ProductIDs don't align with API data. Not an error. |
| Virtual environment not activating | Try deleting `venv` folder and recreating: `python -m venv venv` |
| Permission denied error | Run VS Code or terminal as Administrator |

---

## File Naming Conventions

- Python files: `snake_case` (e.g., `file_handler.py`, `data_processor.py`)
- Markdown files: `snake_case` (e.g., `README.md`)
- Data files: `snake_case_description.txt` (e.g., `sales_data.txt`, `enriched_sales_data.txt`)
- Input files: Include `raw` suffix (e.g., `sales_data.txt`)

---

## Documentation Standards

All code includes:
- Clear one-line and multi-line comments in English
- Meaningful function and variable names
- Type hints on function parameters and returns
- Error handling with try-except blocks
- Docstrings explaining function purpose, parameters, and return values
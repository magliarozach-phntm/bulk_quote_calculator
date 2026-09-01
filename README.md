Trim it. For a portfolio repo, requirements.txt should list the direct project dependencies, not every transitive package installed in your environment.

I’d use:

openpyxl==3.1.5
pytest==9.1.1
pyinstaller==6.22.2

That’s enough because:

openpyxl is used by the app
pytest is used for tests
pyinstaller is used to build the .exe
Tkinter is part of the Python standard library on Windows, so it does not belong in requirements.txt

Packages like et_xmlfile, pluggy, altgraph, pefile, etc. are dependencies of those libraries and pip will install them automatically.

So yes — replace your current file with just those three lines.

can you give me the full readme

Absolutely — here’s a cleaned-up full README you can drop directly into README.md.

# Bulk Quote Calculator

A desktop Python application for importing quote data from Excel, validating each row, applying configurable pricing rules, and exporting formatted quote results and validation errors.

This project demonstrates practical business-process automation using Python, Tkinter, `openpyxl`, JSON configuration, automated testing with `pytest`, and Windows packaging with PyInstaller.

## Screenshots

### Desktop Application

![Bulk Quote Calculator GUI](assets/gui.png)

### Generated Results

![Excel Results](assets/results.png)

### Validation Errors

![Excel Error Reporting](assets/errors.png)

## Features

- Import quote data from `.xlsx` files
- Simple Tkinter desktop interface
- Row-by-row input validation
- Collect all validation errors for a row in one pass
- Calculate:
  - Shipping cost per unit
  - Landed cost per unit
  - Final quoted price
- Configurable markup limits using `config.json`
- Export formatted Excel workbooks
- Separate `Results` and `Errors` worksheets
- Excel tables with filtering and sorting
- Currency and percentage formatting
- Standalone Windows executable support with PyInstaller
- Automated unit and integration testing with `pytest`

## Application Workflow

```text
Excel Input
    ↓
Row Validation
    ↓
Business Calculations
    ↓
Results / Errors Separation
    ↓
Formatted Excel Output

From the user's perspective:

Select Excel File → Calculate Quotes → Review Results
Input Format

The input workbook should contain the following columns:

Column	Description
SKU	Product identifier
Quantity	Number of units
Unit Cost	Cost per individual unit
Shipping Cost	Total shipping cost
Markup	Desired markup percentage

Example:

SKU	Quantity	Unit Cost	Shipping Cost	Markup
ABC123	500	4.25	350.00	20
DEF456	1200	2.80	500.00	25
GHI789	250	8.15	225.00	15
Calculations

The application applies the following pricing logic:

Shipping Per Unit = Shipping Cost / Quantity

Landed Cost = Unit Cost + Shipping Per Unit

Quote Price = Landed Cost × (1 + Markup / 100)

Example:

Quantity:        500
Unit Cost:       $4.25
Shipping Cost:   $350.00
Markup:          20%

Shipping / Unit: $0.70
Landed Cost:     $4.95
Quote Price:     $5.94

Monetary results are rounded to two decimal places.

Validation

Each row is validated before any calculations are performed.

The application checks for:

Missing SKU values
Non-numeric quantities
Zero or negative quantities
Fractional quantities
Negative unit costs
Negative shipping costs
Non-numeric pricing fields
Markup values outside the configured limits

Validation is designed to collect all errors for a row in one pass rather than stopping at the first failure.

Invalid rows are excluded from quote calculations and written to the Errors worksheet.

Excel Output

The generated workbook contains a formatted Results worksheet with:

SKU
Quantity
Unit Cost
Shipping Cost
Markup
Shipping Per Unit
Landed Cost
Quote Price

The Results worksheet includes:

Excel table formatting
Filtering and sorting
Currency formatting
Percentage formatting
Frozen header row
Readable column widths

If invalid rows are detected, an Errors worksheet is added containing:

SKU
All validation messages associated with that row

This allows valid rows to continue processing even when other rows contain bad input.

Configuration

Business rules are stored separately from the calculation logic in config.json.

Example:

{
  "minimum_markup": 0,
  "maximum_markup": 100,
  "currency": "USD",
  "output_filename": "quote_results.xlsx"
}

This allows configurable values to be changed without modifying the core calculation code.

Project Structure
bulk_quote_calculator/
│
├── calculator.py
├── config.json
├── config_loader.py
├── excel_io.py
├── gui.py
├── main.py
├── validator.py
│
├── tests/
│   ├── test_calculator.py
│   ├── test_validator.py
│   └── test_process_quotes.py
│
├── assets/
│   ├── gui.png
│   ├── results.png
│   └── errors.png
│
├── sample_input.xlsx
├── requirements.txt
├── LICENSE
└── README.md
Module Responsibilities
calculator.py

Contains the core pricing calculations.

The calculation layer is kept separate from Excel handling and the GUI so it can be independently tested and reused.

validator.py

Validates incoming quote data and returns all detected validation errors for each row.

excel_io.py

Handles:

Excel workbook input
Excel workbook output
Worksheet creation
Formatting
Excel table generation
Results and Errors sheets
config_loader.py

Loads external configuration values from config.json.

main.py

Coordinates the complete processing workflow:

Read Input
→ Validate Rows
→ Calculate Valid Quotes
→ Separate Errors
→ Write Output Workbook
gui.py

Provides the Tkinter desktop interface.

The GUI is intentionally kept separate from calculation and Excel logic.

tests/

Contains unit and integration tests for the application's core behavior.

Installation

Clone the repository:

git clone https://github.com/magliarozach-phntm/bulk_quote_calculator.git
cd bulk_quote_calculator

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt
Requirements

The project uses:

openpyxl==3.1.5
pytest==9.1.1
pyinstaller==6.22.2

Tkinter is included with standard Python installations on Windows and does not require a separate pip package.

Running the Application

Start the desktop application:

python gui.py

Then:

Click Browse
Select an Excel workbook
Click Calculate Quotes
Review the processing summary
Click Open Results
Review the generated Results and Errors worksheets
Testing

The project uses pytest for automated testing.

Run the full test suite:

python -m pytest -v

Current tests cover:

Quote calculations
Valid row handling
Invalid row handling
Configurable markup limits
Multi-error validation
Integer-like Excel quantities
End-to-end Excel input/output processing
Results workbook creation
Errors worksheet creation

The integration test creates temporary Excel files during testing and verifies the complete application pipeline.

Windows Executable

The application can be packaged as a standalone Windows executable using PyInstaller.

Build with:

python -m PyInstaller --onefile --windowed --name BulkQuoteCalculator gui.py

The executable is generated in:

dist/BulkQuoteCalculator.exe

For the packaged version, config.json should remain alongside the executable:

dist/
├── BulkQuoteCalculator.exe
└── config.json

Keeping configuration external allows business rules to be edited without rebuilding the executable.

Design Goals

This project was built around several software design principles:

Separation of concerns
Business logic independent from UI code
Configurable business rules
Defensive input validation
Batch processing that continues when individual rows fail
Clear audit-friendly Excel output
Automated testing
Maintainable modular structure
Simple workflow for non-technical users
Technologies
Python 3
Tkinter
openpyxl
pytest
JSON
PyInstaller
Microsoft Excel
Potential Extensions

The architecture could be extended to support:

Additional pricing rules
Configurable rate tables
Multiple quote types
Additional Excel templates
More complex landed-cost calculations
Audit logging
User-selectable output locations
Additional business validation rules
License

This project is licensed under the MIT License.


For the GitHub portfolio version, I’d make sure those three screenshots actually exist under `assets/` before you push this README, otherwise the image links will show as broken. 
can you put this all into one file for the readme?

Done — here’s the complete file:

Download README.md

Drop it into the root of your repo, add the three screenshots under assets/, then commit and push. 

README.md
Document

Library
/
README.md
Bulk Quote Calculator

A desktop Python application for importing quote data from Excel, validating each row, applying configurable pricing rules, and exporting formatted quote results and validation errors.

This project demonstrates practical business-process automation using Python, Tkinter, openpyxl, JSON configuration, automated testing with pytest, and Windows packaging with PyInstaller.

Screenshots
Desktop Application




Generated Results




Validation Errors




Features
Import quote data from .xlsx files
Simple Tkinter desktop interface
Row-by-row input validation
Collect all validation errors for a row in one pass
Calculate:
Shipping cost per unit
Landed cost per unit
Final quoted price
Configurable markup limits using config.json
Export formatted Excel workbooks
Separate Results and Errors worksheets
Excel tables with filtering and sorting
Currency and percentage formatting
Standalone Windows executable support with PyInstaller
Automated unit and integration testing with pytest
Application Workflow
Excel Input
    ↓
Row Validation
    ↓
Business Calculations
    ↓
Results / Errors Separation
    ↓
Formatted Excel Output

From the user's perspective:

Select Excel File → Calculate Quotes → Review Results
Input Format

The input workbook should contain the following columns:

Column	Description
SKU	Product identifier
Quantity	Number of units
Unit Cost	Cost per individual unit
Shipping Cost	Total shipping cost
Markup	Desired markup percentage

Example:

SKU	Quantity	Unit Cost	Shipping Cost	Markup
ABC123	500	4.25	350.00	20
DEF456	1200	2.80	500.00	25
GHI789	250	8.15	225.00	15
Calculations

The application applies the following pricing logic:

Shipping Per Unit = Shipping Cost / Quantity

Landed Cost = Unit Cost + Shipping Per Unit

Quote Price = Landed Cost × (1 + Markup / 100)

Example:

Quantity:        500
Unit Cost:       $4.25
Shipping Cost:   $350.00
Markup:          20%

Shipping / Unit: $0.70
Landed Cost:     $4.95
Quote Price:     $5.94

Monetary results are rounded to two decimal places.

Validation

Each row is validated before any calculations are performed.

The application checks for:

Missing SKU values
Non-numeric quantities
Zero or negative quantities
Fractional quantities
Negative unit costs
Negative shipping costs
Non-numeric pricing fields
Markup values outside the configured limits

Validation is designed to collect all errors for a row in one pass rather than stopping at the first failure.

Invalid rows are excluded from quote calculations and written to the Errors worksheet.

Excel Output

The generated workbook contains a formatted Results worksheet with:

SKU
Quantity
Unit Cost
Shipping Cost
Markup
Shipping Per Unit
Landed Cost
Quote Price

The Results worksheet includes:

Excel table formatting
Filtering and sorting
Currency formatting
Percentage formatting
Frozen header row
Readable column widths

If invalid rows are detected, an Errors worksheet is added containing:

SKU
All validation messages associated with that row

This allows valid rows to continue processing even when other rows contain bad input.

Configuration

Business rules are stored separately from the calculation logic in config.json.

Example:

{
  "minimum_markup": 0,
  "maximum_markup": 100,
  "currency": "USD",
  "output_filename": "quote_results.xlsx"
}

This allows configurable values to be changed without modifying the core calculation code.

Project Structure
bulk_quote_calculator/
│
├── calculator.py
├── config.json
├── config_loader.py
├── excel_io.py
├── gui.py
├── main.py
├── validator.py
│
├── tests/
│   ├── test_calculator.py
│   ├── test_validator.py
│   └── test_process_quotes.py
│
├── assets/
│   ├── gui.png
│   ├── results.png
│   └── errors.png
│
├── sample_input.xlsx
├── requirements.txt
├── LICENSE
└── README.md
Module Responsibilities
calculator.py

Contains the core pricing calculations.

The calculation layer is kept separate from Excel handling and the GUI so it can be independently tested and reused.

validator.py

Validates incoming quote data and returns all detected validation errors for each row.

excel_io.py

Handles:

Excel workbook input
Excel workbook output
Worksheet creation
Formatting
Excel table generation
Results and Errors sheets
config_loader.py

Loads external configuration values from config.json.

main.py

Coordinates the complete processing workflow:

Read Input
→ Validate Rows
→ Calculate Valid Quotes
→ Separate Errors
→ Write Output Workbook
gui.py

Provides the Tkinter desktop interface.

The GUI is intentionally kept separate from calculation and Excel logic.

tests/

Contains unit and integration tests for the application's core behavior.

Installation

Clone the repository:

git clone https://github.com/magliarozach-phntm/bulk_quote_calculator.git
cd bulk_quote_calculator

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt
Requirements

The project uses:

openpyxl==3.1.5
pytest==9.1.1
pyinstaller==6.22.2

Tkinter is included with standard Python installations on Windows and does not require a separate pip package.

Running the Application

Start the desktop application:

python gui.py

Then:

Click Browse
Select an Excel workbook
Click Calculate Quotes
Review the processing summary
Click Open Results
Review the generated Results and Errors worksheets
Testing

The project uses pytest for automated testing.

Run the full test suite:

python -m pytest -v

Current tests cover:

Quote calculations
Valid row handling
Invalid row handling
Configurable markup limits
Multi-error validation
Integer-like Excel quantities
End-to-end Excel input/output processing
Results workbook creation
Errors worksheet creation

The integration test creates temporary Excel files during testing and verifies the complete application pipeline.

Windows Executable

The application can be packaged as a standalone Windows executable using PyInstaller.

Build with:

python -m PyInstaller --onefile --windowed --name BulkQuoteCalculator gui.py

The executable is generated in:

dist/BulkQuoteCalculator.exe

For the packaged version, config.json should remain alongside the executable:

dist/
├── BulkQuoteCalculator.exe
└── config.json

Keeping configuration external allows business rules to be edited without rebuilding the executable.

Design Goals

This project was built around several software design principles:

Separation of concerns
Business logic independent from UI code
Configurable business rules
Defensive input validation
Batch processing that continues when individual rows fail
Clear audit-friendly Excel output
Automated testing
Maintainable modular structure
Simple workflow for non-technical users
Technologies
Python 3
Tkinter
openpyxl
pytest
JSON
PyInstaller
Microsoft Excel
Potential Extensions

The architecture could be extended to support:

Additional pricing rules
Configurable rate tables
Multiple quote types
Additional Excel templates
More complex landed-cost calculations
Audit logging
User-selectable output locations
Additional business validation rules
License

This project is licensed under the MIT License.
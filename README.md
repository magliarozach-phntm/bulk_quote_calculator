# Bulk Quote Calculator

A desktop Python application for importing quote data from Excel, validating each row, applying configurable pricing rules, and exporting formatted quote results and validation errors.

This project demonstrates practical business-process automation using Python, Tkinter, `openpyxl`, JSON configuration, automated testing with `pytest`, and Windows packaging with PyInstaller.

## Screenshot

### Desktop Application

![Bulk Quote Calculator GUI](assets/gui.png)



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
```

From the user's perspective:

```text
Select Excel File → Calculate Quotes → Review Results
```

## Input Format

The input workbook should contain the following columns:

| Column | Description |
|---|---|
| SKU | Product identifier |
| Quantity | Number of units |
| Unit Cost | Cost per individual unit |
| Shipping Cost | Total shipping cost |
| Markup | Desired markup percentage |

Example:

| SKU | Quantity | Unit Cost | Shipping Cost | Markup |
|---|---:|---:|---:|---:|
| ABC123 | 500 | 4.25 | 350.00 | 20 |
| DEF456 | 1200 | 2.80 | 500.00 | 25 |
| GHI789 | 250 | 8.15 | 225.00 | 15 |

## Calculations

The application applies the following pricing logic:

```text
Shipping Per Unit = Shipping Cost / Quantity

Landed Cost = Unit Cost + Shipping Per Unit

Quote Price = Landed Cost × (1 + Markup / 100)
```

Example:

```text
Quantity:        500
Unit Cost:       $4.25
Shipping Cost:   $350.00
Markup:          20%

Shipping / Unit: $0.70
Landed Cost:     $4.95
Quote Price:     $5.94
```

Monetary results are rounded to two decimal places.

## Validation

Each row is validated before calculations are performed.

The application checks for:

- Missing SKU values
- Non-numeric quantities
- Zero or negative quantities
- Fractional quantities
- Negative unit costs
- Negative shipping costs
- Non-numeric pricing fields
- Markup values outside configured limits

Validation collects all errors for a row in one pass rather than stopping after the first failure.

Invalid rows are excluded from quote calculations and written to the `Errors` worksheet.

## Excel Output

The generated workbook contains a formatted `Results` worksheet with:

- SKU
- Quantity
- Unit Cost
- Shipping Cost
- Markup
- Shipping Per Unit
- Landed Cost
- Quote Price

The Results worksheet includes:

- Excel table formatting
- Filtering and sorting
- Currency formatting
- Percentage formatting
- Frozen header row
- Readable column widths

If invalid rows are detected, an `Errors` worksheet is created containing:

- SKU
- All validation messages associated with that row

This allows valid rows to continue processing even when other rows contain invalid input.

## Configuration

Business rules are stored separately from the calculation logic in `config.json`.

Example:

```json
{
  "minimum_markup": 0,
  "maximum_markup": 100,
  "currency": "USD",
  "output_filename": "quote_results.xlsx"
}
```

This allows configurable values to be changed without modifying the core application logic.

## Project Structure

```text
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
└── README.md
```

## Module Responsibilities

### `calculator.py`

Contains the core pricing calculations.

The calculation layer is kept separate from Excel handling and the graphical interface so it can be independently tested and reused.

### `validator.py`

Validates incoming quote data and returns all detected validation errors for each row.

### `excel_io.py`

Handles:

- Excel workbook input
- Excel workbook output
- Worksheet creation
- Formatting
- Excel table generation
- Results and Errors sheets

### `config_loader.py`

Loads external application configuration from `config.json`.

### `main.py`

Coordinates the complete processing workflow:

```text
Read Input
→ Validate Rows
→ Calculate Valid Quotes
→ Separate Errors
→ Write Output Workbook
```

### `gui.py`

Provides the Tkinter desktop interface.

The GUI is intentionally separated from calculation, validation, and Excel-processing logic.

### `tests/`

Contains unit and integration tests for the application's core behavior.

## Installation

Clone the repository:

```bash
git clone https://github.com/magliarozach-phntm/bulk_quote_calculator.git
cd bulk_quote_calculator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Requirements

The project uses:

```text
openpyxl==3.1.5
pytest==9.1.1
pyinstaller==6.22.2
```

Tkinter is included with standard Python installations on Windows and does not require a separate pip package.

## Running the Application

Start the desktop application:

```bash
python gui.py
```

Then:

1. Click **Browse**
2. Select an Excel workbook
3. Click **Calculate Quotes**
4. Review the processing summary
5. Click **Open Results**
6. Review the generated Results and Errors worksheets

## Testing

The project uses `pytest` for automated testing.

Run the full test suite:

```bash
python -m pytest -v
```

Tests cover:

- Quote calculations
- Valid row handling
- Invalid row handling
- Configurable markup limits
- Multi-error validation
- Integer-like Excel quantities
- End-to-end Excel input/output processing
- Results workbook creation
- Errors worksheet creation

The integration test creates temporary Excel workbooks and verifies the complete application pipeline.

## Windows Executable

The application can be packaged as a standalone Windows executable using PyInstaller.

Build with:

```bash
python -m PyInstaller --onefile --windowed --name BulkQuoteCalculator gui.py
```

The executable is generated in:

```text
dist/BulkQuoteCalculator.exe
```

For the packaged version, `config.json` remains alongside the executable:

```text
dist/
├── BulkQuoteCalculator.exe
└── config.json
```

Keeping configuration external allows configurable business rules to be edited without rebuilding the executable.

## Design Goals

This project was built around several software design principles:

- Separation of concerns
- Business logic independent from UI code
- Configurable business rules
- Defensive input validation
- Batch processing that continues when individual rows fail
- Clear and audit-friendly Excel output
- Automated testing
- Maintainable modular Python architecture
- Simple workflow for non-technical users

## Technologies

- Python 3
- Tkinter
- openpyxl
- pytest
- JSON
- PyInstaller
- Microsoft Excel

## Potential Extensions

The architecture could be extended to support:

- Additional pricing rules
- Configurable rate tables
- Multiple quote types
- Additional Excel templates
- More complex landed-cost calculations
- Audit logging
- User-selectable output locations
- Additional business validation rules

## Purpose of This Repository

This repository is published as a portfolio project demonstrating Python desktop application development, Excel automation, configurable business-rule processing, validation, testing, and application packaging.

It is not a production implementation for any specific company, client, warehouse, pricing model, or proprietary business process.

## Copyright and Usage

Copyright © 2026 Zachary Magliaro. All rights reserved.

This source code is made publicly viewable for portfolio, educational review, and professional evaluation purposes only.

No permission is granted to copy, modify, redistribute, sublicense, sell, incorporate into another product, or use this software or substantial portions of this software for commercial purposes without prior written permission from the copyright holder.

Viewing this repository does not constitute a license to use the source code.

For licensing or commercial-use inquiries, please contact the repository owner.
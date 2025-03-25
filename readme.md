# Invoice Generator

This is an **Invoice Generator** designed specifically for freelancers who want to easily generate professional invoices without manually creating them. Simply track your hours in a spreadsheet, save it as a CSV file, and enter the csv file name/path in line 134, before running this script to generate a PDF invoice.

I have included a sample csv file, which you can import to google sheets. Make sure to leave the row named: "Total." To easily calculate the Daily cost, use the following formula in your spreadsheet:=PRODUCT(E2,F2), this will multiply the daily hours worked by the hourly rate. (Make sure that the daily hours and hourly rate columns are located in columns E and F). Use the following formula to determined the total amount owed to you, =SUM(G2:G14) (make sure that your daily cost column is located in column G and adjust 'G14' if needed, to include all of the days you ar tracking).


## Features

- **Automated CSV Parsing:** Reads your timesheet CSV to extract relevant data.
- **Invoice Creation:** Uses the ReportLab library to generate a well-formatted invoice PDF.
- **Customizable:** Easily adjust invoice details such as billing information and invoice number.
- **Quick Totals Calculation:** Automatically computes total hours and total cost.

## How It Works

1. **CSV Input:** Track your working hours and related billing information in a spreadsheet. Save the file as a CSV.
2. **Data Filtering:** The script reads the CSV, extracts necessary columns (e.g., task details, daily hours, hourly rate, and daily cost), and computes the totals.
3. **PDF Generation:** Using ReportLab, it creates a PDF with a header section for billing details and an invoice table for your recorded work.
4. **Customization:** You can modify the header information directly in the script (lines 71-72) to include your personal or business details.

# Script Requirements:#
- **Python**
- **ReportLab Library:** Install via pip if not already installed:
 in terminal or command prompt:
  pip install reportlab


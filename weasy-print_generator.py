import csv
from weasyprint import HTML

def create_invoice(csv_filename, output_pdf):
    # 1. Read the CSV
    with open(csv_filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        print("CSV file is empty.")
        return

    header = rows[0]
    data_rows = rows[1:]
    
    # Define which columns we want (similar to ReportLab example: 0 to 6)
    columns_we_want = list(range(7))
    filtered_header = [header[i] for i in columns_we_want]
    
    # 2. Build the invoice table data and calculate totals
    table_header_html = "".join(f"<th>{col}</th>" for col in filtered_header)
    table_rows_html = ""
    total_hours = 0.0
    total_cost = 0.0

    for row in data_rows:
        if all(not cell.strip() for cell in row):
            # Skip empty rows
            continue
        if row[0].strip().lower() == "total":
            # Skip rows marked as "Total"
            continue

        # Filter the row
        filtered_row = [row[i] for i in columns_we_want]
        # Attempt to parse numeric values (Daily Hours = column 4, Daily Cost = column 6)
        hours_str = filtered_row[4].replace("$", "").strip()
        cost_str  = filtered_row[6].replace("$", "").strip()

        try:
            daily_hours = float(hours_str) if hours_str else 0.0
        except ValueError:
            daily_hours = 0.0
        try:
            daily_cost = float(cost_str) if cost_str else 0.0
        except ValueError:
            daily_cost = 0.0

        total_hours += daily_hours
        total_cost  += daily_cost

        # Create an HTML row for the invoice table
        row_html = "".join(f"<td>{cell}</td>" for cell in filtered_row)
        table_rows_html += f"<tr>{row_html}</tr>\n"
    
    # 3. Build the HTML invoice template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Invoice Report</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          margin: 20px;
        }}
        .header-section {{
          display: flex;
          justify-content: space-between;
          margin-bottom: 20px;
        }}
        .header-box {{
          width: 45%;
        }}
        .header-box p {{
          margin: 5px 0;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 20px;
        }}
        th, td {{
          border: 1px solid #333;
          padding: 8px;
          text-align: left;
        }}
        th {{
          background-color: steelblue;
          color: white;
        }}
        .totals {{
          display: flex;
          justify-content: space-between;
          font-weight: bold;
          margin-top: 10px;
        }}
        hr {{
          border: none;
          border-top: 1px solid #333;
          margin: 20px 0;
        }}
      </style>
    </head>
    <body>
      <div class="header-section">
        <div class="header-box">
          <p><strong>BILLED TO:</strong><br/>Company Name Here</p>
        </div>
        <div class="header-box" style="text-align:right;">
          <p><strong>INVOICE</strong><br/>#INVOICE_NUMBER_HERE</p>
        </div>
      </div>
      <div class="header-section">
        <div class="header-box">
          <p><strong>PAY TO:</strong><br/>Your Name Here</p>
        </div>
        <div class="header-box" style="text-align:right;">
          <p><strong>Address:</strong><br/>Your Address Here</p>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            {table_header_html}
          </tr>
        </thead>
        <tbody>
          {table_rows_html}
        </tbody>
      </table>
      <hr/>
      <div class="totals">
        <div>Total Hours: {total_hours:.2f}</div>
        <div>Total Cost: ${total_cost:.2f}</div>
      </div>
    </body>
    </html>
    """
    
    # 4. Generate the PDF using WeasyPrint
    HTML(string=html_template).write_pdf(output_pdf)
    print(f"Invoice created successfully: {output_pdf}")

if __name__ == "__main__":
    # Change the file names as needed.
    create_invoice("dummy.csv", "your_invoice.pdf")

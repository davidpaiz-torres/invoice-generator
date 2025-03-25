import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT

def create_invoice(csv_filename, output_pdf):
    # 1. Read the CSV
    with open(csv_filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader) 

    header = rows[0]
    data_rows = rows[1:]

    # 2. Build the filtered main table data
    columns_we_want = [0, 1, 2, 3, 4, 5, 6] 

    # Filtered header
    main_header = [header[i] for i in columns_we_want]
    main_table_data = [main_header]

    # 3. Compute total hours & total cost
    total_hours = 0.0
    total_cost = 0.0

    for row in data_rows:
        if all(not cell.strip() for cell in row):
            # Skip empty rows
            continue
        if row[0].strip().lower() == "total":
            # Skip the "Total" row
            continue
        
        filtered_row = [row[i] for i in columns_we_want]

        # Convert numeric columns to float (Daily Hours = col 4, Hourly Rate=col 5, Daily Cost=col 6)
        # Remove any "$" sign if present, TO AVOID CONVERSION ERRORS
        hours_str = filtered_row[4].replace("$", "").strip()
        cost_str  = filtered_row[6].replace("$", "").strip()

        daily_hours = float(hours_str) if hours_str else 0.0
        daily_cost  = float(cost_str)  if cost_str else 0.0

        total_hours += daily_hours
        total_cost  += daily_cost

        main_table_data.append(filtered_row)

    # 4. Set up the PDF document
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # 5. Create a list for PDF elements
    elements = []

    # HEADER SECTION
    header_data = [
        [
            Paragraph("<b>BILLED TO:</b><br/>Comapny Name Here", normal_style),
            Paragraph("<para alignment='right'><b>INVOICE</b><br/>#INVOICE_NUMBER_HERE</para>", normal_style)
        ],
        [
            Paragraph("<b>PAY TO:</b><br/>Your Name Here", normal_style),
            Paragraph("<para alignment='right'><b>Address:</b><br/>Your Address Here</para>", normal_style),
        ]
    ]
    header_table = Table(header_data, colWidths=[300, 200])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # INVOICE TABLE
    invoice_table = Table(
        main_table_data,
        colWidths=[60, 70, 70, 140, 60, 60, 60]  # Adjust this if your table apprears too wide or too narrow
    )
    invoice_table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        # Grid lines
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        # Right-align numeric columns (Daily Hours=4, Hourly Rate=5, Daily Cost=6)
        ('ALIGN', (4, 1), (6, -1), 'RIGHT'),
    ]))
    elements.append(invoice_table)


    # HORIZONTAL LINE BELOW TABLE
    elements.append(Spacer(1, 12))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 8))

    totals_row = [
    Paragraph(f"<b>Total Hours:</b> {total_hours:.2f}", normal_style),
    Paragraph(f"<b>Total Cost:</b> ${total_cost:.2f}", normal_style)
]

    totals_table = Table([totals_row], colWidths=["50%", "50%"])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(totals_table)

    # 6. Build the PDF
    doc.build(elements)
    print(f"Invoice created successfully: {output_pdf}")

if __name__ == "__main__":
    create_invoice(
        "your_timesheet.csv", # include file path if it's not in the same folder as this script
        "your_invoice.pdf" # include file path if you want to save it in a specific folder
    )

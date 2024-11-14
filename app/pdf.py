from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
import os

def create_application_pdf(data, filename="application.pdf", save_path="./pdf/applications", logo_path="./static/img/staysync_logo_black.jpg"):
    # Ensure the directory exists
    os.makedirs(save_path, exist_ok=True)
    
    # Full path for saving the PDF
    full_path = os.path.join(save_path, filename)

    c = canvas.Canvas(full_path, pagesize=A4)
    width, height = A4

    # Center the logo at the top if available
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_width = 1.5 * inch
        c.drawImage(logo, (width - logo_width) / 2, height - 120, width=logo_width, height=1.5 * inch, preserveAspectRatio=True)

    # Title - Centered and positioned below the logo
    c.setFont("Helvetica-Bold", 18)
    title = "Hostel Application Confirmation"
    c.drawCentredString(width / 2, height - 160, title)

    # Subtitle - Centered below the title
    c.setFont("Helvetica", 12)
    subtitle = "Thank you for your hostel application. Here are your submitted details:"
    c.drawCentredString(width / 2, height - 190, subtitle)

    # Increase space before the table
    table_start_y = height - 450  # Increased spacing

    # Table Data - Format the data dictionary for the table
    table_data = [["Field", "Details"]]  # Header row
    table_data += [[field.replace("_", " ").title(), value] for field, value in data.items()]

    # Table Style
    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.teal),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Draw the table on the canvas, positioned further down
    table_x = 100
    table.wrapOn(c, width, height)
    table.drawOn(c, table_x, table_start_y)

    # Footer
    c.setFont("Helvetica", 10)
    footer_text = "Please review your details above. Contact us if any information is incorrect."
    c.drawCentredString(width / 2, 80, footer_text)

    disclaimer_text = "Disclaimer: This report has been automatically generated by a bot."
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 20, disclaimer_text)

    # Finalize and save the PDF
    c.showPage()
    c.save()
    
    print(f"PDF saved at {full_path}")
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from pathlib import Path


class PDFGenerator:
    def __init__(self, output_path, logo_path=None):
        """Initialize PDF generator."""
        self.output_path = output_path
        self.logo_path = logo_path
        self.story = []
        # this must exist before _setup_custom_styles()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=12
        ))

        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
    
    def _header_footer(self, canvas, doc):
     canvas.saveState()

    # header top reference (SAFE here)
     header_top = doc.height + doc.topMargin

    # Row 1: Title
     title_y = header_top - 0.4 * inch
     if hasattr(self, 'report_title'):
        canvas.setFont('Helvetica-Bold', 15)
        canvas.drawCentredString(
            doc.leftMargin + doc.width / 2,
            title_y,
            self.report_title
        )

    # Row 2: Logo + Timestamp
     row2_y = title_y - 0.45 * inch

     if self.logo_path and Path(self.logo_path).exists():
        try:
            logo_width = 1.4 * inch
            logo_height = 0.45 * inch
            logo = Image(self.logo_path, logo_width, logo_height)
            logo.drawOn(canvas, doc.leftMargin, row2_y - logo_height)
        except:
            pass

     if hasattr(self, 'timestamp'):
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(
            doc.leftMargin + doc.width,
            row2_y - 0.15 * inch,
            self.timestamp
        )

    # Row 3: Farmer name
     farmer_y = row2_y - 0.55 * inch
     if hasattr(self, 'farmer_name'):
        canvas.setFont('Helvetica', 10)
        canvas.drawString(
            doc.leftMargin,
            farmer_y,
            f"Farmer: {self.farmer_name}"
        )

    # Footer
     canvas.setFont('Helvetica', 9)
     canvas.setFillColor(colors.grey)
     canvas.drawCentredString(
        doc.leftMargin + doc.width / 2,
        0.5 * inch,
        "Proudly maintained accounting with GramIQ"
    )

     canvas.restoreState()



    def generate_pdf(self, data):
        """
        Generate the complete PDF report.
        
        Args:
            data: Dictionary containing all report data
        """
        # Extract data
        farmer_name = data.get('farmer_name', '')
        crop_name = data.get('crop_name', '')
        season = data.get('season', '')
        total_acres = data.get('total_acres', 0)
        year = datetime.now().year
        
        # Set dynamic title
        self.report_title = f"{crop_name} _ {total_acres} Acres _ {season} {year}"
        self.timestamp = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.farmer_name = farmer_name
        
        # Create PDF document
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1.5*inch,
            bottomMargin=1*inch
        )
        
        # Build content
        self._add_finance_summary(data)
        self._add_expense_breakdown(data)
        self._add_income_breakdown(data)
        self._add_ledger(data)
        
        # Build PDF with header/footer
        doc.build(self.story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
    
    def _add_finance_summary(self, data):
        """Add Section 1: Finance Summary."""
        self.story.append(Paragraph("Finance Summary", self.styles['SectionHeading']))
        self.story.append(Spacer(1, 0.6 * inch))

        
        # Summary data
        total_income = data.get('total_income', 0)
        total_expense = data.get('total_expense', 0)
        total_production = data.get('total_production', 0)  # Assuming this is provided
        profit_loss = data.get('profit_or_loss', 0)
        cost_per_acre = data.get('cost_per_acre', 0)
        
        summary_data = [
            ['Metric', 'Amount (₹)'],
            ['Total Income', f'{total_income:,.2f}'],
            ['Total Expense', f'{total_expense:,.2f}'],
            ['Total Production', f'{total_production:,.2f}'],
            ['Profit/Loss', f'{profit_loss:,.2f}'],
            ['Cost of Cultivation per Acre', f'{cost_per_acre:,.2f}']
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        self.story.append(summary_table)
        self.story.append(Spacer(1, 0.6 * inch))
        
        # Embed chart
        chart_path = data.get('chart_path')
        if chart_path and Path(chart_path).exists():
            try:
                chart_img = Image(chart_path, width=5*inch, height=3.75*inch)
                self.story.append(chart_img)
                self.story.append(Spacer(1, 0.3*inch))
            except:
                pass  # Skip chart if image can't be loaded
        
        self.story.append(PageBreak())
    
    def _add_expense_breakdown(self, data):
        """Add Section 3: Expense Breakdown Table."""
        self.story.append(Paragraph("Expense Breakdown", self.styles['SectionHeading']))
        self.story.append(Spacer(1, 0.6 * inch))
        
        expenses = data.get('expenses', [])
        
        if not expenses:
            self.story.append(Paragraph("No expense records found.", self.styles['Normal']))
            self.story.append(Spacer(1, 0.3*inch))
            return
        
        # Table headers
        expense_data = [['Category', 'Amount (₹)', 'Date', 'Description']]
        
        # Add expense rows
        for expense in expenses:
            expense_data.append([
                expense.get('category', ''),
                f"{expense.get('amount', 0):,.2f}",
                expense.get('date', ''),
                expense.get('description', '') or '-'
            ])
        
        expense_table = Table(expense_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 2.3*inch])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        self.story.append(expense_table)
        self.story.append(Spacer(1, 0.3*inch))
        self.story.append(PageBreak())
    
    def _add_income_breakdown(self, data):
        """Add Section 4: Income Breakdown Table."""
        self.story.append(Paragraph("Income Breakdown", self.styles['SectionHeading']))
        self.story.append(Spacer(1, 0.6 * inch))
        
        incomes = data.get('incomes', [])
        
        if not incomes:
            self.story.append(Paragraph("No income records found.", self.styles['Normal']))
            self.story.append(Spacer(1, 0.3*inch))
            return
        
        # Table headers
        income_data = [['Category', 'Amount (₹)', 'Date', 'Description']]
        
        # Add income rows
        for income in incomes:
            income_data.append([
                income.get('category', ''),
                f"{income.get('amount', 0):,.2f}",
                income.get('date', ''),
                income.get('description', '') or '-'
            ])
        
        income_table = Table(income_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 2.3*inch])
        income_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        self.story.append(income_table)
        self.story.append(Spacer(1, 0.3*inch))
        self.story.append(PageBreak())
    
    def _add_ledger(self, data):
        """Add Section 5: Ledger (merged income + expense)."""
        self.story.append(Paragraph("Ledger", self.styles['SectionHeading']))
        self.story.append(Spacer(1, 0.6 * inch))
        
        # Combine and sort by date
        ledger_entries = []
        
        # Add expenses
        for expense in data.get('expenses', []):
            ledger_entries.append({
                'date': expense.get('date', ''),
                'particulars': expense.get('category', ''),
                'type': 'Expense',
                'description': expense.get('description', '') or '-',
                'amount': expense.get('amount', 0)
            })
        
        # Add incomes
        for income in data.get('incomes', []):
            ledger_entries.append({
                'date': income.get('date', ''),
                'particulars': income.get('category', ''),
                'type': 'Income',
                'description': income.get('description', '') or '-',
                'amount': income.get('amount', 0)
            })
        
        # Sort by date
        ledger_entries.sort(key=lambda x: x['date'])
        
        if not ledger_entries:
            self.story.append(Paragraph("No ledger entries found.", self.styles['Normal']))
            return
        
        # Table headers
        ledger_data = [['Date', 'Particulars', 'Type', 'Description', 'Amount (₹)']]
        
        # Add ledger rows
        for entry in ledger_entries:
            ledger_data.append([
                entry['date'],
                entry['particulars'],
                entry['type'],
                entry['description'],
                f"{entry['amount']:,.2f}"
            ])
        
        ledger_table = Table(ledger_data, colWidths=[1*inch, 1.2*inch, 0.8*inch, 1.8*inch, 1.2*inch])
        ledger_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        self.story.append(ledger_table)


def generate_pdf_report(data, output_path, logo_path=None):
    """
    Convenience function to generate PDF report.
    
    Args:
        data: Dictionary containing all report data
        output_path: Path where PDF will be saved
        logo_path: Optional path to logo image
        
    Returns:
        str: Path to generated PDF
    """
    generator = PDFGenerator(output_path, logo_path)
    generator.generate_pdf(data)
    return output_path
# GramIQ Farm Finance Report

A Flask-based web application for generating comprehensive PDF financial reports for farm operations. This application helps farmers track income, expenses, and calculate key financial metrics with visual charts and detailed breakdowns.

---

## 📋 Project Overview

GramIQ Farm Finance Report simplifies farm financial record-keeping and reporting. Farmers can input crop details, income, and expense information through a user-friendly web form, and automatically generate a professional PDF report with financial summaries, charts, and detailed breakdowns.

---

## ✨ Features

- **Interactive Web Form:** Easy-to-use HTML form for entering farm and financial data.  
- **Financial Calculations:** Automatic calculation of:
  - Total income and expenses
  - Profit or loss
  - Cost of cultivation per acre
- **Visual Charts:** Bar chart comparing income vs expenses using Matplotlib.  
- **Comprehensive PDF Reports:** Professional PDF reports including:
  - Finance summary table
  - Income vs expense comparison chart
  - Detailed expense breakdown
  - Detailed income breakdown
  - Complete ledger (merged income and expense entries)
- **Multi-Entry Support:** Support for multiple income and expense entries.  
- **Professional Formatting:** Clean, organized PDF layout with headers and footers on every page.  
- **Error Handling:** Robust error handling with user-friendly messages.

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher  
- pip (Python package installer)

### Installation Steps
1. Clone or download the repository:
   ```bash
   git clone <repository_url>
   cd Gram-IQ-farm-finance-report

2. Create a virtual environment:
   ```bash
   python -m venv venv

3. Activate the virtual environment:
   -Windows: venv\Scripts\activate
   -macOS/Linux: source venv/bin/activate

4. Install Dependencies:
   ```bash
   pip install -r requirements.txt

5. Verify installation:
   Ensure the following directories exist (they are auto-created if missing):

   -static/charts/ - for generated chart images

   -static/images/ - for logo (optional)

   -reports/ - for generated PDF files

   -templates/ - for HTML templates

templates

🏃 How to Run the Application

1.Start the Flask development server:
   python app.py

2.Access the application in your web browser at:
  http://localhost:5000


3.Generate a Report:

Fill in the form with:

Farmer and crop details (name, crop, season, acres, dates, location)
Expense information (category, amount, date, description)
Income information (category, amount, date, description)

Click Generate Report
The PDF will be automatically downloaded.

4.View Generated Files:
-PDF reports are saved in the reports/ directory
-Chart images are saved in the static/charts/ directory

📚 Libraries Used

-Flask (3.0.0): Web framework for building the application.
-Werkzeug (3.0.1): WSGI utilities library, Flask dependency.
-ReportLab (4.0.7): PDF generation library for creating professional reports.
-Matplotlib (3.8.2): Charting library for generating income vs expense visualizations.

📁 Project Structure
Gram-IQ-farm-finance-report/
├── app.py                # Main Flask application
├── utils.py              # Financial calculation utilities
├── chart_generator.py    # Chart generation module
├── pdf_generator.py      # PDF report generation module
├── requirements.txt      # Python dependencies
├── templates/
│   └── form.html         # Web form template
├── static/
│   ├── images/
│   │   └── logo.png      # GramIQ logo (optional)
│   └── charts/           # Generated chart images
└── reports/              # Generated PDF reports

Configuration
The application runs in debug mode by default. For production, edit app.py and set:
app.run(debug=False)
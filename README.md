# Gram-IQ-farm-finance-report
# GramIQ Farm Finance Report

A Flask-based web application for generating comprehensive PDF financial reports for farm operations. This application helps farmers track income, expenses, and calculate key financial metrics with visual charts and detailed breakdowns.

## 📋 Project Overview

GramIQ Farm Finance Report is a web application designed to simplify farm financial record-keeping and reporting. It allows farmers to input their crop details, income, and expense information through a user-friendly web form, and automatically generates a professional PDF report with financial summaries, charts, and detailed breakdowns.

## ✨ Features

- **Interactive Web Form**: Easy-to-use HTML form for entering farm and financial data
- **Financial Calculations**: Automatic calculation of:
  - Total income and expenses
  - Profit or loss
  - Cost of cultivation per acre
- **Visual Charts**: Bar chart comparing income vs expenses using matplotlib
- **Comprehensive PDF Reports**: Professional PDF reports with:
  - Finance summary table
  - Income vs expense comparison chart
  - Detailed expense breakdown
  - Detailed income breakdown
  - Complete ledger (merged income and expense entries)
- **Multi-Entry Support**: Support for multiple income and expense entries
- **Professional Formatting**: Clean, organized PDF layout with headers and footers on every page
- **Error Handling**: Robust error handling with user-friendly messages

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the repository**
   cd Gram-IQ-farm-finance-report
   2. **Create a virtual environment (recommended)**
   
   python -m venv venv
   3. **Activate the virtual environment**
   
   On Windows:
   venv\Scripts\activate
      
   On macOS/Linux:
   source venv/bin/activate
   4. **Install dependencies**
   
   pip install -r requirements.txt
   5. **Verify installation**
   - Ensure all required directories exist:
     - `static/charts/` - for generated chart images
     - `static/images/` - for logo (optional)
     - `reports/` - for generated PDF files
     - `templates/` - for HTML templates
   - These directories are created automatically when the application runs

## 🏃 How to Run the Application

1. **Start the Flask development server**
 
   python app.py
   2. **Access the application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - You should see the Farm Finance Report Form

3. **Generate a Report**
   - Fill in the form with:
     - Farmer and crop details (name, crop, season, acres, dates, location)
     - Expense information (category, amount, date, description)
     - Income information (category, amount, date, description)
   - Click "Generate Report"
   - The PDF will be automatically downloaded

4. **View Generated Files**
   - PDF reports are saved in the `reports/` directory
   - Chart images are saved in the `static/charts/` directory

## 📚 Libraries Used

- **Flask (3.0.0)**: Web framework for building the application and handling HTTP requests
- **Werkzeug (3.0.1)**: WSGI utilities library, Flask dependency
- **ReportLab (4.0.7)**: PDF generation library for creating professional reports
- **Matplotlib (3.8.2)**: Charting library for generating income vs expense visualizations

## 📁 Project Structure
Gram-IQ-farm-finance-report/
├── app.py                 # Main Flask application
├── utils.py              # Financial calculation utilities
├── chart_generator.py     # Chart generation module
├── pdf_generator.py       # PDF report generation module
├── requirements.txt       # Python dependencies
├── templates/
│   └── form.html         # Web form template
├── static/
│   ├── images/
│   │   └── logo.png      # GramIQ logo (optional)
│   └── charts/           # Generated chart images
└── reports/              # Generated PDF reports

2.Create a virtual environment
   python -m venv venvnk to demo video will be added here]

## 🔧 Configuration

The application runs in debug mode by default. To change this:

- Edit `app.py` and modify the last line:
  
  app.run(debug=False)  # Set to False for production
  ## 📝 Notes

- The logo is optional - the application will work without it
- Generated PDFs and charts are saved with timestamped filenames
- The application supports both single and multiple income/expense entries
- All financial calculations are performed server-side for accuracy

## 🤝 Contributing

This is a project for GramIQ farm finance reporting. For contributions or issues, please contact the development team.

## 📄 License

[Add your license information here]

---

**Developed for GramIQ** - Proudly maintained accounting with GramIQ

3. Activate the virtual environment
On Windows:
     venv\Scripts\activate
On macOS/Linux:
         source venv/bin/activate

4. Install dependencies
        pip install -r requirements.txt

🏃 How to Run the Application
1.Start the Flask development server
     python app.py

2. Access the application
-Open your web browser
-Navigate to: http://localhost:5000
-You should see the Farm Finance Report Form

3. Generate a Report
-Fill in the form with:
-Farmer and crop details (name, crop, season, acres, dates, location)
-Expense information (category, amount, date, description)
-Income information (category, amount, date, description)
-Click "Generate Report"
-The PDF will be automatically downloaded

4. View Generated Files
-PDF reports are saved in the reports/ directory
-Chart images are saved in the static/charts/ directory

📚 Libraries Used
-Flask (3.0.0): Web framework for building the application and handling HTTP requests
-Werkzeug (3.0.1): WSGI utilities library, Flask dependency
-ReportLab (4.0.7): PDF generation library for creating professional reports
-Matplotlib (3.8.2): Charting library for generating income vs expense visualizations

🎥 Demo Video


🔧 Configuration
The application runs in debug mode by default. To change this:
-Edit app.py and modify the last 
     app.run(debug=False)  # Set to False for production
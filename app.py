from flask import Flask, render_template, request, send_file
from pathlib import Path
import os
from datetime import datetime
import traceback

from utils import (
    calculate_total_income,
    calculate_total_expense,
    calculate_profit_or_loss,
    calculate_cost_of_cultivation_per_acre
)
from chart_generator import generate_income_expense_chart
from pdf_generator import generate_pdf_report

app = Flask(__name__)

# Create necessary directories
Path('static/charts').mkdir(parents=True, exist_ok=True)
Path('reports').mkdir(parents=True, exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    """Render the form page."""
    return render_template('form.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate PDF report from form data."""
    try:
        # Parse form data
        form_data = request.form
        
        # Extract farmer & crop details
        farmer_name = form_data.get('farmer_name', '').strip()
        crop_name = form_data.get('crop_name', '').strip()
        season = form_data.get('season', '').strip()
        total_acres = float(form_data.get('total_acres', 0))
        date_of_sowing = form_data.get('date_of_sowing', '')
        date_of_harvest = form_data.get('date_of_harvest', '')
        location = form_data.get('location', '').strip()
        
        # Validate required fields
        if not all([farmer_name, crop_name, season, total_acres > 0]):
            return render_template('form.html', error='Please fill in all required fields.'), 400
        
        # Parse expense data (support multiple entries)
        expenses = []
        expense_categories = form_data.getlist('expense_category')
        expense_amounts = form_data.getlist('expense_amount')
        expense_dates = form_data.getlist('expense_date')
        expense_descriptions = form_data.getlist('expense_description')
        
        # If single entry (current form structure)
        if not expense_categories and form_data.get('expense_category'):
            expense_categories = [form_data.get('expense_category')]
            expense_amounts = [form_data.get('expense_amount')]
            expense_dates = [form_data.get('expense_date')]
            expense_descriptions = [form_data.get('expense_description', '')]
        
        # Build expense list
        for i in range(len(expense_categories)):
            if expense_categories[i] and expense_amounts[i]:
                try:
                    expenses.append({
                        'category': expense_categories[i].strip(),
                        'amount': float(expense_amounts[i]),
                        'date': expense_dates[i] if i < len(expense_dates) else '',
                        'description': expense_descriptions[i].strip() if i < len(expense_descriptions) else ''
                    })
                except (ValueError, IndexError):
                    continue
        
        # Parse income data (support multiple entries)
        incomes = []
        income_categories = form_data.getlist('income_category')
        income_amounts = form_data.getlist('income_amount')
        income_dates = form_data.getlist('income_date')
        income_descriptions = form_data.getlist('income_description')
        
        # If single entry (current form structure)
        if not income_categories and form_data.get('income_category'):
            income_categories = [form_data.get('income_category')]
            income_amounts = [form_data.get('income_amount')]
            income_dates = [form_data.get('income_date')]
            income_descriptions = [form_data.get('income_description', '')]
        
        # Build income list
        for i in range(len(income_categories)):
            if income_categories[i] and income_amounts[i]:
                try:
                    incomes.append({
                        'category': income_categories[i].strip(),
                        'amount': float(income_amounts[i]),
                        'date': income_dates[i] if i < len(income_dates) else '',
                        'description': income_descriptions[i].strip() if i < len(income_descriptions) else ''
                    })
                except (ValueError, IndexError):
                    continue
        
        # Validate that we have at least one income or expense
        if not expenses and not incomes:
            return render_template('form.html', error='Please provide at least one income or expense entry.'), 400
        
        # Calculate financial metrics
        try:
            total_income = calculate_total_income(incomes)
            total_expense = calculate_total_expense(expenses)
            profit_or_loss = calculate_profit_or_loss(total_income, total_expense)
            cost_per_acre = calculate_cost_of_cultivation_per_acre(total_expense, total_acres)
        except ValueError as e:
            return render_template('form.html', error=f'Calculation error: {str(e)}'), 400
        
        # Generate chart
        chart_filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        chart_path = os.path.join('static', 'charts', chart_filename)
        
        try:
            generate_income_expense_chart(total_income, total_expense, chart_path)
        except Exception as e:
            # Continue without chart if generation fails
            chart_path = None
            print(f"Chart generation failed: {str(e)}")
        
        # Prepare data for PDF
        pdf_data = {
            'farmer_name': farmer_name,
            'crop_name': crop_name,
            'season': season,
            'total_acres': total_acres,
            'date_of_sowing': date_of_sowing,
            'date_of_harvest': date_of_harvest,
            'location': location,
            'total_income': total_income,
            'total_expense': total_expense,
            'total_production': total_income,  # Assuming production equals income
            'profit_or_loss': profit_or_loss,
            'cost_per_acre': cost_per_acre,
            'chart_path': chart_path,
            'expenses': expenses,
            'incomes': incomes
        }
        
        # Generate PDF
        pdf_filename = f"farm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join('reports', pdf_filename)
        
        try:
            # Optional: Add logo path if available
            logo_path = os.path.join('static', 'images', 'logo.png')
            if not os.path.exists(logo_path):
                logo_path = None
            
            generate_pdf_report(pdf_data, pdf_path, logo_path)
        except Exception as e:
            return render_template('form.html', error=f'PDF generation failed: {str(e)}'), 500
        
        # Return PDF as downloadable file
        try:
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"Farm_Finance_Report_{farmer_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mimetype='application/pdf'
            )
        except Exception as e:
            return render_template('form.html', error=f'Error sending file: {str(e)}'), 500
    
    except Exception as e:
        # Log the full error for debugging
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        return render_template('form.html', error=f'An unexpected error occurred: {str(e)}'), 500


if __name__ == '__main__':
    app.run(debug=True)



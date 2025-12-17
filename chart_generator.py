import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path


def generate_income_expense_chart(total_income, total_expense, output_path):
    """
    Generate a bar chart comparing total income vs total expense.
    
    Args:
        total_income: Total income amount
        total_expense: Total expense amount
        output_path: Path where the chart image will be saved
        
    Returns:
        str: Path to the saved chart image
    """
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Data for the bar chart
    categories = ['Income', 'Expense']
    amounts = [total_income, total_expense]
    colors = ['#2ecc71', '#e74c3c']  # Green for income, red for expense
    
    # Create bar chart
    bars = ax.bar(categories, amounts, color=colors, width=0.6)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:,.2f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Set labels and title
    ax.set_ylabel('Amount (₹)', fontsize=12, fontweight='bold')
    ax.set_title('Income vs Expense Comparison', fontsize=14, fontweight='bold', pad=20)
    
    # Format y-axis to show currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    return str(output_path)
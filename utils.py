#utility.py


def calculate_total_income(incomes):
    """
    Calculate the total income from a list of income dictionaries.
    
    Args:
        incomes: List of dictionaries, each containing an "amount" key
        
    Returns:
        float: Total income amount
    """
    return sum(income.get("amount", 0) for income in incomes)


def calculate_total_expense(expenses):
    """
    Calculate the total expense from a list of expense dictionaries.
    
    Args:
        expenses: List of dictionaries, each containing an "amount" key
        
    Returns:
        float: Total expense amount
    """
    return sum(expense.get("amount", 0) for expense in expenses)


def calculate_profit_or_loss(total_income, total_expense):
    """
    Calculate profit (positive) or loss (negative) from income and expense.
    
    Args:
        total_income: Total income amount
        total_expense: Total expense amount
        
    Returns:
        float: Profit (positive) or loss (negative) amount
    """
    return total_income - total_expense


def calculate_cost_of_cultivation_per_acre(total_expense, total_acres):
    """
    Calculate the cost of cultivation per acre.
    
    Args:
        total_expense: Total expense amount
        total_acres: Total acres (must be greater than 0)
        
    Returns:
        float: Cost of cultivation per acre
        
    Raises:
        ValueError: If total_acres is zero or negative
    """
    if total_acres <= 0:
        raise ValueError("Total acres must be greater than zero")
    return total_expense / total_acres
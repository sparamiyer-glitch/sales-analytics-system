# This module handles all data analysis and processing tasks for the sales system

from typing import List, Dict, Tuple
from collections import defaultdict

# Task 2.1: Sales Summary Calculator Functions

def calculate_total_revenue(transactions: List[Dict]) -> float:
    """
    Calculates total revenue from all transactions.
    
    Parameters:
        transactions (list): List of transaction dictionaries
    
    Returns:
        float: Total revenue sum
    
    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    
    # Initialize total revenue to zero
    total_revenue = 0.0
    
    # Loop through each transaction
    for transaction in transactions:
        # Multiply quantity by unit price for each transaction
        transaction_amount = transaction['Quantity'] * transaction['UnitPrice']
        
        # Add to running total
        total_revenue += transaction_amount
    
    # Return the calculated total
    return total_revenue


def region_wise_sales(transactions: List[Dict]) -> Dict:
    """
    Analyzes sales by region.
    
    Parameters:
        transactions (list): List of transaction dictionaries
    
    Returns:
        dict: Dictionary with region statistics
    
    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }
    
    Requirements:
        - Calculate total sales per region
        - Count transactions per region
        - Calculate percentage of total sales
        - Sort by total_sales in descending order
    """
    
    # Dictionary to store region-wise data
    region_data = defaultdict(lambda: {'total_sales': 0.0, 'transaction_count': 0})
    
    # Calculate total revenue first for percentage calculation
    total_revenue = calculate_total_revenue(transactions)
    
    # Process each transaction
    for transaction in transactions:
        # Get region name
        region = transaction['Region']
        
        # Calculate amount for this transaction
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        # Add amount to region total
        region_data[region]['total_sales'] += amount
        
        # Increment transaction count for this region
        region_data[region]['transaction_count'] += 1
    
    # Convert defaultdict to regular dict and add percentages
    result = {}
    for region, data in region_data.items():
        # Calculate percentage of total sales
        percentage = (data['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0
        
        # Create result entry with all fields
        result[region] = {
            'total_sales': data['total_sales'],
            'transaction_count': data['transaction_count'],
            'percentage': round(percentage, 2)
        }
    
    # Sort by total_sales in descending order
    sorted_result = dict(sorted(result.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    
    # Return the sorted dictionary
    return sorted_result


def top_selling_products(transactions: List[Dict], n: int = 5) -> List[Tuple]:
    """
    Finds top n products by total quantity sold.
    
    Parameters:
        transactions (list): List of transaction dictionaries
        n (int): Number of top products to return (default 5)
    
    Returns:
        list: List of tuples
    
    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]
    
    Requirements:
        - Aggregate by ProductName
        - Calculate total quantity sold
        - Calculate total revenue for each product
        - Sort by TotalQuantity descending
        - Return top n products
    """
    
    # Dictionary to store product data
    product_data = {}
    
    # Process each transaction
    for transaction in transactions:
        # Get product name
        product_name = transaction['ProductName']
        
        # Calculate revenue for this transaction
        revenue = transaction['Quantity'] * transaction['UnitPrice']
        
        # If product not in dictionary, create entry
        if product_name not in product_data:
            product_data[product_name] = {'quantity': 0, 'revenue': 0.0}
        
        # Add quantity to product total
        product_data[product_name]['quantity'] += transaction['Quantity']
        
        # Add revenue to product total
        product_data[product_name]['revenue'] += revenue
    
    # Convert to list of tuples for sorting
    product_list = [
        (name, data['quantity'], data['revenue'])
        for name, data in product_data.items()
    ]
    
    # Sort by quantity in descending order
    sorted_products = sorted(product_list, key=lambda x: x[1], reverse=True)
    
    # Return only top n products
    return sorted_products[:n]


def customer_analysis(transactions: List[Dict]) -> Dict:
    """
    Analyzes customer purchase patterns.
    
    Parameters:
        transactions (list): List of transaction dictionaries
    
    Returns:
        dict: Dictionary of customer statistics
    
    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }
    
    Requirements:
        - Calculate total amount spent per customer
        - Count number of purchases
        - Calculate average order value
        - List unique products bought
        - Sort by total_spent descending
    """
    
    # Dictionary to store customer data
    customer_data = {}
    
    # Process each transaction
    for transaction in transactions:
        # Get customer ID
        customer_id = transaction['CustomerID']
        
        # Get product name
        product_name = transaction['ProductName']
        
        # Calculate transaction amount
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        # If customer not in dictionary, create entry
        if customer_id not in customer_data:
            customer_data[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }
        
        # Add amount to customer total
        customer_data[customer_id]['total_spent'] += amount
        
        # Increment purchase count
        customer_data[customer_id]['purchase_count'] += 1
        
        # Add product to set of unique products
        customer_data[customer_id]['products'].add(product_name)
    
    # Build result dictionary with formatted data
    result = {}
    for customer_id, data in customer_data.items():
        # Calculate average order value
        avg_order = data['total_spent'] / data['purchase_count'] if data['purchase_count'] > 0 else 0
        
        # Convert set to sorted list
        products_list = sorted(list(data['products']))
        
        # Create result entry
        result[customer_id] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_order, 2),
            'products_bought': products_list
        }
    
    # Sort by total_spent in descending order
    sorted_result = dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    # Return the sorted dictionary
    return sorted_result


# Task 2.2: Date-based Analysis Functions

def daily_sales_trend(transactions: List[Dict]) -> Dict:
    """
    Analyzes sales trends by date.
    
    Parameters:
        transactions (list): List of transaction dictionaries
    
    Returns:
        dict: Dictionary sorted by date
    
    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }
    
    Requirements:
        - Group by date
        - Calculate daily revenue
        - Count daily transactions
        - Count unique customers per day
        - Sort chronologically
    """
    
    # Dictionary to store daily data
    daily_data = {}
    
    # Process each transaction
    for transaction in transactions:
        # Get transaction date
        date = transaction['Date']
        
        # Get customer ID
        customer_id = transaction['CustomerID']
        
        # Calculate transaction amount
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        # If date not in dictionary, create entry
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }
        
        # Add amount to daily total
        daily_data[date]['revenue'] += amount
        
        # Increment daily transaction count
        daily_data[date]['transaction_count'] += 1
        
        # Add customer to set of unique customers
        daily_data[date]['customers'].add(customer_id)
    
    # Build result dictionary with formatted data
    result = {}
    for date, data in daily_data.items():
        # Count unique customers
        unique_customers = len(data['customers'])
        
        # Create result entry
        result[date] = {
            'revenue': data['revenue'],
            'transaction_count': data['transaction_count'],
            'unique_customers': unique_customers
        }
    
    # Sort chronologically by date
    sorted_result = dict(sorted(result.items()))
    
    # Return the sorted dictionary
    return sorted_result


def find_peak_sales_day(transactions: List[Dict]) -> Tuple:
    """
    Identifies the date with highest revenue.
    
    Parameters:
        transactions (list): List of transaction dictionaries
    
    Returns:
        tuple: (date, revenue, transaction_count)
    
    Expected Output Format:
        ('2024-12-15', 185000.0, 12)
    """
    
    # Get daily sales trend first
    daily_trend = daily_sales_trend(transactions)
    
    # Initialize peak day variables
    peak_date = None
    peak_revenue = 0.0
    peak_count = 0
    
    # Find date with highest revenue
    for date, data in daily_trend.items():
        # Compare revenue to find maximum
        if data['revenue'] > peak_revenue:
            # Update peak day info
            peak_date = date
            peak_revenue = data['revenue']
            peak_count = data['transaction_count']
    
    # Return tuple with peak day information
    return (peak_date, peak_revenue, peak_count)


# Task 2.3: Product Performance Functions

def low_performing_products(transactions: List[Dict], threshold: int = 10) -> List[Tuple]:
    """
    Identifies products with low sales.
    
    Parameters:
        transactions (list): List of transaction dictionaries
        threshold (int): Minimum quantity threshold (default 10)
    
    Returns:
        list: List of tuples
    
    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]
    
    Requirements:
        - Find products with total quantity < threshold
        - Include total quantity and revenue
        - Sort by TotalQuantity ascending
    """
    
    # Dictionary to store product data
    product_data = {}
    
    # Process each transaction
    for transaction in transactions:
        # Get product name
        product_name = transaction['ProductName']
        
        # Calculate revenue for this transaction
        revenue = transaction['Quantity'] * transaction['UnitPrice']
        
        # If product not in dictionary, create entry
        if product_name not in product_data:
            product_data[product_name] = {'quantity': 0, 'revenue': 0.0}
        
        # Add quantity to product total
        product_data[product_name]['quantity'] += transaction['Quantity']
        
        # Add revenue to product total
        product_data[product_name]['revenue'] += revenue
    
    # Find products below threshold
    low_products = []
    for name, data in product_data.items():
        # Check if quantity is below threshold
        if data['quantity'] < threshold:
            # Add to low products list
            low_products.append((name, data['quantity'], data['revenue']))
    
    # Sort by quantity in ascending order
    sorted_low = sorted(low_products, key=lambda x: x[1])
    
    # Return sorted list of low performing products
    return sorted_low
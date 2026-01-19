# This module handles all file reading, parsing and validation tasks for sales data

import csv
from typing import List, Dict, Tuple

def read_sales_data(filename: str) -> List[str]:
    """
    Reads sales data from a file and handles different encoding issues.
    
    Parameters:
        filename (str): Path to the sales data file
    
    Returns:
        list: List of raw lines (strings) from the file
    
    Expected Output Format:
        ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    
    Requirements:
        - Use 'with' statement for file operations
        - Handle different encodings (try UTF-8, latin-1, cp1252)
        - Handle FileNotFoundError with appropriate error message
        - Skip the header row
        - Remove empty lines
    """
    
    # List of encodings to try in order
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    try:
        # Try each encoding until one works
        for encoding in encodings:
            try:
                # Open file using with statement for proper resource management
                with open(filename, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                
                # Skip the header row by starting from index 1
                raw_lines = []
                for i, line in enumerate(lines):
                    # Skip first line which is the header
                    if i == 0:
                        continue
                    
                    # Strip whitespace and skip empty lines completely
                    cleaned_line = line.strip()
                    if cleaned_line:
                        raw_lines.append(cleaned_line)
                
                # Return the cleaned lines if reading was successful
                return raw_lines
            
            # If encoding fails, try next encoding
            except UnicodeDecodeError:
                continue
        
        # Raise error if no encoding worked
        raise ValueError(f"Could not read file {filename} with any supported encoding")
    
    except FileNotFoundError:
        # Handle case where file does not exist
        print(f"Error: File '{filename}' not found. Please check the file path and try again.")
        return []


def parse_transactions(raw_lines: List[str]) -> List[Dict]:
    """
    Parses raw lines into clean list of transaction dictionaries.
    
    Parameters:
        raw_lines (list): List of raw line strings from file
    
    Returns:
        list: List of dictionaries with cleaned transaction data
    
    Expected Output Format:
        [
            {
                'TransactionID': 'T001',
                'Date': '2024-12-01',
                'ProductID': 'P101',
                'ProductName': 'Laptop',
                'Quantity': 2,
                'UnitPrice': 45000.0,
                'CustomerID': 'C001',
                'Region': 'North'
            },
            ...
        ]
    
    Requirements:
        - Split by pipe delimiter '|'
        - Handle commas within ProductName (remove commas)
        - Remove commas from numeric fields and convert to proper types
        - Convert Quantity to int
        - Convert UnitPrice to float
        - Skip rows with incorrect number of fields
    """
    
    # List to store parsed transactions
    transactions = []
    
    # Field names for the transaction dictionary
    field_names = ['TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    # Process each raw line
    for line in raw_lines:
        try:
            # Split the line using pipe delimiter
            fields = line.split('|')
            
            # Skip rows that don't have exactly 8 fields
            if len(fields) != 8:
                continue
            
            # Strip whitespace from all fields
            fields = [field.strip() for field in fields]
            
            # Remove commas from ProductName field (index 3)
            fields[3] = fields[3].replace(',', '')
            
            # Remove commas from Quantity field (index 4) and convert to integer
            fields[4] = int(fields[4].replace(',', ''))
            
            # Remove commas from UnitPrice field (index 5) and convert to float
            fields[5] = float(fields[5].replace(',', ''))
            
            # Create dictionary from field names and values
            transaction = dict(zip(field_names, fields))
            
            # Add the transaction to our list
            transactions.append(transaction)
        
        # Skip any line that causes an error during parsing
        except (ValueError, IndexError):
            continue
    
    # Return all successfully parsed transactions
    return transactions


def validate_and_filter(
    transactions: List[Dict],
    region: str = None,
    min_amount: float = None,
    max_amount: float = None
) -> Tuple[List[Dict], int, Dict]:
    """
    Validates transactions and applies optional filters.
    
    Parameters:
        transactions (list): List of transaction dictionaries
        region (str): Filter by specific region (optional)
        min_amount (float): Minimum transaction amount (optional)
        max_amount (float): Maximum transaction amount (optional)
    
    Returns:
        tuple: (valid_transactions, invalid_count, filter_summary)
    
    Expected Output Format:
        (
            [list of valid filtered transactions],
            5,  # count of invalid transactions
            {
                'total_input': 100,
                'invalid': 5,
                'filtered_by_region': 20,
                'filtered_by_amount': 10,
                'final_count': 65
            }
        )
    
    Validation Rules:
        - Quantity must be > 0
        - UnitPrice must be > 0
        - All required fields must be present
        - TransactionID must start with 'T'
        - ProductID must start with 'P'
        - CustomerID must start with 'C'
    
    Filter Display:
        - Print available regions to user before filtering
        - Print transaction amount range (min/max) to user
        - Show count of records after each filter applied
    """
    
    # Initialize tracking variables
    valid_transactions = []
    invalid_count = 0
    
    # Count transactions at each filtering stage
    total_input = len(transactions)
    
    # First pass: validate all transactions
    for transaction in transactions:
        
        # Check if Quantity is greater than 0
        if transaction['Quantity'] <= 0:
            invalid_count += 1
            continue
        
        # Check if UnitPrice is greater than 0
        if transaction['UnitPrice'] <= 0:
            invalid_count += 1
            continue
        
        # Check if TransactionID starts with 'T'
        if not transaction['TransactionID'].startswith('T'):
            invalid_count += 1
            continue
        
        # Check if ProductID starts with 'P'
        if not transaction['ProductID'].startswith('P'):
            invalid_count += 1
            continue
        
        # Check if CustomerID starts with 'C'
        if not transaction['CustomerID'].startswith('C'):
            invalid_count += 1
            continue
        
        # Check if CustomerID and Region exist and are not empty
        if not transaction.get('CustomerID') or not transaction.get('Region'):
            invalid_count += 1
            continue
        
        # If all validations pass, add to valid list
        valid_transactions.append(transaction)
    
    # Calculate and display available regions
    regions_set = set(t['Region'] for t in valid_transactions)
    regions_list = sorted(list(regions_set))
    print(f"\nAvailable Regions: {', '.join(regions_list)}")
    
    # Calculate and display transaction amount range
    if valid_transactions:
        amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_transactions]
        min_transaction = min(amounts)
        max_transaction = max(amounts)
        print(f"Transaction Amount Range: {min_transaction} - {max_transaction}")
    
    # Initialize filter counts
    after_region_filter = len(valid_transactions)
    after_amount_filter = len(valid_transactions)
    
    # Apply region filter if specified
    if region:
        valid_transactions = [t for t in valid_transactions if t['Region'] == region]
        after_region_filter = len(valid_transactions)
        print(f"After region filter: {after_region_filter} records")
    
    # Apply amount range filters if specified
    if min_amount or max_amount:
        filtered_transactions = []
        for t in valid_transactions:
            # Calculate transaction amount
            transaction_amount = t['Quantity'] * t['UnitPrice']
            
            # Check if within min and max bounds
            if min_amount and transaction_amount < min_amount:
                continue
            if max_amount and transaction_amount > max_amount:
                continue
            
            # Add to filtered list if it passes amount checks
            filtered_transactions.append(t)
        
        valid_transactions = filtered_transactions
        after_amount_filter = len(valid_transactions)
        print(f"After amount filter: {after_amount_filter} records")
    
    # Create summary dictionary with all filter information
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': after_region_filter,
        'filtered_by_amount': after_amount_filter,
        'final_count': len(valid_transactions)
    }
    
    # Return tuple with valid transactions, invalid count, and summary
    return valid_transactions, invalid_count, filter_summary
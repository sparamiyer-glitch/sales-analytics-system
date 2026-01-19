# This module handles all API integration and data enrichment tasks for the sales system

import requests
from typing import List, Dict

# Task 3.1: Fetch Product Details Functions

def fetch_all_products() -> List[Dict]:
    """
    Fetches all products from DummyJSON API.
    
    Parameters:
        None
    
    Returns:
        list: List of product dictionaries
    
    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    
    Requirements:
        - Fetch all available products (use limit=100)
        - Handle connection errors with try-except
        - Return empty list if API fails
        - Print status message (success/failure)
    """
    
    # API endpoint URL with limit parameter
    api_url = 'https://dummyjson.com/products?limit=100'
    
    # List to store products
    products = []
    
    try:
        # Make HTTP GET request to the API
        response = requests.get(api_url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Extract products list from response
            if 'products' in data:
                # Get the products array
                api_products = data['products']
                
                # Loop through each product
                for product in api_products:
                    # Create product entry with required fields
                    product_entry = {
                        'id': product.get('id'),
                        'title': product.get('title'),
                        'category': product.get('category'),
                        'brand': product.get('brand'),
                        'price': product.get('price'),
                        'rating': product.get('rating')
                    }
                    
                    # Add to products list
                    products.append(product_entry)
                
                # Print success message with count
                print(f"Successfully fetched {len(products)} products from API")
            
            else:
                # Print error if products key not found
                print("Error: Products key not found in API response")
        
        else:
            # Print error if HTTP status is not 200
            print(f"Error: API returned status code {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        # Handle connection error
        print("Error: Failed to connect to API. Check your internet connection.")
    
    except requests.exceptions.Timeout:
        # Handle timeout error
        print("Error: API request timed out. Server took too long to respond.")
    
    except requests.exceptions.RequestException as e:
        # Handle any other request error
        print(f"Error: API request failed with error: {str(e)}")
    
    except Exception as e:
        # Handle any unexpected error
        print(f"Error: Unexpected error while fetching products: {str(e)}")
    
    # Return products list (empty if any error occurred)
    return products


def create_product_mapping(api_products: List[Dict]) -> Dict:
    """
    Creates a mapping of product IDs to product info.
    
    Parameters:
        api_products (list): List from fetch_all_products()
    
    Returns:
        dict: Dictionary mapping product IDs to info
    
    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    
    # Dictionary to store product mapping
    product_mapping = {}
    
    # Loop through each product from API
    for product in api_products:
        # Extract product ID
        product_id = product['id']
        
        # Create product info dictionary with key fields
        product_info = {
            'title': product['title'],
            'category': product['category'],
            'brand': product['brand'],
            'rating': product['rating']
        }
        
        # Map product ID to its information
        product_mapping[product_id] = product_info
    
    # Return the complete mapping
    return product_mapping


# Task 3.2: Enrich Sales Data Functions

def enrich_sales_data(transactions: List[Dict], product_mapping: Dict) -> List[Dict]:
    """
    Enriches transaction data with API product information.
    
    Parameters:
        transactions (list): List of transaction dictionaries
        product_mapping (dict): Dictionary from create_product_mapping()
    
    Returns:
        list: List of enriched transaction dictionaries
    
    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True
    }
    
    Enrichment Logic:
        - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
        - If ID exists in product_mapping, add API fields
        - If ID doesn't exist, set API_Match to False and other fields to None
        - Handle all errors gracefully
    """
    
    # List to store enriched transactions
    enriched_transactions = []
    
    # Loop through each transaction
    for transaction in transactions:
        # Create copy of transaction to preserve original
        enriched = transaction.copy()
        
        # Extract ProductID field
        product_id_str = transaction['ProductID']
        
        try:
            # Extract numeric part from ProductID (remove 'P' prefix)
            numeric_id = int(product_id_str[1:])
            
            # Check if numeric ID exists in product mapping
            if numeric_id in product_mapping:
                # Get product info from mapping
                product_info = product_mapping[numeric_id]
                
                # Add category from API
                enriched['API_Category'] = product_info['category']
                
                # Add brand from API
                enriched['API_Brand'] = product_info['brand']
                
                # Add rating from API
                enriched['API_Rating'] = product_info['rating']
                
                # Mark as successfully matched
                enriched['API_Match'] = True
            
            else:
                # Product ID not found in API data
                enriched['API_Category'] = None
                enriched['API_Brand'] = None
                enriched['API_Rating'] = None
                enriched['API_Match'] = False
        
        except (ValueError, IndexError):
            # Error extracting numeric ID from ProductID
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False
        
        except Exception as e:
            # Any other unexpected error during enrichment
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False
        
        # Add enriched transaction to list
        enriched_transactions.append(enriched)
    
    # Return all enriched transactions
    return enriched_transactions


def save_enriched_data(enriched_transactions: List[Dict], filename: str = 'data/enriched_sales_data.txt') -> None:
    """
    Saves enriched transactions back to file.
    
    Parameters:
        enriched_transactions (list): List of enriched transaction dictionaries
        filename (str): Output file path (default: 'data/enriched_sales_data.txt')
    
    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...
    
    Requirements:
        - Create output file with all original + new fields
        - Use pipe delimiter
        - Handle None values appropriately
    """
    
    try:
        # Open file for writing
        with open(filename, 'w') as file:
            
            # Define field names for header
            field_names = [
                'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity',
                'UnitPrice', 'CustomerID', 'Region', 'API_Category', 'API_Brand',
                'API_Rating', 'API_Match'
            ]
            
            # Write header row
            header = '|'.join(field_names)
            file.write(header + '\n')
            
            # Write each transaction as a row
            for transaction in enriched_transactions:
                # Build row values in order
                row_values = []
                for field in field_names:
                    # Get value from transaction
                    value = transaction.get(field)
                    
                    # Convert None to empty string
                    if value is None:
                        value = ''
                    
                    # Convert to string
                    value_str = str(value)
                    
                    # Add to row
                    row_values.append(value_str)
                
                # Join values with pipe delimiter
                row = '|'.join(row_values)
                
                # Write row to file
                file.write(row + '\n')
        
        # Print success message
        print(f"Successfully saved enriched data to {filename}")
    
    except IOError as e:
        # Handle file write error
        print(f"Error: Failed to write to file {filename}: {str(e)}")
    
    except Exception as e:
        # Handle any other error
        print(f"Error: Unexpected error while saving enriched data: {str(e)}")
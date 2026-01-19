# Main application file that orchestrates the entire sales analytics workflow
# This script brings together all modules and runs the complete analysis system

import os
import sys
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from utils.report_handler import generate_sales_report


def main():
    """
    Main execution function that orchestrates the complete sales analytics workflow.
    
    Workflow:
        1. Print welcome message
        2. Read sales data file (handle encoding)
        3. Parse and clean transactions
        4. Display filter options to user
        5. Ask if user wants to filter (y/n)
        6. If yes, ask for filter criteria and apply
        7. Validate transactions
        8. Display validation summary
        9. Perform all data analyses
        10. Fetch products from API
        11. Enrich sales data with API info
        12. Save enriched data to file
        13. Generate comprehensive report
        14. Print success message with file locations
    
    Error Handling:
        - Wrap entire process in try-except
        - Display user-friendly error messages
        - Don't let program crash on errors
    """
    
    try:
        # Print welcome banner for the application
        print("\n" + "=" * 60)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 60 + "\n")
        
        
        # STEP 1: Read sales data file with encoding handling
        print("[1/13] Reading sales data file...")
        
        # Define the data file path
        data_file = 'data/sales_data.txt'
        
        # Check if file exists before reading
        if not os.path.exists(data_file):
            # Inform user if file path does not exist
            print(f"Error: Data file '{data_file}' not found.")
            print("Please ensure sales_data.txt is in the data/ folder.")
            return
        
        # Read raw lines from the file
        raw_lines = read_sales_data(data_file)
        
        # Check if any data was read successfully
        if not raw_lines:
            print("Error: No data could be read from the file.")
            return
        
        # Print success message with record count
        print(f"✓ Successfully read {len(raw_lines)} transaction lines\n")
        
        
        # STEP 2: Parse and clean the transaction data
        print("[2/13] Parsing and cleaning transaction data...")
        
        # Parse raw lines into structured transaction dictionaries
        transactions = parse_transactions(raw_lines)
        
        # Check if transactions were parsed successfully
        if not transactions:
            print("Error: No valid transactions could be parsed.")
            return
        
        # Print success message with parsed count
        print(f"✓ Successfully parsed {len(transactions)} records\n")
        
        
        # STEP 3: Display available filter options to user
        print("[3/13] Filter Options Available:\n")
        
        # Extract unique regions from transactions
        regions = set(t['Region'] for t in transactions)
        regions_list = sorted(list(regions))
        
        # Display available regions
        print(f"Regions: {', '.join(regions_list)}")
        
        # Calculate transaction amount range
        amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
        min_amount = min(amounts)
        max_amount = max(amounts)
        
        # Display amount range
        print(f"Amount Range: Rs. {min_amount:,.2f} - Rs. {max_amount:,.2f}\n")
        
        
        # STEP 4: Ask user if they want to apply filters
        filter_choice = input("Do you want to filter the data? (y/n): ").strip().lower()
        
        # Initialize variables for filtered data
        filtered_transactions = transactions
        filter_summary = None
        
        # Process user's filtering choice
        if filter_choice == 'y':
            # Ask which region to filter by
            print("\nEnter region name (or press Enter to skip region filter):")
            region_input = input("Region: ").strip()
            
            # Set region to None if user skipped
            region_to_filter = region_input if region_input else None
            
            # Ask for minimum amount filter
            print("\nEnter minimum transaction amount (or press Enter to skip):")
            min_input = input("Minimum Amount: ").strip()
            
            # Convert to float or None
            try:
                min_amount_filter = float(min_input) if min_input else None
            except ValueError:
                print("Invalid amount, skipping minimum filter.")
                min_amount_filter = None
            
            # Ask for maximum amount filter
            print("\nEnter maximum transaction amount (or press Enter to skip):")
            max_input = input("Maximum Amount: ").strip()
            
            # Convert to float or None
            try:
                max_amount_filter = float(max_input) if max_input else None
            except ValueError:
                print("Invalid amount, skipping maximum filter.")
                max_amount_filter = None
            
            # Apply filters to transactions
            filtered_transactions, invalid_count, filter_summary = validate_and_filter(
                transactions,
                region=region_to_filter,
                min_amount=min_amount_filter,
                max_amount=max_amount_filter
            )
            
            # Print filter result message
            print(f"\n✓ Filtering complete: {len(filtered_transactions)} records remain\n")
        
        else:
            # User chose not to filter, validate without filters
            filtered_transactions, invalid_count, filter_summary = validate_and_filter(transactions)
            print("✓ No filters applied\n")
        
        
        # STEP 5: Validate transactions and display summary
        print("[4/13] Validating transactions...\n")
        
        # Display validation results
        print(f"Total records input: {filter_summary['total_input']}")
        print(f"Invalid records removed: {filter_summary['invalid']}")
        print(f"Valid records after cleaning: {len(filtered_transactions)}\n")
        
        
        # STEP 6: Perform all data analyses
        print("[5/13] Analyzing sales data...")
        
        # Calculate total revenue
        total_revenue = calculate_total_revenue(filtered_transactions)
        
        # Get region-wise sales analysis
        region_data = region_wise_sales(filtered_transactions)
        
        # Get top selling products
        top_products = top_selling_products(filtered_transactions, n=5)
        
        # Get customer analysis
        customer_data = customer_analysis(filtered_transactions)
        
        # Get daily sales trend
        daily_data = daily_sales_trend(filtered_transactions)
        
        # Find peak sales day
        peak_day = find_peak_sales_day(filtered_transactions)
        
        # Get low performing products
        low_products = low_performing_products(filtered_transactions, threshold=10)
        
        # Print analysis completion message
        print("✓ Analysis complete\n")
        
        
        # STEP 7: Fetch products from external API
        print("[6/13] Fetching product data from API...")
        
        # Fetch all products from DummyJSON API
        api_products = fetch_all_products()
        
        # Print completion status
        print()
        
        
        # STEP 8: Create product mapping from API data
        print("[7/13] Creating product mapping from API data...")
        
        # Create mapping of product IDs to product information
        product_mapping = create_product_mapping(api_products)
        
        # Print success message
        print(f"✓ Created mapping for {len(product_mapping)} products from API\n")
        
        
        # STEP 9: Enrich sales data with API information
        print("[8/13] Enriching sales data with API information...")
        
        # Enrich transactions with API product details
        enriched_transactions = enrich_sales_data(filtered_transactions, product_mapping)
        
        # Count successful enrichments
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match') == True)
        enrichment_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
        
        # Print enrichment summary
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({enrichment_rate:.1f}%)\n")
        
        
        # STEP 10: Save enriched data to file
        print("[9/13] Saving enriched data to file...")
        
        # Define output path for enriched data
        enriched_output_file = 'data/enriched_sales_data.txt'
        
        # Ensure output directory exists
        output_dir = os.path.dirname(enriched_output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save enriched transactions to file
        save_enriched_data(enriched_transactions, enriched_output_file)
        
        print()
        
        
        # STEP 11: Generate comprehensive report
        print("[10/13] Generating comprehensive sales report...")
        
        # Define output path for report
        report_output_file = 'output/sales_report.txt'
        
        # Ensure output directory exists
        report_dir = os.path.dirname(report_output_file)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        
        # Generate the full sales report
        generate_sales_report(filtered_transactions, enriched_transactions, report_output_file)
        
        print()
        
        
        # STEP 12: Print completion message with file locations
        print("[11/13] Process Complete!\n")
        print("=" * 60)
        print("ANALYSIS COMPLETE - FILES GENERATED\n")
        
        # Display output file locations
        print("Output Files Created:")
        print(f"  1. Enriched Data: {enriched_output_file}")
        print(f"  2. Report: {report_output_file}\n")
        
        # Display summary statistics
        print("Summary Statistics:")
        print(f"  - Total Transactions Analyzed: {len(filtered_transactions)}")
        print(f"  - Total Revenue: Rs. {total_revenue:,.2f}")
        print(f"  - Regions Analyzed: {len(region_data)}")
        print(f"  - Unique Customers: {len(customer_data)}")
        print(f"  - Date Range: {min(t['Date'] for t in filtered_transactions)} to {max(t['Date'] for t in filtered_transactions)}\n")
        
        print("=" * 60)
        print("Thank you for using Sales Analytics System!")
        print("=" * 60 + "\n")
    
    except FileNotFoundError as e:
        # Handle file not found errors
        print(f"\nError: Required file not found - {str(e)}")
        print("Please check that all required files are in place.")
    
    except KeyError as e:
        # Handle missing dictionary keys
        print(f"\nError: Missing required data field - {str(e)}")
        print("Please check the data file format.")
    
    except ValueError as e:
        # Handle value conversion errors
        print(f"\nError: Invalid data value - {str(e)}")
        print("Please check the data file for formatting issues.")
    
    except Exception as e:
        # Handle any other unexpected errors
        print(f"\nError: An unexpected error occurred - {str(e)}")
        print("Please check the error message and try again.")
        print("If the problem persists, please contact support.")


# Standard Python entry point for script execution
if __name__ == "__main__":
    # Call main function to start the application
    main()
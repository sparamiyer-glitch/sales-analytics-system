# This module handles all report generation and formatting tasks for the sales system

from typing import List, Dict, Tuple
from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products
)


def generate_sales_report(
    transactions: List[Dict],
    enriched_transactions: List[Dict],
    output_file: str = 'output/sales_report.txt'
) -> None:
    """
    Generates a comprehensive formatted text report with 8 sections.
    
    Parameters:
        transactions (list): List of cleaned transaction dictionaries
        enriched_transactions (list): List of enriched transaction dictionaries with API data
        output_file (str): Output file path (default: 'output/sales_report.txt')
    
    Report Must Include (in this order):
        1. HEADER - Report title, generation date/time, records processed
        2. OVERALL SUMMARY - Total revenue, transactions, average order value, date range
        3. REGION-WISE PERFORMANCE - Table with sales, percentage, transaction count
        4. TOP 5 PRODUCTS - Table with rank, product name, quantity, revenue
        5. TOP 5 CUSTOMERS - Table with rank, customer ID, total spent, order count
        6. DAILY SALES TREND - Table with date, revenue, transactions, unique customers
        7. PRODUCT PERFORMANCE ANALYSIS - Best day, low performers, average by region
        8. API ENRICHMENT SUMMARY - Total enriched, success rate, unmatched products
    """
    
    try:
        # Open file for writing report
        with open(output_file, 'w') as file:
            
            # SECTION 1: HEADER
            # Write top border line for visual appeal
            file.write("=" * 60 + "\n")
            
            # Write report title
            file.write("SALES ANALYTICS REPORT\n")
            
            # Get current date and time for generation timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Generated: {current_time}\n")
            
            # Write total records count
            file.write(f"Records Processed: {len(transactions)}\n")
            
            # Write bottom border line
            file.write("=" * 60 + "\n\n")
            
            
            # SECTION 2: OVERALL SUMMARY
            # Write section header
            file.write("OVERALL SUMMARY\n")
            file.write("-" * 60 + "\n")
            
            # Calculate total revenue using function
            total_revenue = calculate_total_revenue(transactions)
            
            # Format revenue with commas and currency symbol
            revenue_formatted = f"Rs. {total_revenue:,.2f}"
            file.write(f"Total Revenue: {revenue_formatted}\n")
            
            # Write total transaction count
            total_transactions = len(transactions)
            file.write(f"Total Transactions: {total_transactions}\n")
            
            # Calculate average order value
            avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
            avg_formatted = f"Rs. {avg_order_value:,.2f}"
            file.write(f"Average Order Value: {avg_formatted}\n")
            
            # Extract date range from transactions
            if transactions:
                # Get all dates and sort them
                dates = sorted([t['Date'] for t in transactions])
                # Get earliest and latest dates
                start_date = dates[0]
                end_date = dates[-1]
                file.write(f"Date Range: {start_date} to {end_date}\n")
            
            file.write("\n")
            
            
            # SECTION 3: REGION-WISE PERFORMANCE
            # Write section header
            file.write("REGION-WISE PERFORMANCE\n")
            file.write("-" * 60 + "\n")
            
            # Write table header
            file.write(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions':<15}\n")
            file.write("-" * 60 + "\n")
            
            # Get region-wise data using function
            region_data = region_wise_sales(transactions)
            
            # Write each region's data
            for region, data in region_data.items():
                # Format region name
                region_name = region[:14]
                
                # Format sales with commas
                sales_formatted = f"Rs. {data['total_sales']:,.2f}"
                
                # Format percentage
                percentage = f"{data['percentage']:.2f}%"
                
                # Format transaction count
                trans_count = str(data['transaction_count'])
                
                # Write row with proper alignment
                file.write(f"{region_name:<15} {sales_formatted:<20} {percentage:<15} {trans_count:<15}\n")
            
            file.write("\n")
            
            
            # SECTION 4: TOP 5 PRODUCTS
            # Write section header
            file.write("TOP 5 PRODUCTS BY QUANTITY SOLD\n")
            file.write("-" * 60 + "\n")
            
            # Write table header
            file.write(f"{'Rank':<8} {'Product Name':<25} {'Quantity':<12} {'Revenue':<15}\n")
            file.write("-" * 60 + "\n")
            
            # Get top 5 products using function
            top_products = top_selling_products(transactions, n=5)
            
            # Write each product with rank
            for rank, (product_name, quantity, revenue) in enumerate(top_products, 1):
                # Truncate product name if too long
                product_display = product_name[:24]
                
                # Format revenue with commas
                revenue_formatted = f"Rs. {revenue:,.2f}"
                
                # Write row with rank and data
                file.write(f"{rank:<8} {product_display:<25} {quantity:<12} {revenue_formatted:<15}\n")
            
            file.write("\n")
            
            
            # SECTION 5: TOP 5 CUSTOMERS
            # Write section header
            file.write("TOP 5 CUSTOMERS BY SPENDING\n")
            file.write("-" * 60 + "\n")
            
            # Write table header
            file.write(f"{'Rank':<8} {'Customer ID':<15} {'Total Spent':<20} {'Order Count':<12}\n")
            file.write("-" * 60 + "\n")
            
            # Get customer data using function
            customer_data = customer_analysis(transactions)
            
            # Get top 5 customers sorted by spending
            top_customers = sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
            
            # Write each customer with rank
            for rank, (customer_id, data) in enumerate(top_customers, 1):
                # Format total spent with commas
                spent_formatted = f"Rs. {data['total_spent']:,.2f}"
                
                # Get order count
                order_count = data['purchase_count']
                
                # Write row with rank and data
                file.write(f"{rank:<8} {customer_id:<15} {spent_formatted:<20} {order_count:<12}\n")
            
            file.write("\n")
            
            
            # SECTION 6: DAILY SALES TREND
            # Write section header
            file.write("DAILY SALES TREND\n")
            file.write("-" * 60 + "\n")
            
            # Write table header
            file.write(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<10}\n")
            file.write("-" * 60 + "\n")
            
            # Get daily trend data using function
            daily_data = daily_sales_trend(transactions)
            
            # Write each day's data
            for date, data in daily_data.items():
                # Format revenue with commas
                revenue_formatted = f"Rs. {data['revenue']:,.2f}"
                
                # Get transaction count
                trans_count = str(data['transaction_count'])
                
                # Get unique customer count
                unique_cust = str(data['unique_customers'])
                
                # Write row with date and data
                file.write(f"{date:<15} {revenue_formatted:<20} {trans_count:<15} {unique_cust:<10}\n")
            
            file.write("\n")
            
            
            # SECTION 7: PRODUCT PERFORMANCE ANALYSIS
            # Write section header
            file.write("PRODUCT PERFORMANCE ANALYSIS\n")
            file.write("-" * 60 + "\n")
            
            # Find and display peak sales day
            peak_day = find_peak_sales_day(transactions)
            peak_date = peak_day[0]
            peak_revenue = peak_day[1]
            peak_count = peak_day[2]
            
            # Write peak day information
            file.write(f"Best Selling Day: {peak_date} with Rs. {peak_revenue:,.2f} revenue ({peak_count} transactions)\n")
            
            # Find and display low performing products
            low_products = low_performing_products(transactions, threshold=10)
            
            # Write low performing products section
            if low_products:
                file.write(f"\nLow Performing Products (< 10 units sold):\n")
                
                # Write table header for low performers
                file.write(f"{'Product Name':<25} {'Quantity':<12} {'Revenue':<15}\n")
                
                # Write each low product
                for product_name, quantity, revenue in low_products:
                    # Truncate product name if needed
                    product_display = product_name[:24]
                    
                    # Format revenue
                    revenue_formatted = f"Rs. {revenue:,.2f}"
                    
                    # Write product row
                    file.write(f"{product_display:<25} {quantity:<12} {revenue_formatted:<15}\n")
            else:
                # Message if no low performers
                file.write("Low Performing Products: None - All products performing well!\n")
            
            # Calculate average transaction value per region
            file.write(f"\nAverage Transaction Value Per Region:\n")
            
            # Loop through regions and calculate average
            for region, data in region_data.items():
                # Calculate average by dividing total sales by transaction count
                if data['transaction_count'] > 0:
                    avg_trans = data['total_sales'] / data['transaction_count']
                    avg_formatted = f"Rs. {avg_trans:,.2f}"
                else:
                    avg_formatted = "Rs. 0.00"
                
                # Write region average
                file.write(f"  {region}: {avg_formatted}\n")
            
            file.write("\n")
            
            
            # SECTION 8: API ENRICHMENT SUMMARY
            # Write section header
            file.write("API ENRICHMENT SUMMARY\n")
            file.write("-" * 60 + "\n")
            
            # Count successfully enriched products
            enriched_count = 0
            unmatched_products = set()
            
            # Loop through enriched transactions
            for enriched in enriched_transactions:
                # Check if API match was successful
                if enriched.get('API_Match') == True:
                    # Increment count for successful matches
                    enriched_count += 1
                else:
                    # Add to unmatched set if not matched
                    product_id = enriched.get('ProductID', 'Unknown')
                    unmatched_products.add(product_id)
            
            # Calculate success rate percentage
            total_enriched = len(enriched_transactions)
            success_rate = (enriched_count / total_enriched * 100) if total_enriched > 0 else 0
            
            # Write enrichment statistics
            file.write(f"Total Products Enriched: {enriched_count} / {total_enriched}\n")
            file.write(f"Success Rate: {success_rate:.2f}%\n")
            
            # Write unmatched products if any
            if unmatched_products:
                file.write(f"\nProducts Not Matched with API Data:\n")
                
                # Sort and display each unmatched product
                for product_id in sorted(unmatched_products):
                    file.write(f"  - {product_id}\n")
            else:
                # Message if all products were matched
                file.write("Products Not Matched: None - All products successfully enriched!\n")
            
            # Write closing border
            file.write("\n" + "=" * 60 + "\n")
            file.write("END OF REPORT\n")
            file.write("=" * 60 + "\n")
        
        # Print success message with file location
        print(f"Report successfully generated and saved to {output_file}")
    
    except IOError as e:
        # Handle file write error
        print(f"Error: Failed to write report to {output_file}: {str(e)}")
    
    except Exception as e:
        # Handle any unexpected error during report generation
        print(f"Error: Unexpected error while generating report: {str(e)}")
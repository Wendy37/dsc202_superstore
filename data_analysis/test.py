import pandas as pd

# Load the orders and returns data (adjust file paths as necessary)
orders_df = pd.read_csv("Orders_Formatted.csv")
returns_df = pd.read_csv("Returns.csv")

# Assume that:
# - orders_df contains columns: "Order ID", "Region", and "Category" (representing product category)
# - returns_df contains the column "Order ID" for returned orders

# Create a flag in orders_df indicating if an order was returned
orders_df['Returned'] = orders_df['Order ID'].isin(returns_df['Order ID'])

# Group the orders by Region and Product Category to calculate the metrics
agg_df = orders_df.groupby(['Region', 'Category']).agg(
    TotalOrders=('Order ID', 'nunique'),
    ReturnedOrders=('Returned', 'sum')
).reset_index()

# Calculate the return rate as a percentage
agg_df['ReturnRate'] = (agg_df['ReturnedOrders'] / agg_df['TotalOrders']) * 100

# Sort the result by Region and then by ReturnRate in descending order
agg_df = agg_df.sort_values(by=['Region'], ascending=[True])

# Display the result as a table
print(agg_df)

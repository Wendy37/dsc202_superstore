import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
orders_path = "./Orders.csv"
returns_path = "./Returns.csv"
people_path = "./People.csv"

orders_df = pd.read_csv(orders_path)
returns_df = pd.read_csv(returns_path)
people_df = pd.read_csv(people_path)

# Display the shape of each table
print("Orders Table Shape:", orders_df.shape)
print("Returns Table Shape:", returns_df.shape)
print("People Table Shape:", people_df.shape)

# Check for missing data
print("\nMissing Data Summary:")
print(orders_df.isnull().sum())
print(returns_df.isnull().sum())
print(people_df.isnull().sum())



#-----------------
# Define the list of product names (as provided)
product_names = [
    "Easy-staple paper",
    "Staple envelope",
    "Staples",
    "Staple envelope",
    "Easy-staple paper",
    "Staples",
    "Easy-staple paper",
    "Staples",
    "Staple envelope",
    "Staples",
    "Staple envelope",
    "Imation 16GB Mini TravelDrive USB 2.0 Flash Drive"
]

# Optional: remove duplicates from the list if you only need to search each product once
unique_product_names = list(set(product_names))

# Load your DataFrame (adjust the file name or path accordingly)
# For example, if your data is stored in a CSV file called "Products.csv":
df = pd.read_csv("Orders_Formatted.csv")

# Filter the DataFrame to include only rows with a product name in your list
filtered_df = df[df["Product Name"].isin(unique_product_names)]

# Optional: If you only want to see the Product Name, Category, and Sub-Category columns, and remove duplicate rows:
result = filtered_df[["Product Name", "Category", "Sub-Category"]].drop_duplicates()

# Print the result
print(result)
# Convert Ship Date to DateTime format
# if 'Ship Date' in orders_df.columns:
#     orders_df['Ship Date'] = pd.to_datetime(orders_df['Ship Date'], errors='coerce')
    

# # Order Count by Region (Pie Chart)
# if 'Region' in orders_df.columns:
#     region_counts = orders_df['Region'].value_counts()
#     plt.figure(figsize=(8, 6))
#     region_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette("viridis", len(region_counts)))
#     plt.title("Order Count by Region")
#     plt.ylabel("")
#     plt.show()


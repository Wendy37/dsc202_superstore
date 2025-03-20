import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

orders_path = "./dataset/Orders.csv"
returns_path = "./dataset/Returns.csv"
people_path = "./dataset/People.csv"

orders_df = pd.read_csv(orders_path)
returns_df = pd.read_csv(returns_path)
people_df = pd.read_csv(people_path)
print("Orders Table Shape:", orders_df.shape)
print("Returns Table Shape:", returns_df.shape)
print("People Table Shape:", people_df.shape)
print("\nMissing Data Summary:")
print(orders_df.isnull().sum())
print(returns_df.isnull().sum())
print(people_df.isnull().sum())


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
unique_product_names = list(set(product_names))
df = pd.read_csv("Orders_Formatted.csv")
filtered_df = df[df["Product Name"].isin(unique_product_names)]
result = filtered_df[["Product Name", "Category", "Sub-Category"]].drop_duplicates()

print(result)
if 'Ship Date' in orders_df.columns:
    orders_df['Ship Date'] = pd.to_datetime(orders_df['Ship Date'], errors='coerce')
    

# Order Count by Region (Pie Chart)
if 'Region' in orders_df.columns:
    region_counts = orders_df['Region'].value_counts()
    plt.figure(figsize=(8, 6))
    region_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette("viridis", len(region_counts)))
    plt.title("Order Count by Region")
    plt.ylabel("")
    plt.show()


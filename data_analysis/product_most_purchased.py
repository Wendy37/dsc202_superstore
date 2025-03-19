import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "./data_analysis/region_order_count.csv"
df = pd.read_csv(file_path)
df.columns = ["Region", "ProductName", "OrderCount"]

df["OrderCount"] = df["OrderCount"].astype(int)
top_5_gross_products = df.groupby("ProductName")["OrderCount"].sum().nlargest(5).index
top_5_gross_data = df[df["ProductName"].isin(top_5_gross_products)]
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")

ax = sns.lineplot(data=top_5_gross_data, x="Region", y="OrderCount", hue="ProductName", marker="o", linewidth=2.5, palette="viridis")

plt.title("Order Trends of Top 5 Grossing Products Across Regions", fontsize=14)
plt.ylabel("Order Count", fontsize=12)
plt.xlabel("Region", fontsize=12)
plt.legend(title="Product Name", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show Chart
plt.show()

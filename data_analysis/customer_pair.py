# Re-import necessary libraries since the execution state was reset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Simulated dataset similar to Neo4j query results
data = {
    "Product": ["Laptop", "Chair", "Printer", "Desk", "Monitor", "Pen", "Notebook"],
    "CustomerPairs": [15, 30, 10, 25, 18, 5, 12]  # Number of unique customer pairs who ordered the same product
}

# Create DataFrame
df = pd.DataFrame(data)

# Set visualization style
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Create a bar chart
ax = sns.barplot(x="Product", y="CustomerPairs", data=df, palette="mako")

# Annotate each bar with the corresponding value
for container in ax.containers:
    ax.bar_label(container, fmt="%d", fontsize=12, color="black", label_type="edge")

# Chart Formatting
plt.title("Number of Unique Customer Pairs Who Ordered the Same Product", fontsize=14)
plt.ylabel("Number of Customer Pairs", fontsize=12)
plt.xlabel("Product", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show Chart
plt.show()

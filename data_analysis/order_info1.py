from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

NEO4J_URI = "bolt://localhost:7691"  # Update with your Neo4j instance URI
USERNAME = "neo4j"  # Your Neo4j username
PASSWORD = "12345678"  # Your Neo4j password

QUERY = """
MATCH (o:Order)-[:CONTAINS]->(p:Product)
MATCH (o)-[:SHIPPED_TO]->(r:Region)
OPTIONAL MATCH (o)-[:RETURNED]->(ret:Return)
WITH r.RegionName AS Region, 
     p.Category AS ProductCategory,
     COUNT(o) AS TotalOrders,
     COUNT(ret) AS ReturnedOrders
RETURN Region, ProductCategory, 
       (toFloat(ReturnedOrders) / TotalOrders) * 100 AS ReturnRate,
       ReturnedOrders, TotalOrders
ORDER BY Region, ReturnRate DESC;
"""

def fetch_data(uri, user, password, query):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run(query)
        data = [record.data() for record in result]
    driver.close()
    return pd.DataFrame(data)

df = fetch_data(NEO4J_URI, USERNAME, PASSWORD, QUERY)

df["ReturnRate"] = df["ReturnRate"].astype(float)
df["TotalOrders"] = df["TotalOrders"].astype(int)
df["ReturnedOrders"] = df["ReturnedOrders"].astype(int)

# Set Visualization Style
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Create a Stacked Bar Chart
pivot_df = df.pivot(index="Region", columns="ProductCategory", values="ReturnRate")

# Plot the stacked bar chart
ax = pivot_df.plot(kind="bar", stacked=True, colormap="GnBu", figsize=(12, 6))

# Annotate each bar segment with its value
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f", label_type="center", fontsize=10, color="black")

# Chart Formatting
plt.title("Return Rate by Product Category & Region", fontsize=14)
plt.ylabel("Return Rate (%)", fontsize=12)
plt.xlabel("Region", fontsize=12)
plt.legend(title="Product Category")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show Chart
plt.show()
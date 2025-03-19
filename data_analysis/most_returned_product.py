from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Neo4j Database Connection (Update with actual credentials)
NEO4J_URI = "bolt://localhost:7691"  # Update with your Neo4j instance URI
USERNAME = "neo4j"  # Your Neo4j username
PASSWORD = "12345678"  # Your Neo4j password

# Define Neo4j Query to get most returned products in each region
QUERY = """
MATCH (o:Order)-[:CONTAINS]->(p:Product), (o)-[:SHIPPED_TO]->(r:Region)
OPTIONAL MATCH (o)-[:RETURNED]->(ret:Return)
WITH r.RegionName AS Region, 
     p.ProductName AS ProductName, 
     COUNT(o) AS OrderCount
RETURN Region, ProductName, OrderCount
ORDER BY Region, OrderCount DESC;
"""

# Function to Execute Query and Fetch Data
def fetch_data(uri, user, password, query):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run(query)
        data = [record.data() for record in result]
    driver.close()
    return pd.DataFrame(data)

# Fetch Data from Neo4j
df = fetch_data(NEO4J_URI, USERNAME, PASSWORD, QUERY)

# Convert Data Types
df["OrderCount"] = df["OrderCount"].astype(int)

# Set visualization style
plt.figure(figsize=(7, 3.5))
sns.set_theme(style="whitegrid")

# Create a Stacked Bar Chart
pivot_df = df.pivot(index="Region", columns="ProductName", values="OrderCount")

# Plot the stacked bar chart
ax = pivot_df.plot(kind="bar", stacked=True, colormap="coolwarm", figsize=(12, 6))

# Annotate each bar segment with its value
for container in ax.containers:
    ax.bar_label(container, fmt="%d", fontsize=10, color="black", label_type="center")

# Chart Formatting
plt.title("Most Returned Products in Each Region", fontsize=14)
plt.ylabel("Order Count", fontsize=12)
plt.xlabel("Region", fontsize=12)
plt.legend(title="Product Name", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show Chart
plt.show()

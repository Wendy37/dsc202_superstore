from neo4j import GraphDatabase
import pandas as pd

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

query_title = [
    "Top 10 Customers by Order Count",
    "Top 10 Products by Return Count",
    "Customers in the Same Region",
    "Most Returned Products in Each Region",
    "All Returned Products with Orders and Regions",
    "Customers Who Ordered the Same Product",
    "Most Popular Products by Region",
    "Top Customers by Sales in Each Region"
]

QUERIES = [
    # Top 10 Customers by Order Count
    """
    MATCH (c:Customer)-[:PLACED]->(o:Order)
    RETURN c.CustomerName AS Customer, COUNT(o) AS OrderCount
    ORDER BY OrderCount DESC
    LIMIT 10;
    """,

    # Top 10 Products by Return Count
    """
    MATCH (o:Order)-[:CONTAINS]->(p:Product)
    MATCH (o)-[:RETURNED]->(r:Return)
    WITH p.ProductName AS Product, COUNT(r) AS ReturnCount
    ORDER BY ReturnCount DESC
    LIMIT 10
    RETURN Product, ReturnCount;
    """,

    # Customers in the Same Region
    """
    MATCH (c1:Customer)-[:PLACED]->(o1:Order)-[:SHIPPED_TO]->(r:Region),
          (c2:Customer)-[:PLACED]->(o2:Order)-[:SHIPPED_TO]->(r)
    WHERE c1 <> c2
    RETURN c1.CustomerName AS Customer1, c2.CustomerName AS Customer2, r.RegionName AS Region;
    """,

    # Most Returned Products in Each Region
    """
    MATCH (o:Order)-[:CONTAINS]->(p:Product)
    MATCH (o)-[:SHIPPED_TO]->(r:Region)
    MATCH (o)-[:RETURNED]->(ret:Return)
    WITH p.ProductName AS Product, r.RegionName AS Region, COUNT(ret) AS ReturnCount
    RETURN Product, Region, ReturnCount
    ORDER BY Region, ReturnCount DESC;
    """,

    # All Returned Products with Orders and Regions
    """
    MATCH (o:Order)-[:CONTAINS]->(p:Product)
    MATCH (o)-[:SHIPPED_TO]->(r:Region)
    MATCH (o)-[:RETURNED]->(ret:Return)
    RETURN p.ProductName AS Product, o.OrderID AS OrderID, r.RegionName AS Region, ret.OrderID AS ReturnedOrder;
    """,

    # Customers Who Ordered the Same Product
    """
    MATCH (c1:Customer)-[:PLACED]->(o1:Order)-[:CONTAINS]->(p:Product)
          <-[:CONTAINS]-(o2:Order)<-[:PLACED]-(c2:Customer)
    WHERE c1 <> c2
    RETURN c1.CustomerName AS Customer1, c2.CustomerName AS Customer2, p.ProductName AS Product
    ORDER BY Product;
    """,

    # Most Popular Products by Region
    """
    MATCH (o:Order)-[:CONTAINS]->(p:Product), (o)-[:SHIPPED_TO]->(r:Region)
    RETURN r.RegionName AS Region, p.ProductName AS Product, COUNT(o) AS OrderCount
    ORDER BY Region, OrderCount DESC;
    """,

    # Top Customers by Sales in Each Region
    """
    MATCH (r:Region)
    CALL {
        WITH r
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:SHIPPED_TO]->(r)
        RETURN c.CustomerName AS Customer, SUM(o.Sales) AS TotalSales
        ORDER BY TotalSales DESC
        LIMIT 10
    }
    RETURN r.RegionName AS Region, Customer, TotalSales
    ORDER BY Region, TotalSales DESC;
    """
]

def execute_query(query):
    with driver.session() as session:
        result = session.run(query)
        return pd.DataFrame([dict(record) for record in result])

query_index = 0
while query_index < len(QUERIES):
    print(f"\nExecuting Query {query_index + 1}: {query_title[query_index]}...\n")
    df = execute_query(QUERIES[query_index])
    if not df.empty:
        print(df)
    else:
        print("No results found for this query.")

    query_index += 1

driver.close()
print("\nAll queries executed successfully.")
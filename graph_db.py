from neo4j import GraphDatabase
import pandas as pd

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:7687"  # Change this if running remotely
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"    # Using the password you set for the DBMS

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Load CSV data into Pandas
orders_df = pd.read_csv("Orders.csv")
people_df = pd.read_csv("People.csv")
returns_df = pd.read_csv("Returns.csv")

# Cypher Queries to create constraints for unique nodes
CONSTRAINT_QUERIES = [
    "CREATE CONSTRAINT FOR (c:Customer) REQUIRE c.CustomerID IS UNIQUE",
    "CREATE CONSTRAINT FOR (o:Order) REQUIRE o.OrderID IS UNIQUE",
    "CREATE CONSTRAINT FOR (p:Product) REQUIRE p.ProductID IS UNIQUE",
    "CREATE CONSTRAINT FOR (r:Region) REQUIRE r.RegionName IS UNIQUE",
    "CREATE CONSTRAINT FOR (m:Person) REQUIRE m.PersonName IS UNIQUE",
    "CREATE CONSTRAINT FOR (ret:Return) REQUIRE ret.OrderID IS UNIQUE"
]

# Function to execute queries
def execute_query(query, params=None):
    with driver.session() as session:
        session.run(query, params)

# Create constraints in Neo4j
for query in CONSTRAINT_QUERIES:
    try:
        execute_query(query)
    except Exception as e:
        print(f"Constraint creation error: {e}")

# Insert Customers
for _, row in orders_df.groupby(["Customer ID", "Customer Name", "Segment"]).size().reset_index().iterrows():
    query = """
    MERGE (c:Customer {CustomerID: $CustomerID})
    ON CREATE SET c.CustomerName = $CustomerName, c.Segment = $Segment
    """
    execute_query(query, {
        "CustomerID": row["Customer ID"],
        "CustomerName": row["Customer Name"],
        "Segment": row["Segment"]
    })

# Insert Orders
for _, row in orders_df.iterrows():
    query = """
    MERGE (o:Order {OrderID: $OrderID})
    ON CREATE SET o.OrderDate = $OrderDate, o.ShipDate = $ShipDate, o.Sales = $Sales, 
                  o.Discount = $Discount, o.Profit = $Profit
    """
    execute_query(query, {
        "OrderID": row["Order ID"],
        "OrderDate": row["Order Date"],
        "ShipDate": row["Ship Date"],
        "Sales": row["Sales"],
        "Discount": row["Discount"],
        "Profit": row["Profit"]
    })

# Insert Products
for _, row in orders_df.groupby(["Product ID", "Product Name", "Category", "Sub-Category"]).size().reset_index().iterrows():
    query = """
    MERGE (p:Product {ProductID: $ProductID})
    ON CREATE SET p.ProductName = $ProductName, p.Category = $Category, p.SubCategory = $SubCategory
    """
    execute_query(query, {
        "ProductID": row["Product ID"],
        "ProductName": row["Product Name"],
        "Category": row["Category"],
        "SubCategory": row["Sub-Category"]
    })

# Insert Regions
for _, row in orders_df.groupby(["Region"]).size().reset_index().iterrows():
    query = """
    MERGE (r:Region {RegionName: $RegionName})
    """
    execute_query(query, {
        "RegionName": row["Region"]
    })

# Insert People
for _, row in people_df.iterrows():
    query = """
    MERGE (m:Person {PersonName: $PersonName})
    ON CREATE SET m.Region = $Region
    """
    execute_query(query, {
        "PersonName": row["Person"],
        "Region": row["Region"]
    })

# Insert Returns
for _, row in returns_df.iterrows():
    query = """
    MERGE (ret:Return {OrderID: $OrderID})
    ON CREATE SET ret.Returned = $Returned
    """
    execute_query(query, {
        "OrderID": row["Order ID"],
        "Returned": row["Returned"]
    })

# Create Relationships
RELATIONSHIP_QUERIES = [
    # Customer -> Order
    """
    MATCH (c:Customer {CustomerID: $CustomerID}), (o:Order {OrderID: $OrderID})
    MERGE (c)-[:PLACED]->(o)
    """,
    
    # Order -> Product
    """
    MATCH (o:Order {OrderID: $OrderID}), (p:Product {ProductID: $ProductID})
    MERGE (o)-[:CONTAINS]->(p)
    """,
    
    # Order -> Region
    """
    MATCH (o:Order {OrderID: $OrderID}), (r:Region {RegionName: $RegionName})
    MERGE (o)-[:SHIPPED_TO]->(r)
    """,
    
    # Person -> Region
    """
    MATCH (m:Person {PersonName: $PersonName}), (r:Region {RegionName: $RegionName})
    MERGE (m)-[:MANAGES]->(r)
    """,
    
    # Order -> Return
    """
    MATCH (o:Order {OrderID: $OrderID}), (ret:Return {OrderID: $OrderID})
    MERGE (o)-[:RETURNED]->(ret)
    """
]

# Insert relationships
for _, row in orders_df.iterrows():
    execute_query(RELATIONSHIP_QUERIES[0], {"CustomerID": row["Customer ID"], "OrderID": row["Order ID"]})
    execute_query(RELATIONSHIP_QUERIES[1], {"OrderID": row["Order ID"], "ProductID": row["Product ID"]})
    execute_query(RELATIONSHIP_QUERIES[2], {"OrderID": row["Order ID"], "RegionName": row["Region"]})

for _, row in people_df.iterrows():
    execute_query(RELATIONSHIP_QUERIES[3], {"PersonName": row["Person"], "RegionName": row["Region"]})

for _, row in returns_df.iterrows():
    execute_query(RELATIONSHIP_QUERIES[4], {"OrderID": row["Order ID"]})

# Close the Neo4j connection
driver.close()

print("Graph database successfully created in Neo4j!")

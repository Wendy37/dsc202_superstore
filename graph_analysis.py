from neo4j import GraphDatabase

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678" 

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def execute_and_print_query(query, params=None):
    with driver.session() as session:
        result = session.run(query, params)
        for record in result:
            print(record)

QEURIES = [
    # Query 1: Top 10 Customers by Order Count
    """
    MATCH (c:Customer)-[:PLACED]->(o:Order)
    RETURN c.CustomerName, COUNT(o) AS OrderCount
    ORDER BY OrderCount DESC
    LIMIT 10;
    """,

    # Query 2: Top 10 Products by Return Count
    """
    MATCH (o:Order)-[:CONTAINS]->(p:Product)
    MATCH (o)-[:RETURNED]->(r:Return)
    WITH p, COUNT(r) AS ReturnCount
    ORDER BY ReturnCount DESC
    LIMIT 10
    MATCH (o)-[:CONTAINS]->(p)
    MATCH (o)-[:RETURNED]->(r)
    RETURN p, o, r;
    """,

    # Query 3: Customers in the Same Region
    
    """
    MATCH (c1:Customer)-[:PLACED]->(o1:Order)-[:SHIPPED_TO]->(r:Region),
        (c2:Customer)-[:PLACED]->(o2:Order)-[:SHIPPED_TO]->(r)
    WHERE c1 <> c2
    RETURN c1.CustomerName, c2.CustomerName, r.RegionName;
    """,

    # Query 7: 
    """
    MATCH (o:Order)-[:CONTAINS]->(p:Product)
    MATCH (o)-[:SHIPPED_TO]->(r:Region)
    MATCH (o)-[:RETURNED]->(ret:Return)
    WITH p, r, COUNT(ret) AS ReturnCount
    SET p.ReturnCount = ReturnCount
    RETURN p.ProductName, r.RegionName, p.ReturnCount
    ORDER BY r.RegionName, ReturnCount DESC;
    """,
    """MATCH (o:Order)-[:CONTAINS]->(p:Product)
    MATCH (o)-[:SHIPPED_TO]->(r:Region)
    MATCH (o)-[:RETURNED]->(ret:Return)
    RETURN p, o, r, ret, p.ReturnCount;
    """,

    # Query 8:
]



# Close the Neo4j connection
driver.close()

print("Queries executed successfully!")
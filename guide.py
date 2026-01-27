#############
# VADEMECUM #
#############


### CREATE ###

# node creation
q = """
    CREATE (n:Person {name: "Alice", age: 30});
    """

# edge creation
q = """
    MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
    CREATE (a)-[r:KNOWS]->(b);
    """

q = """
    MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
    CREATE (a)-[r:KNOWS {since: 2020, context: "Work"}]->(b);
    """

# node property creation or update
q = """
    MATCH (n:Product {name: "Laptop"})
    SET n.weight = 2.5,
        n.brand = "Lenovo";
    """

# edge property creation or update
q = """
    MATCH (a:Person {name:"Alice"})-[r:KNOWS]->(b:Person {name:"Bob"})
    SET r.strength = 5,
        r.description = "Friend";
    """

# merge (MATCH + CREATE) / create if not exist
# node
q = """
    MERGE (p:Person {name: "Alice"})
    ON CREATE SET p.createdAt = timestamp()
    ON MATCH  SET p.lastSeen = timestamp();
    """

# edge
q = """
    MATCH (a:Person {name: "Alice"})
    MATCH (b:Person {name: "Bob"})
    MERGE (a)-[r:KNOWS]->(b)
    ON CREATE SET r.since = 2020
    ON MATCH  SET r.lastSeen = timestamp();
    """


### MATCH ###

q = """
    MATCH (n)
    RETURN n;
    """

q = """
    MATCH (p:Person)
    RETURN p.name, p.age;
    """


q = """
    MATCH (a)-[r:KNOWS]->(b)
    RETURN a, r, b;
    """

q = """
    MATCH (p:Person)
    WHERE p.age > 30
    RETURN p;
    """


### DELETE ###

# delete edge
q = """
    MATCH (a)-[r:KNOWS]->(b)
    DELETE r;
    """

# delete node if isolated
q = """
    MATCH (p:Person {name:"Alice"})
    DELETE p;
    """

# delete node and all its edges
q = """
    MATCH (p:Person {name:"Alice"})
    DETACH DELETE p;
    """

# delete all
q = """
    MATCH (n)
    DETACH DELETE n
    """
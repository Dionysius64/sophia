import logging
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class GraphManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri,
                                           auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def run_dump(self, query):
        statements = [stmt.strip() for stmt in query.split(";") if stmt.strip()]

        try:
            with self.driver.session() as session:
                for i, stmt in enumerate(statements, start=1):
                    print(f"Running statement {i}/{len(statements)}...")
                    session.run(stmt)

            print("All Cypher statements executed successfully!")

        except Exception as e:
            print("Error while executing Cypher:")
            print(e)

        finally:
            self.driver.close()

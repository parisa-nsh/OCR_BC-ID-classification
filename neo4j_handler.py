from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import time

class Neo4jHandler:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password123")
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self._connect()

    def _connect(self):
        """Establish connection to Neo4j with retries"""
        for attempt in range(self.max_retries):
            try:
                self.driver = GraphDatabase.driver(
                    self.uri, 
                    auth=(self.user, self.password),
                    max_connection_lifetime=200
                )
                # Verify connection
                self.driver.verify_connectivity()
                return
            except Exception as e:
                print(f"Neo4j connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("Using fallback mode without database")
                    self.driver = None

    def close(self):
        """Close the Neo4j connection"""
        if self.driver:
            self.driver.close()

    def create_id_card_node(self, id_card_info):
        """Create a new ID card node with its properties"""
        if not self.driver:
            print("Database not available, skipping write operation")
            return

        try:
            with self.driver.session() as session:
                query = """
                CREATE (id:IDCard {
                    gender: $gender,
                    age: $age,
                    height: $height,
                    postal_code: $postal_code,
                    age_group: $age_group
                })
                """
                session.run(query, **id_card_info)
        except Exception as e:
            print(f"Error creating node: {str(e)}")

    def get_gender_distribution(self):
        """Get gender distribution statistics"""
        if not self.driver:
            return [{'gender': 'M', 'count': 0}, {'gender': 'F', 'count': 0}]

        try:
            with self.driver.session() as session:
                query = """
                MATCH (id:IDCard)
                RETURN id.gender as gender, count(*) as count
                """
                result = session.run(query)
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Error getting gender distribution: {str(e)}")
            return [{'gender': 'M', 'count': 0}, {'gender': 'F', 'count': 0}]

    def get_age_group_distribution(self):
        """Get age group distribution statistics"""
        if not self.driver:
            return [
                {'age_group': '18-24', 'count': 0},
                {'age_group': '25-49', 'count': 0},
                {'age_group': '50+', 'count': 0}
            ]

        try:
            with self.driver.session() as session:
                query = """
                MATCH (id:IDCard)
                RETURN id.age_group as age_group, count(*) as count
                """
                result = session.run(query)
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Error getting age group distribution: {str(e)}")
            return [
                {'age_group': '18-24', 'count': 0},
                {'age_group': '25-49', 'count': 0},
                {'age_group': '50+', 'count': 0}
            ]

    def get_height_distribution(self):
        """Get height distribution statistics"""
        if not self.driver:
            return [{'height': 170, 'count': 0}]

        try:
            with self.driver.session() as session:
                query = """
                MATCH (id:IDCard)
                RETURN id.height as height, count(*) as count
                ORDER BY id.height
                """
                result = session.run(query)
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Error getting height distribution: {str(e)}")
            return [{'height': 170, 'count': 0}]

    def get_postal_code_distribution(self):
        """Get postal code distribution statistics"""
        if not self.driver:
            return [{'postal_code': 'N/A', 'count': 0}]

        try:
            with self.driver.session() as session:
                query = """
                MATCH (id:IDCard)
                RETURN id.postal_code as postal_code, count(*) as count
                ORDER BY count(*) DESC
                """
                result = session.run(query)
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Error getting postal code distribution: {str(e)}")
            return [{'postal_code': 'N/A', 'count': 0}]

    def get_statistics(self):
        """Get all statistics in one query"""
        return {
            'gender_distribution': self.get_gender_distribution(),
            'age_group_distribution': self.get_age_group_distribution(),
            'height_distribution': self.get_height_distribution(),
            'postal_code_distribution': self.get_postal_code_distribution()
        } 
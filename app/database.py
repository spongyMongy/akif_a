from abc import ABC, abstractmethod
import psycopg2


class BaseDatabase(ABC):

    @abstractmethod
    def connect(self, query, data=None):
        pass

    @abstractmethod
    def execute_query(self, query, data=None):
        pass

    @abstractmethod
    def setup_database(self, query, data=None):
        pass


class PostgresDatabase(BaseDatabase):
    def __init__(self, host, port, user, password, database):
        self.db_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }

    def execute_query(self, query, data=None):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")

    def insert_metadata(self, metadata):
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS file_metadata (
                id SERIAL PRIMARY KEY,
                file_path TEXT,
                file_size INTEGER,
                file_type TEXT,
                architecture TEXT
            );
        """)
        for data in metadata:
            self.execute_query("""
                INSERT INTO file_metadata (file_path, file_size, file_type, architecture)
                VALUES (%s, %s, %s, %s);
            """, (data['file_path'], data['file_size'], data['file_type'],
                  data['architecture']))

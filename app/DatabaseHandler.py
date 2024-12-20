import psycopg2

from database import BaseDatabase


class DatabaseHandler(BaseDatabase):
    def __init__(self, host, port, user, password, database):
        self.db_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }
        self.connection = None
        self.connect()
        self.setup_database()

    def connect(self):
        """Establish a single connection to the database."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("Connected to the database successfully.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, data=None):
        """Execute a query with optional parameters."""
        try:
            if self.connection is None or self.connection.closed:
                print("Reconnecting to the database...")
                self.connect()

            with self.connection.cursor() as cursor:
                print(f"Executing query: {query}")
                print(f"With data: {data}")
                cursor.execute(query, data)
                self.connection.commit()
        except psycopg2.IntegrityError as e:
            print(f"Integrity error: {e}")
            self.connection.rollback()
        except Exception as e:
            print(f"Database error: {e}")
            self.connection.rollback()

    def setup_database(self):
        """Ensure the necessary schema and table exist."""
        try:
            with self.connection.cursor() as cursor:
                # Create the schema if it doesn't exist
                cursor.execute("""
                    CREATE SCHEMA IF NOT EXISTS filedb;
                """)
                print("Schema `filedb` has been ensured.")

                # Create the table within the schema
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS filedb.file_metadata (
                        id SERIAL PRIMARY KEY,
                        file_path TEXT UNIQUE, -- Ensure file_path is unique
                        file_size INTEGER,
                        file_type TEXT,
                        architecture TEXT,
                        number_of_imports INT,
                        number_of_exports INT
                    );
                """)
                print(
                    "Table `file_metadata` within schema `filedb` has been created or already exists.")
        except Exception as e:
            print(f"Error ensuring schema and table exist: {e}")

    def insert_metadata(self, metadata):
        """Insert metadata into the database."""

        for data in metadata:
            if not self.check_metadata_exists(data.get("file_path")):

                print(f"Processing metadata: {data}")
                try:
                    self.execute_query("""
                        INSERT INTO filedb.file_metadata (file_path, file_size, 
                        file_type, architecture, number_of_imports, number_of_exports)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (data['file_path'], data['file_size'], data['file_type'],
                          data['architecture'], data["number_of_imports"], data["number_of_exports"]))
                    print(f"Inserted metadata for: {data['file_path']}")
                except psycopg2.IntegrityError as e:
                    print(f"Duplicate entry for {data['file_path']}: {e}")
                except Exception as e:
                    print(f"Error inserting {data['file_path']}: {e}")
            else:
                print("Data already exist.")

    def check_metadata_exists(self, file_path):
        """Check if metadata for a file already exists in the database."""
        try:
            if self.connection is None or self.connection.closed:
                print("Reconnecting to the database...")
                self.connect()

            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM filedb.file_metadata WHERE file_path = %s
                    );
                """, (file_path,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Database error while checking metadata: {e}")
            return False

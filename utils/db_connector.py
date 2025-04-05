import psycopg2
from psycopg2 import sql
from config.constants import DBConfig

class DBConnector:
    @staticmethod
    def get_connection():
        try:
            conn = psycopg2.connect(
                dbname=DBConfig.DB_NAME,
                user=DBConfig.DB_USER,
                password=DBConfig.DB_PASSWORD,
                host=DBConfig.DB_HOST,
                port=DBConfig.DB_PORT
            )
            return conn
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None

    @staticmethod
    def get_schema(conn):
        schema = {}
        try:
            with conn.cursor() as cursor:
                # Get all tables
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cursor.fetchall()]

                # Get columns and foreign keys for each table
                for table in tables:
                    # Get columns
                    cursor.execute(sql.SQL("""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = {}
                    """).format(sql.Literal(table)))
                    columns = cursor.fetchall()

                    # Get foreign keys
                    cursor.execute("""
                        SELECT
                            tc.table_name, 
                            kcu.column_name, 
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name 
                        FROM 
                            information_schema.table_constraints AS tc 
                            JOIN information_schema.key_column_usage AS kcu
                              ON tc.constraint_name = kcu.constraint_name
                            JOIN information_schema.constraint_column_usage AS ccu
                              ON ccu.constraint_name = tc.constraint_name
                        WHERE 
                            tc.constraint_type = 'FOREIGN KEY' 
                            AND tc.table_name = %s
                    """, (table,))
                    foreign_keys = cursor.fetchall()

                    schema[table] = {
                        'columns': columns,
                        'foreign_keys': foreign_keys
                    }
            return schema
        except Exception as e:
            print(f"Error fetching schema: {e}")
            return None
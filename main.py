import argparse
from utils.db_connector import DBConnector
from  utils.diagram_generator import DiagramGenerator

def main():
    parser = argparse.ArgumentParser(description='Database Schema Visualizer')
    parser.add_argument('--dbname', help='Database name')
    parser.add_argument('--user', help='Database username')
    parser.add_argument('--password', help='Database password')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='5432', help='Database port')
    parser.add_argument('--output', default='diagrams/schema_diagram', 
                       help='Output path for diagram (without extension)')
    args = parser.parse_args()

    # Update config if arguments provided
    if args.dbname or args.user or args.password:
        from config import constants
        if args.dbname:
            constants.DBConfig.DB_NAME = args.dbname
        if args.user:
            constants.DBConfig.DB_USER = args.user
        if args.password:
            constants.DBConfig.DB_PASSWORD = args.password
        if args.host:
            constants.DBConfig.DB_HOST = args.host
        if args.port:
            constants.DBConfig.DB_PORT = args.port

    # Connect to database and generate diagram
    conn = DBConnector.get_connection()
    if conn:
        schema = DBConnector.get_schema(conn)
        conn.close()
        
        if schema:
            output_path = DiagramGenerator.generate_pdf(schema, args.output)
            print(f"Successfully generated diagram at: {output_path}")
        else:
            print("Failed to generate schema diagram.")
    else:
        print("Could not connect to database.")

if __name__ == "__main__":
    main()
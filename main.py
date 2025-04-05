import argparse
import google.generativeai as genai
from pathlib import Path
from utils.db_connector import DBConnector
from utils.diagram_generator import DiagramGenerator
from config.settings import AIConfig

# Initialize Gemini
genai.configure(api_key=AIConfig.API_KEY)  # Replace with your actual API key
model = genai.GenerativeModel(AIConfig.MODEL)

def generate_sql_from_natural_language(schema_pdf_path, user_query):
    """Send schema PDF to Gemini and generate SQL from natural language"""
    try:
        # Upload the generated schema PDF
        pdf_file = genai.upload_file(schema_pdf_path)
        
        response = model.generate_content([
            "You are a PostgreSQL expert. Given this database schema:",
            pdf_file,
            f"Convert this natural language query to SQL:\n{user_query}\n"
            "Provide ONLY the SQL code, no explanations."
        ])
        
        return response.text.strip()
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Database Schema Visualizer with AI Assistant')
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
            # Generate the schema diagram PDF
            pdf_path = DiagramGenerator.generate_pdf(schema, args.output)
            print(f"Schema diagram generated at: {pdf_path}")
            
            # AI Query Interface
            while True:
                print("\nAI SQL Assistant (type 'exit' to quit)")
                user_query = input("Enter your query in natural language: ")
                
                if user_query.lower() == 'exit':
                    break
                    
                if user_query.strip():
                    sql = generate_sql_from_natural_language(pdf_path, user_query)
                    if sql:
                        print("\nGenerated SQL:\n" + sql)
                        # Add execute option here if needed
        else:
            print("Failed to generate schema diagram.")
    else:
        print("Could not connect to database.")

if __name__ == "__main__":
    main()
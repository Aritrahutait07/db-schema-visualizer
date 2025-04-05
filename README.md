# Database Schema Visualizer with AI SQL Assistant

![image](https://github.com/user-attachments/assets/4918fd4b-4e2b-44f0-83c6-35b052b47258)


A Python tool that automatically:
1. Generates PDF diagrams of PostgreSQL database schemas
2. Converts natural language queries to SQL using Google Gemini AI

## Features

- **Schema Visualization**
  - Auto-detects tables, columns, and relationships
  - Generates professional PDF diagrams with Graphviz
  - Supports custom styling and layouts

- **AI SQL Assistant**
  - Natural language to SQL conversion
  - Uses Google Gemini AI for accurate query generation
  - Supports schema-aware query suggestions

- **Database Connectivity**
  - PostgreSQL support with psycopg2
  - Configurable connection parameters
  - Secure credential management via `.env`

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/db-schema-visualizer.git
   cd db-schema-visualizer

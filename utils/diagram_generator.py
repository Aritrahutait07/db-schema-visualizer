from graphviz import Digraph
import os

class DiagramGenerator:
    @staticmethod
    def generate_pdf(schema, output_path="diagrams/schema_diagram"):
        dot = Digraph(comment='Database Schema', format='pdf')
        dot.attr(rankdir='LR', fontname='Helvetica', nodesep='0.5')  # Layout settings
        
        # Custom style for tables
        table_style = {
            'shape': 'plaintext',
            'margin': '0',
            'fontname': 'Helvetica'
        }

        # Add tables with proper HTML-like table representation
        for table_name, table_data in schema.items():
            # Create HTML table structure
            table_label = '''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                <TR><TD COLSPAN="2" BGCOLOR="#1e81b0"><FONT COLOR="white"><B>{}</B></FONT></TD></TR>
                {}
            </TABLE>>'''.format(
                table_name.upper(),
                '\n'.join([
                    '<TR><TD ALIGN="LEFT" PORT="{}">{}</TD><TD ALIGN="LEFT">{}</TD></TR>'.format(
                        col[0], col[0], col[1]
                    ) 
                    for col in table_data['columns']
                ])
            )
            
            dot.node(table_name, table_label, **table_style)

        # Add relationships with proper styling
        for table_name, table_data in schema.items():
            for fk in table_data['foreign_keys']:
                dot.edge(
                    '{}:{}'.format(fk[0], fk[1]),  # Source table and column
                    '{}:{}'.format(fk[2], fk[3]),  # Target table and column
                    label='',  # No label on the line itself
                    arrowhead='vee',  # Solid arrow
                    arrowsize='0.7',
                    penwidth='1.5',
                    color='#666666'
                )

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Render and save
        dot.render(output_path, cleanup=True)
        print(f"Diagram generated at: {output_path}.pdf")
        return f"{output_path}.pdf"
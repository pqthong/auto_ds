import re
import sqlparse
from graphviz import Digraph

def parse_sql_to_erd(sql):
    statements = sqlparse.parse(sql)
    tables = {}
    relationships = []

    for stmt in statements:
        if stmt.get_type() == "CREATE":
            table_name = None
            columns = []

            for token in stmt.tokens:
                if token.ttype is None and token.get_real_name():
                    table_name = token.get_real_name()

                if isinstance(token, sqlparse.sql.Parenthesis):
                    col_defs = token.get_sublists()
                    for col_def in col_defs:
                        col_parts = [p.get_real_name() for p in col_def.get_sublists() if p.get_real_name()]
                        if col_parts:
                            columns.append(col_parts[0])

                        if "FOREIGN" in col_def.value:
                            ref_table = re.findall(r"REFERENCES\s+(\w+)", col_def.value)
                            if ref_table:
                                relationships.append((table_name, ref_table[0]))

            if table_name and columns:
                tables[table_name] = columns

    return tables, relationships

def generate_erd(sql):
    tables, relationships = parse_sql_to_erd(sql)

    dot = Digraph()

    for table, columns in tables.items():
        label = f"{{ {table} | " + " | ".join(columns) + " }}"
        dot.node(table, label=label, shape="record")

    for from_table, to_table in relationships:
        dot.edge(from_table, to_table, label="FK")

    return dot
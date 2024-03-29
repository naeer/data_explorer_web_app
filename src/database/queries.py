
def get_tables_list_query():
    """
    --------------------
    Description
    --------------------
    -> get_tables_list_query (method): Function that returns the query used for extracting the list of tables from a Postgres table

    --------------------
    Parameters
    --------------------
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Set the query to extract the list of tables (in the form of schema.table) from a Postgres database in a variable called query
    -> Return that variable

    --------------------
    Returns
    --------------------
    -> (str): Returns the query that is used to extract the list of tables from a Postgres database
    """
    query = "SELECT table_schema || '.' || table_name AS table_name FROM information_schema.tables;"
    return query

def get_table_data_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> get_table_data_query (method): Function that returns the query used for extracting the content of a Postgres table

    --------------------
    Parameters
    --------------------
    -> schema_name (str): Name of the schema on which the SQL query is going to be executed on
    -> table_name (str): Name of the table (in the schema) on which the SQL query is going to be executed on

    --------------------
    Pseudo-Code
    --------------------
    -> If schema_name and table_name has values, i.e., they are not empty or None:
        -> Set the query to extract the content of a Postgres table in a variable called query
        -> Return that variable
    -> Return None

    --------------------
    Returns
    --------------------
    -> (str): If schema_name and table_name exists, returns the query that is used to extract the content of a Postgres table. Otherwise, returns None
    """
    if schema_name and table_name:
        query = f"SELECT * FROM {schema_name}.{table_name}"
        return query
    return None

def get_table_schema_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> get_table_schema_query (method): Function that returns the query used for extracting the list of columns from a Postgres table and their information

    --------------------
    Parameters
    --------------------
    -> schema_name (str): Name of the schema on which the SQL query is going to be executed on
    -> table_name (str): Name of the table (in the schema) on which the SQL query is going to be executed on

    --------------------
    Pseudo-Code
    --------------------
    -> If schema_name and table_name has values, i.e., they are not empty or None:
        -> Set the query to extract a list of columns and their information from a Postgres table in a variable called query
        -> Return that variable
    -> Return None

    --------------------
    Returns
    --------------------
    -> (str): If schema_name and table_name exists, returns the query that is used to extract a list of columns and their information from a Postgres table. Otherwise returns None
    """
    if schema_name and table_name:
        query = f"SELECT c.table_name, c.column_name, c.data_type, CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k WHERE c.table_name = k.table_name and k.column_name = c.column_name) THEN true ELSE false END as primary_key, c.is_nullable, c.character_maximum_length, c.numeric_precision FROM INFORMATION_SCHEMA.COLUMNS c WHERE c.table_schema='{schema_name}' AND c.table_name='{table_name}'"
        return query
    return None

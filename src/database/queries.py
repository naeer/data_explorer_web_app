
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
    -> Set the query to extract the list of tables from a Postgres database in a variable called query
    -> Return that variable

    --------------------
    Returns
    --------------------
    -> (str): Returns the query that is used to extract the list of tables from a Postgres database
    """
    query = "SELECT table_schema, table_name FROM information_schema.tables;"
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
    -> Set the query to extract the content of a Postgres table in a variable called query
    -> Return that variable

    --------------------
    Returns
    --------------------
    -> (str): Returns the query that is used to extract the content of a Postgres table
    """
    query = f"SELECT * FROM {schema_name}.{table_name}"
    return query


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
    => To be filled by student
    -> pseudo-code
    -> Set the query to extract a list of columns and their information from a Postgres table in a variable called query
    -> Return that variable

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description
    -> (str): Returns the query that is used to extract a list of columns and their information from a Postgres table
    """
    query = f"SELECT * FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = '{table_name}';"
    return query

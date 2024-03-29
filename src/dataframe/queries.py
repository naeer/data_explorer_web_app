def get_numeric_tables_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    get_numeric_tables_query (method): Function that returns the query used for extracting the list of numeric columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str): name of selected Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)

    """
    query = f"select column_name from information_schema.columns where table_schema = '{schema_name}' and table_name = '{table_name}' and data_type in ('smallint', 'integer', 'bigint', 'decimal', 'numeric', 'real', 'double precision', 'smallserial', 'serial', 'bigserial', 'money')"
    return query

def get_text_tables_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    get_text_tables_query (method): Function that returns the query used for extracting the list of text columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str): name of selected Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)

    """
    query = f"select column_name from information_schema.columns where table_schema = '{schema_name}' and table_name = '{table_name}' and data_type in ('character varying', 'varchar', 'character', 'text', 'char', 'name', 'bytea')"
    return query

def get_date_tables_query(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    get_date_tables_query (method): Function that returns the query used for extracting the list of datetime columns from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str): name of selected Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)
    """
    query = f"select column_name from information_schema.columns where table_schema = '{schema_name}' and table_name = '{table_name}' and data_type in ('timestamp without time zone', 'timestamp with time zone', 'time with time zone', 'time without time zone', 'interval', 'date')"
    return query

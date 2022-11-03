def get_negative_number_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_negative_number_query (method): Function that returns the query used for computing the number of times a column from a Postgres table has negative values 

    --------------------
    Parameters
    --------------------
    -> schema_name (str): The name of the database schema
    -> table_name (str): The name of the table containing the required column. 
    -> col_name (str): The column being analysed 

    --------------------
    Pseudo-Code
    --------------------
    -> Construct query using passed parameters

    --------------------
    Returns
    --------------------
    -> query (str): Constructed query used to determine the number of negative values for passed schema, table and column

    """
    query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} < 0"
    return query

def get_std_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_std_query (method): Function that returns the query used for computing the standard deviation value of a column from a Postgres table

    --------------------
    Parameters
    --------------------
    -> schema_name (str): The name of the database schema
    -> table_name (str): The name of the table containing the required column. 
    -> col_name (str): The column being analysed 

    --------------------
    Pseudo-Code
    --------------------
    -> Construct query using passed parameters

    --------------------
    Returns
    --------------------
    -> query (str): Constructed query used to determine the standard deviation of the values for passed schema, table and column

    """
    query = f"""select stddev({col_name}) from {schema_name}.{table_name}"""
    return query

def get_unique_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_unique_query (method): Function that returns the query used for computing the number of unique values of a column from a Postgres table

    --------------------
    Parameters
    --------------------
    -> schema_name (str): The name of the database schema
    -> table_name (str): The name of the table containing the required column. 
    -> col_name (str): The column being analysed 

    --------------------
    Pseudo-Code
    --------------------
    -> Construct query using passed parameters

    --------------------
    Returns
    --------------------
    -> query (str): Constructed query used to determine the the number of unique values for passed schema, table and column

    """
    query = f"select count(distinct {col_name}) from {schema_name}.{table_name}"
    return query
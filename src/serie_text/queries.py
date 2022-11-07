import statistics

def get_mode_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_mode_query (method): Function that returns the query used for computing the mode value of a column from a Postgres table
"""
    query = f"select mode() within group (order by {col_name}) from {schema_name}.{table_name}"
    return query

def get_alpha_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_alpha_query (method): Function that returns the query used for computing the number of times a column from a Postgres table has only alphabetical characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '^[[:alpha:]]*$'" #this returns characters only with a space

    return query


def get_whitespace(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_whitespace (method): Function that returns the query used for computing the number of times a serie has only space characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '^[[:space:]]*$'" #this returns characters only with a space

    return query

def get_lowercase(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_lowercase (method): Function that returns the query used for computing the number of times a serie has only lowercase characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '^[[:lower:]]*$'" 

    return query

def get_uppercase(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_uppercase (method): Function that returns the query used for computing the number of times a serie has only uppercase characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '^[[:upper:]]*$'" 

    return query

def get_digit(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_digit (method): Function that returns the query used for computing the number of times a serie has only digit characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '^[[:digit:]]*$'" 

    return query

def get_missing_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_missing_query (method): Function that returns the query used for computing the number of missing values of a column from a Postgres table
"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name}  is NULL"

    return query 
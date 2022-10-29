def get_mode_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_mode_query (method): Function that returns the query used for computing the mode value of a column from a Postgres table
"""
    query = f"SELECT round(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY {col_name}) ::numeric, 2) median_unit_price FROM {schema_name}.{table_name}"
 
    return query

def get_alpha_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_alpha_query (method): Function that returns the query used for computing the number of times a column from a Postgres table has only alphabetical characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:alpha:]]'" #this returns characters only with a space

    return query


def get_whitespace(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_whitespace (method): Function that returns the query used for computing the number of times a serie has only space characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:space:]]'" #this returns characters only with a space

    return query

def get_lowercase(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_lowercase (method): Function that returns the query used for computing the number of times a serie has only lowercase characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where lower({col_name})" 

    return query

def get_uppercase(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_uppercase (method): Function that returns the query used for computing the number of times a serie has only uppercase characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where upper({col_name})" 

    return query

def get_digit(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_digit (method): Function that returns the query used for computing the number of times a serie has only digit characters

"""
    query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:digit:]]'" 

    return query
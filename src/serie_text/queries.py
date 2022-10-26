def get_missing_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_missing_query (method): Function that returns the query used for computing the number of missing values of a column from a Postgres table
"""
 query = 'SELECT count(*) FROM' + schema_name +'.' +table_name +' where '+col_name +'is NULL;'

return query

def get_mode_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_mode_query (method): Function that returns the query used for computing the mode value of a column from a Postgres table
"""
 query = 'SELECT round(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY '+col_name+') ::numeric, 2) median_unit_price FROM' + schema_name +'.' +table_name +';'

def get_alpha_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    -> get_alpha_query (method): Function that returns the query used for computing the number of times a column from a Postgres table has only alphabetical characters

"""
query = 'SELECT count(*) FROM' + schema_name +'.' +table_name +' where '+col_name +'~ ''^[[:alnum:],.!?; ]+$';' #this does number letter and ,.!?; characters

return query
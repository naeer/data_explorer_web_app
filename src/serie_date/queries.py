def get_column_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_column_query (method): Function that returns the query used for extracting selected column from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)

    """
    query = f"select {col_name} from {schema_name}.{table_name}"
    return query

def get_min_date_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_min_date_query (method): Function that returns the query used for computing the earliest date of a datetime column from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)

    """
    query = f"select min({col_name}) from {schema_name}.{table_name}"
    return query

def get_max_date_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_max_date_query (method): Function that returns the query used for computing the latest date of a datetime column from a Postgres table

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)
    """
    query = f"select max({col_name}) from {schema_name}.{table_name}"
    return query

def get_weekend_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_weekend_count_query (method): Function that returns the query used for computing the number of times a date of a datetime column falls during weekends

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)
    """
    query = f"select count({col_name}) from {schema_name}.{table_name} where extract(isodow from {col_name}) in (6, 7)"
    return query

def get_weekday_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_weekday_count_query (method): Function that returns the query used for computing the number of times a date of a datetime column falls during weekdays

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)
    """
    query = f"select count({col_name}) from {schema_name}.{table_name} where extract(isodow from {col_name}) in (1, 2, 3, 4, 5)"
    return query

def get_future_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_future_count_query (method): Function that returns the query used for computing the number of times a date of a datetime column falls after current datetime

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)

    """
    query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} > current_date"
    return query

def get_1900_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_1900_count_query (method): Function that returns the query used for computing the number of times a datetime column has the value '1900-01-01'

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)

    """
    query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} = '1900-01-01'"
    return query

def get_1970_count_query(schema_name, table_name, col_name):
    """
    --------------------
    Description
    --------------------
    get_1970_count_query (method): Function that returns the query used for computing the number of times a datetime column has the value '1970-01-01'

    --------------------
    Parameters
    --------------------
    schema_name(str), table_name(str), col_name(str): name of selected column fom Postgres table

    --------------------
    Returns
    --------------------
    SQL query(str)
    """
    query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} = '1970-01-01'"
    return query

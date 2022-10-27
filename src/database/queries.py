
def get_tables_list_query():
	"""
    --------------------
    Description
    --------------------
    -> get_tables_list_query (method): Function that returns the query used for extracting the list of tables from a Postgres table

    --------------------
    Parameters
    --------------------
    => To be filled by student
    -> name (type): description

    --------------------
    Pseudo-Code
    --------------------
    => To be filled by student
    -> pseudo-code

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
	query = "select table_name from information_schema.tables where table_schema = 'public'"
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
    => To be filled by student
    -> name (type): description

    --------------------
    Pseudo-Code
    --------------------
    => To be filled by student
    -> pseudo-code

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
	query = f'select * from {schema_name}.{table_name}'
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
    => To be filled by student
    -> name (type): description

    --------------------
    Pseudo-Code
    --------------------
    => To be filled by student
    -> pseudo-code

    --------------------
    Returns
    --------------------
    => To be filled by student
    -> (type): description

    """
	query = f"SELECT c.table_name, c.column_name, c.data_type, CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k WHERE c.table_name = k.table_name and k.column_name = c.column_name) THEN true ELSE false END as primary_key, c.is_nullable, c.character_maximum_length, c.numeric_precision FROM INFORMATION_SCHEMA.COLUMNS c WHERE c.table_name='employees'"
	#query = f'select column_name, data_type from information_schema.columns where table_schema = {schema_name} and table_name = {table_name}'
	return query

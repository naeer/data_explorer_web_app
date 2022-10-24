import psycopg2
from psycopg2 import OperationalError
import pandas as pd

from src.database.queries import get_tables_list_query, get_table_data_query, get_table_schema_query

class PostgresConnector:
    """
    --------------------
    Description
    --------------------
    -> PostgresConnector (class): Class that manages the connection to a Postgres database

    --------------------
    Attributes
    --------------------
    -> database (str): Name of Postgres database (mandatory)
    -> user (str): Username used for connecting to Postgres database (mandatory)
    -> password (str): Password used for connecting to Postgres database (mandatory)
    -> host (str): URL of Postgres database (mandatory)
    -> port (str): Port number of Postgres database (mandatory)
    -> conn (psycopg2._psycopg.connection): Postgres connection object (optional)
    -> cursor (psycopg2._psycopg.connection.cursor): Postgres cursor for executing query (optional)
    -> excluded_schemas (list): List containing the names of internal Postgres schemas to be excluded from selection (information_schema, pg_catalog)
    """
    def __init__(self, database="postgres", user='postgres', password='password', host='127.0.0.1', port='5432'):
        #=> To be filled by student
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.excluded_schemas = ['information_schema', 'pg_catalog']
    
    def open_connection(self):
        """
        --------------------
        Description
        --------------------
        -> open_connection (method): Class method that creates an active connection to a Postgres database

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
        #=> To be filled by student
        try:
            self.conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database)
        except OperationalError:
            print(OperationalError)

    def close_connection(self):
        """
        --------------------
        Description
        --------------------
        -> close_connection (method): Class method that closes an active connection to a Postgres database

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
        #=> To be filled by student
        self.conn.close()

    def open_cursor(self):
        """
        --------------------
        Description
        --------------------
        -> open_cursor (method): Class method that creates an active cursor to a Postgres database 

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
        #=> To be filled by student
        self.cursor = self.conn.cursor()

        
    def close_cursor(self):
        """
        --------------------
        Description
        --------------------
        -> close_cursor (method): Class method that closes an active cursor to a Postgres database 

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
        #=> To be filled by student
        self.cursor.close()

    def run_query(self, sql_query):
        """
        --------------------
        Description
        --------------------
        -> run_query (method): Class method that executes a SQL query and returns the result as a Pandas dataframe

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
        #=> To be filled by student
        self.cursor.execute(sql_query)
        query_result = self.cursor.fetchall()
        query_result_df = pd.DataFrame(query_result)
        return query_result_df
        
    def list_tables(self):
        """
        --------------------
        Description
        --------------------
        -> list_tables (method): Class method that extracts the list of available tables using a SQL query (get_tables_list_query())

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
        #=> To be filled by student
        sql_query = get_tables_list_query()
        self.cursor.execute(sql_query)
        query_result = self.cursor.fetchall()
        list_tables = []
        for tuples in query_result:
            for i in range(len(tuples)):
                if tuples[i] not in self.excluded_schemas and i == 0:
                    i = i + 1
                    list_tables.append(tuples[i])
        return list_tables

    def load_table(self, schema_name, table_name):
        """
        --------------------
        Description
        --------------------
        -> load_table (method): Class method that load the content of a table using a SQL query (get_table_data_query())

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
        #=> To be filled by student
        sql_query = get_table_data_query(schema_name=schema_name, table_name=table_name)
        self.cursor.execute(sql_query)
        query_result = self.cursor.fetchall()
        return query_result

    def get_table_schema(self, schema_name, table_name):
        """
        --------------------
        Description
        --------------------
        -> get_table_schema (method): Class method that extracts the schema information of a table using a SQL query (get_table_schema_query())

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
        # => To be filled by student
        sql_query = get_table_schema_query(schema_name=schema_name, table_name=table_name)
        self.cursor.execute(sql_query)
        query_result = self.cursor.fetchall()
        return query_result
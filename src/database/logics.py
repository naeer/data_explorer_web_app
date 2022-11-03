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
        -> self (class object): Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        => To be filled by student
        -> pseudo-code
        -> try:
            -> Create an active connection to the Postgres database by calling the connect() function of psycopg2 class and passing the user, password, host, port and name of database
            -> Return the active connection object
        -> except:
            -> Return None

        --------------------
        Returns
        --------------------
        -> (psycopg2.extensions.connection) Returns an active connection object if connection successful, otherwise returns None

        """
        try:
            self.conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database)
            return self.conn
        except OperationalError:
            self.conn = None
            return self.conn

    def close_connection(self):
        """
        --------------------
        Description
        --------------------
        -> close_connection (method): Class method that closes an active connection to a Postgres database

        --------------------
        Parameters
        --------------------
        -> self (class object): Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Close an active connection to the Postgres database by calling the close method of the connection class in psycopg2 package

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.conn:
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
        -> self (class object): Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Create an active cursor to the Postgres database by calling the cursor method of the connection class in psycopg2 package

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.conn:
            self.cursor = self.conn.cursor()
        else:
            self.cursor = None

    def close_cursor(self):
        """
        --------------------
        Description
        --------------------
        -> close_cursor (method): Class method that closes an active cursor to a Postgres database

        --------------------
        Parameters
        --------------------
        -> self (class object): Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Close an active cursor to the Postgres database by calling the close method of the connection class in pyscopg2 package

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.cursor:
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
        -> self (class object): Reference to the current instance of the class
        -> sql_query (str): The SQL query that is going to be executed on the database

        --------------------
        Pseudo-Code
        --------------------
        -> Execute the SQL query by passing the sql_query parameter to the execute() method of the cursor class in psycopg2 package
        -> Retrieve all the rows from the result of the SQL query by calling the fetchall() method of the cursor class and store them in a variable
        -> Convert the results of the SQL query to a Pandas dataframe
        -> Return the Pandas dataframe

        --------------------
        Returns
        --------------------
        -> (pandas.core.frame.DataFrame): Returns the result of a SQL query as a Pandas dataframe

        """
        if self.cursor and sql_query:
            self.cursor.execute(sql_query)
            query_result = self.cursor.fetchall()
            query_result_df = pd.DataFrame(query_result)
            return query_result_df
        return None
        
    def list_tables(self):
        """
        --------------------
        Description
        --------------------
        -> list_tables (method): Class method that extracts the list of available tables using a SQL query (get_tables_list_query())

        --------------------
        Parameters
        --------------------
        -> self (class object): Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Get the SQL query from get_tables_list_query() function that retrieves the list of tables and their schema name from a Postgres database
        -> Execute the SQL query by calling the execute() method of the cursor class
        -> Retrieve all the rows from the result of the SQL query by calling the fetchall() method and store them in a variable called query_result
        -> Declare an empty list for the list of tables
        -> For all the tables and their schema names in the SQL query result:
            -> Check that the schema name for the table is not same as the excluded schemas (information_schema, pg_catalog)
            -> If the schema name is not the same as the excluded schemas:
                -> Take the table name and append it to the list of tables
        -> Return the list of tables (which are not part of the excluded schemas)

        --------------------
        Returns
        --------------------
        -> (list): Returns a list of available tables from a database by exeuting a SQL query 

        """
        sql_query = get_tables_list_query()
        if self.cursor:
            self.cursor.execute(sql_query)
            query_result = self.cursor.fetchall()
            list_tables = []
            for results in query_result:
                result_after_split = results[0].split(".")
                if result_after_split[0] not in self.excluded_schemas:
                    list_tables.append(results[0])
            return list_tables
        return None

    def load_table(self, schema_name, table_name):
        """
        --------------------
        Description
        --------------------
        -> load_table (method): Class method that load the content of a table using a SQL query (get_table_data_query())

        --------------------
        Parameters
        --------------------
        -> self (class object): Reference to the current instance of the class
        -> schema_name (str): Name of the schema on which the SQL query is going to be executed on
        -> table_name (str): Name of the table (in the schema) on which the SQL query is going to be executed on

        --------------------
        Pseudo-Code
        --------------------
        -> Get the SQL query from the get_table_data_query() function by passing the schema name and the table name
        -> Execute the SQL query by calling the execute() method of the cursor class
        -> Retrieve all the rows from the result of the SQL query by calling the fetchall() method and the column names of the table and store it as a Pandas dataframe
        -> Return the Pandas dataframe

        --------------------
        Returns
        --------------------
        -> (pandas.core.frame.DataFrame): Returns the content of a table as a Pandas dataframe by passing the name of the schema and the table to a SQL query

        """
        query = get_table_data_query(schema_name, table_name)
        if self.cursor:
            self.cursor.execute(query)
            df = pd.DataFrame(self.cursor.fetchall(), columns=[desc[0] for desc in self.cursor.description])
            return df
        return None

    def get_table_schema(self, schema_name, table_name):
        """
        --------------------
        Description
        --------------------
        -> get_table_schema (method): Class method that extracts the schema information of a table using a SQL query (get_table_schema_query())

        --------------------
        Parameters
        --------------------
        -> self (class object): Reference to the current instance of the class
        -> schema_name (str): Name of the schema on which the SQL query is going to be executed on
        -> table_name (str): Name of the table (in the schema) on which the SQL query is going to be executed on

        --------------------
        Pseudo-Code
        --------------------
        -> Get the SQL query from the get_table_schema_query() function by passing the schema name and the table name
        -> Execute the SQL query by calling the execute() method of the cursor class
        -> Retrieve all the rows from the result of the SQL query by calling the fetchall() method and the column names of the table and store it as a Pandas dataframe
        -> Return the Pandas dataframe

        --------------------
        Returns
        --------------------
        -> (pandas.core.frame.DataFrame): Returns the schema information of a table as a Pandas dataframe by passing the name of the schema and the table as a SQL query

        """
        query = get_table_schema_query(schema_name, table_name)
        if self.cursor:
            self.cursor.execute(query)
            df = pd.DataFrame(self.cursor.fetchall(), columns=[desc[0] for desc in self.cursor.description])
            return df
        return None
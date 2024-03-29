import pandas as pd
import streamlit as st

from src.database.logics import PostgresConnector
from src.dataframe.queries import get_numeric_tables_query, get_text_tables_query, get_date_tables_query


class Dataset:
    """
    --------------------
    Description
    --------------------
    -> Dataset (class): Class that manages a dataset loaded from Postgres

    --------------------
    Attributes
    --------------------
    -> schema_name (str): Name of the dataset schema (mandatory)
    -> table_name (str): Name of the dataset table (mandatory)
    -> db (PostgresConnector): Instantation of PostgresConnector class for handling Postgres connection (mandatory)
    -> df (pd.Dataframe): Pandas dataframe where the table content has been loaded (mandatory)
    -> n_rows (int): Number of rows of dataset (optional)
    -> n_cols (int): Number of columns of dataset (optional)
    -> n_duplicates (int): Number of duplicated rows of dataset (optional)
    -> n_missing (int): Number of missing values of dataset (optional)
    -> num_cols (list): List of columns of numerical type (optional)
    -> text_cols (list): List of columns of text type (optional)
    -> date_cols (list): List of columns of datetime type (optional)
    """
    def __init__(self, schema_name=None, table_name=None, db=None, df=pd.DataFrame()):
        self.schema_name = schema_name
        self.table_name = table_name
        self.db = db
        self.df = df
        self.n_rows = None
        self.n_cols = None
        self.n_duplicates = None
        self.n_missing = None
        self.num_cols = None
        self.text_cols = None
        self.date_cols = None

    def set_data(self):
        """
        --------------------
        Description
        --------------------
        set_data (method): Class method that computes all requested information from self.df to be displayed in the Overall section of Streamlit app

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        open connection and cursor to the database
        extract content of selected Postgres table and load into class attribute as pandas dataframe
        close cursor and connection to the database
        call class fucntions to compute table attributes after checking the dataframe is not empty

        --------------------
        Returns
        --------------------
        none

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.df = self.db.load_table(self.schema_name, self.table_name)
        self.db.close_cursor()
        self.db.close_connection()

        if (not self.is_df_none()):
            self.set_dimensions()
            self.set_duplicates()
            self.set_missing()
            self.set_numeric_columns()
            self.set_text_columns()
            self.set_date_columns()

    def is_df_none(self):
        """
        --------------------
        Description
        --------------------
        is_df_none (method): Class method that checks if self.df is empty or none

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        return boolean value indicating if the dataframe is empty

        --------------------
        Returns
        --------------------
        Boolean value

        """
        return self.df.empty

    def set_dimensions(self):
        """
        --------------------
        Description
        --------------------
        set_dimensions (method): Class method that computes the dimensions (number of columns and rows) of self.df and store them as attributes (self.n_rows, self.n_cols)

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the classtion

        --------------------
        Pseudo-Code
        --------------------
        save relevant dataframe shape into attributes representing number of columns and rows of the dataframe

        --------------------
        Returns
        --------------------
        none

        """
        self.n_rows = self.df.shape[0]
        self.n_cols = self.df.shape[1]

    def set_duplicates(self):
        """
        --------------------
        Description
        --------------------
        set_duplicates (method): Class method that computes the number of duplicated of self.df and store it as attribute (self.n_duplicates)

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        save the number of duplicated rows in the class's dataframe to the class attribute

        --------------------
        Returns
        --------------------
        none

        """
        self.n_duplicates = self.df.duplicated().sum()

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        set_missing (method): Class method that computes the number of missing values of self.df and store it as attribute (self.n_missing)

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        save the number of missing rows in the class's dataframe to corresponding class attribute

        --------------------
        Returns
        --------------------
        none

        """
        self.n_missing = self.df.isna().sum().sum()

    def set_numeric_columns(self):
        """
        --------------------
        Description
        --------------------
        set_numeric_columns (method): Class method that extract the list of numeric columns from a table using a SQL query (from get_numeric_tables_query()),
        store it as attribute (self.num_cols) and then convert the relevant columns of self.df accordingly.

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class


        --------------------
        Pseudo-Code
        --------------------
        open connection and cursor to the database
        using existing sql query to extract numeric columns of the Postgres table
        transform class's dataframe's columns based on extracted numeric columns after checking the dataframe is not empty
        close connection and cursor to the database
        --------------------
        Returns
        --------------------
        none

        """
        self.db.open_connection()
        self.db.open_cursor()
        result = self.db.run_query(get_numeric_tables_query(self.schema_name, self.table_name))
        if (not result.empty):
            self.num_cols = list(result[0])
            for column in self.num_cols:
                for col in self.df.columns:
                    if (col == column):
                        self.df[col] = pd.to_numeric(self.df[col])
        self.db.close_cursor()
        self.db.close_connection()

    def set_text_columns(self):
        """
        --------------------
        Description
        --------------------
        set_text_columns (method): Class method that extract the list of text columns from a table using a SQL query (from get_numeric_tables_query()),
        store it as attribute (self.text_cols) and then convert the relevant columns of self.df accordingly.

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class


        --------------------
        Pseudo-Code
        --------------------
        open connection and cursor to the database
        using existing sql query to extract text columns of the Postgres table
        transform class's dataframe's columns based on extracted text columns after checking the dataframe is not empty
        close connection and cursor to the database
        --------------------
        Returns
        --------------------
        none
        """
        self.db.open_connection()
        self.db.open_cursor()
        result = self.db.run_query(get_text_tables_query(self.schema_name, self.table_name))
        if (not result.empty):
            self.text_cols = list(result[0])
            for column in self.text_cols:
                for col in self.df.columns:
                    if (col == column):
                        self.df[col].apply(lambda v: str(v) if not pd.isnull(v) else None)
        self.db.close_cursor()
        self.db.close_connection()

    def set_date_columns(self):
        """
        --------------------
        Description
        --------------------
        set_date_columns (method): Class method that extract the list of datetime columns from a table using a SQL query (from get_numeric_tables_query()),
        store it as attribute (self.date_cols) and then convert the relevant columns of self.df accordingly.

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class


        --------------------
        Pseudo-Code
        --------------------
        open connection and cursor to the database
        using existing sql query to extract date columns of the Postgres table
        transform class's dataframe's columns based on extracted datte columns after checking the dataframe is not empty
        close connection and cursor to the database
        --------------------
        Returns
        --------------------
        none

        """
        self.db.open_connection()
        self.db.open_cursor()
        result = self.db.run_query(get_date_tables_query(self.schema_name, self.table_name))
        if (not result.empty):
            self.date_cols = list(result[0])
            for column in self.date_cols:
                for col in self.df.columns:
                    if (col == column):
                        self.df[col] = pd.to_datetime(self.df[col], utc=True)
        self.db.close_cursor()
        self.db.close_connection()

    def get_head(self, n=5):
        """
        --------------------
        Description
        --------------------
        get_head (method): Class method that computes the first rows of self.df according to the provided number of rows specified as parameter (default: 5)

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class
        n(int): control the number of rows to be displayed

        --------------------
        Pseudo-Code
        --------------------
        show the top n rows of the class's dataframe

        --------------------
        Returns
        --------------------
        pandas dataframe

        """
        return self.df.head(n)

    def get_tail(self, n=5):
        """
        --------------------
        Description
        --------------------
        get_tail (method): Class method that computes the last rows of self.df according to the provided number of rows specified as parameter (default: 5)

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class
        n(int): control the number of rows to be displayed

        --------------------
        Pseudo-Code
        --------------------
        show the bottom n rows of the class's dataframe

        --------------------
        Returns
        --------------------
        pandas dataframe

        """
        return self.df.tail(n)

    def get_sample(self, n=5):
        """
        --------------------
        Description
        --------------------
        get_sample (method): Class method that computes a random sample of rows of self.df according to the provided number of rows specified as parameter (default: 5)

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class
        n(int): control the number of rows to be displayed

        --------------------
        Pseudo-Code
        --------------------
        show random n rows of the class's dataframe

        --------------------
        Returns
        --------------------
        pandas dataframe

        """
        return self.df.sample(n)

    def get_summary_df(self):
        """
        --------------------
        Description
        --------------------
        get_summary_df (method): Class method that formats all requested information from self.df to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        setup an empty pandas DataFrame
        set specified columns and values from computed attributes of the class's dataframe

        --------------------
        Returns
        --------------------
        pandas dataframe

        """
        summary = pd.DataFrame()
        summary['Description'] = ['Name of Table', 'Number of Rows', 'Number of Columns', 'Number of Duplicated Rows', 'Number of Rows with Missing Values']
        summary['Value'] = [self.table_name, self.n_rows, self.n_cols, self.n_duplicates, self.n_missing]
        return summary

    def get_schema(self):
        """
        --------------------
        Description
        --------------------
        get_schema (method): Class method that formats table schema information for selected Postgres table

        --------------------
        Parameters
        --------------------
        self: Reference to the current instance of the class


        --------------------
        Pseudo-Code
        --------------------
        open connection and cursor to the database
        get table schema information for classls selected table from existing sql query
        close connection and cursor to the database

        --------------------
        Returns
        --------------------
        pandas dataframe

        """
        self.db.open_connection()
        self.db.open_cursor()
        schema = self.db.get_table_schema(self.schema_name, self.table_name)
        self.db.close_cursor()
        self.db.close_connection()
        return schema

import streamlit as st
import pandas as pd
import altair as alt

from src.database.logics import PostgresConnector
from src.serie_text.queries import get_missing_query, get_mode_query, get_alpha_query

class TextColumn:
    """
    --------------------
    Description
    --------------------
    -> TextColumn (class): Class that manages a column loaded from Postgres

    --------------------
    Attributes
    --------------------
    -> schema_name (str): Name of the dataset schema (mandatory)
    -> table_name (str): Name of the dataset table (mandatory)
    -> col_name (str): Name of the column (mandatory)
    -> db (PostgresConnector): Instantation of PostgresConnector class for handling Postgres connection (mandatory)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (mandatory)
    -> n_unique (int): Number of unique value of a serie (optional)
    -> n_missing (int): Number of missing values of a serie (optional)
    -> n_empty (int): Number of times a serie has empty value (optional)
    -> n_mode (int): Mode value of a serie (optional)
    -> n_space (int): Number of times a serie has only space characters (optional)
    -> n_lower (int): Number of times a serie has only lowercase characters (optional)
    -> n_upper (int): Number of times a serie has only uppercase characters (optional)
    -> n_alpha (int): Number of times a serie has only alphabetical characters (optional)
    -> n_digit (int): Number of times a serie has only digit characters (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Datframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, schema_name=None, table_name=None, col_name=None, db=None, serie=None):
        self.schema_name = schema_name
        self.table_name = table_name
        self.col_name = col_name
        self.db = PostgresConnector()
        self.serie = pd.Series()
        self.n_unique = None
        self.n_empty = None
        self.n_missing = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = None
        self.frequent = None
    
    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information from self.serie to be displayed in the Text section of Streamlit app 
        """

        self.db.open_connection()
        self.db.open_cursor()
        self.serie = self.db.run_query(get_column_query(self.schema_name, self.table_name, self.col_name))[0].squeeze()
        self.db.close_cursor()
        self.db.close_connection()

        self.is_serie_none()
        self.set_unique()
        self.set_missing()
        self.set_empty()
        self.set_mode()
        self.set_whitespace()
        self.set_lowercase()
        self.set_uppercase()
        self.set_alphabet()
        self.set_digit()
        self.set_barchart()
        self.set_frequent()
        self.get_summary_df()
      
    def is_serie_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_serie_none (method): Class method that checks if self.serie is empty or none 

        """
        return (self.serie == None) | self.serie.empty

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a serie

        """
        self.n_unique = self.serie.nunique()

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie using a SQL query (get_missing_query())

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_missing = self.db.run_query(get_missing_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()


    def set_empty(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty (method): Class method that computes the number of times a serie has empty value

        """
        self.n_empty = self.serie.empty()

    def set_mode(self):
        """
        --------------------
        Description
        --------------------
        -> set_mode (method): Class method that computes the mode value of a serie using a SQL query (get_mode_query())

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_mode = self.db.run_query(get_mode_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()


    def set_whitespace(self):
        """
        --------------------
        Description
        --------------------
        -> set_whitespace (method): Class method that computes the number of times a serie has only space characters

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_whitespace = self.db.run_query(get_whitespace(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()

    def set_lowercase(self):
        """
        --------------------
        Description
        --------------------
        -> set_lowercase (method): Class method that computes the number of times a serie has only lowercase characters

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_lowercase = self.db.run_query(get_lowercase(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()

    def set_uppercase(self):
        """
        --------------------
        Description
        --------------------
        -> set_uppercase (method): Class method that computes the number of times a serie has only uppercase characters

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_uppercase = self.db.run_query(get_uppercase(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()
    
    def set_alphabet(self):
        """
        --------------------
        Description
        --------------------
        -> set_alphabet (method): Class method that computes the number of times a serie has only alphabetical characters using a SQL query (get_alpha_query())

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_alphabet = self.db.run_query(get_alpha_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()

    def set_digit(self):
        """
        --------------------
        Description
        --------------------
        -> set_digit (method): Class method that computes the number of times a serie has only digit characters

        """
        self.db.open_connection()
        self.db.open_cursor()
        self.n_digit = self.db.run_query(get_digit(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        self.db.close_connection()

    def set_barchart(self):  
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a serie

        """
        self.db.open_connection()
        self.db.open_cursor()
        counts = self.serie.value_counts().to_frame()
        value_c = pd.DataFrame()
        value_c['value'] = pd.to_datetime(counts.index)
        value_c['occurrence'] = counts.values
        self.barchart = alt.Chart(value_c).mark_bar().encode(x='value', y='occurrence')
        self.db.close_cursor()
        self.db.close_connection()
      
    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie

        """
        self.db.open_connection()
        self.db.open_cursor()
        counts = self.serie.value_counts().to_frame()
        counts_perc = round(self.serie.value_counts(normalize=True).to_frame(), 4)
        value_c = pd.DataFrame()
        value_c['value'] = pd.to_datetime(counts.index)
        value_c['occurrence'] = counts.values
        value_c['percentage'] = counts_perc.values
        self.frequent = value_c
        self.db.close_cursor()
        self.db.close_connection()

    def get_summary_df(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary_df (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        """

        summary = pd.DataFrame()
        summary['Description'] = ['Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Empty values', 'Number of Whitespaces', 'Mode of Values','Number of lowercase', 'Number of uppercase', 'Number of Series with alphabetical characters', 'Number of Series with digit characters']
        summary['Value'] = [self.n_unique, self.n_missing, self.n_empty, self.n_whitespace, self.n_mode, self.n_lowercase, self.n_uppercase, self.n_alphabet, self.n_digit]
        return summary
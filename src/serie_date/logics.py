import streamlit as st
import pandas as pd
import altair as alt

from src.database.logics import PostgresConnector
from src.serie_date.queries import get_column_query, get_min_date_query, get_max_date_query, get_weekend_count_query, get_weekday_count_query, get_future_count_query, get_1900_count_query, get_1970_count_query

class DateColumn:
    """
    --------------------
    Description
    --------------------
    -> DateColumn (class): Class that manages a column loaded from Postgres

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
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> n_weekend (int): Number of times a serie has dates falling during weekend (optional)
    -> n_weekday (int): Number of times a serie has dates not falling during weekend (optional)
    -> n_future (int): Number of times a serie has dates falling in the future (optional)
    -> n_empty_1900 (int): Number of times a serie has dates equal to '1900-01-01' (optional)
    -> n_empty_1970 (int): Number of times a serie has dates equal to '1970-01-01' (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Dataframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, schema_name=None, table_name=None, col_name=None, db=None, serie=None):
        self.schema_name = schema_name
        self.table_name = table_name
        self.col_name = col_name
        self.db = PostgresConnector()
        self.serie = pd.Series()
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = None
        self.frequent = None

    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information from self.serie to be displayed in the Date section of Streamlit app

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.serie = self.db.run_query(get_column_query(self.schema_name, self.table_name, self.col_name))[0].squeeze()
        self.db.close_cursor()
        # self.db.close_connection()

        self.is_serie_none()
        self.set_unique()
        self.set_missing()
        self.set_min()
        self.set_max()
        self.set_weekend()
        self.set_weekday()
        self.set_future()
        self.set_empty_1900()
        self.set_empty_1970()
        self.set_barchart()
        self.set_frequent()

    def is_serie_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_serie_none (method): Class method that checks if self.serie is empty or none

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
        return (self.serie == None) | self.serie.empty

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a serie

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
        self.n_unique = self.serie.nunique()

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie

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
        self.n_missing = self.serie.isna().sum()

    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie using a SQL query (get_min_date_query())

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.col_min = self.db.run_query(get_min_date_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the maximum value of a serie

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.col_max = self.db.run_query(get_max_date_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_weekend(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekend (method): Class method that computes the number of times a serie has dates falling during weekend using a SQL query (get_weekend_count_query())

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.n_weekend = self.db.run_query(get_weekend_count_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_weekday(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekday (method): Class method that computes the number of times a serie has dates not falling during weekend

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.n_weekday = self.db.run_query(get_weekday_count_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_future(self):
        """
        --------------------
        Description
        --------------------
        -> set_future (method): Class method that computes the number of times a serie has dates falling in the future

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.n_future = self.db.run_query(get_future_count_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_empty_1900(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1900 (method): Class method that computes the number of times a serie has dates equal to '1900-01-01' using a SQL query (get_1900_count_query())

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.n_empty_1900 = self.db.run_query(get_1900_count_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_empty_1970(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1970 (method): Class method that computes the number of times a serie has dates equal to '1970-01-01'

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
        # self.db.open_connection()
        self.db.open_cursor()
        self.n_empty_1970 = self.db.run_query(get_1970_count_query(self.schema_name, self.table_name, self.col_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_barchart(self):
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a serie

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
        # self.db.open_connection()
        self.db.open_cursor()
        counts = self.serie.value_counts().to_frame()
        value_c = pd.DataFrame()
        value_c['value'] = pd.to_datetime(counts.index)
        value_c['occurrence'] = counts.values
        self.barchart = alt.Chart(value_c).mark_bar().encode(x='value', y='occurrence')
        self.db.close_cursor()
        # self.db.close_connection()


    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie

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
        self.db.open_connection()
        self.db.open_cursor()
        counts = self.serie.value_counts().to_frame().head(end)
        counts_perc = round(self.serie.value_counts(normalize=True).to_frame().head(end), 4)
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
        summary = pd.DataFrame()
        summary['Description'] = ['Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Weekend Dates', 'Number of Weekday Dates', 'Number of Dates in Future', 'Number of Rows with 1900-01-01', 'Number of Rows with 1970-01-01', 'Minimum Value', 'Maximum Value']
        summary['Value'] = [self.n_unique, self.n_missing, self.n_weekend, self.n_weekday, self.n_future, self.n_empty_1900, self.n_empty_1970, self.col_min, self.col_max]
        return summary

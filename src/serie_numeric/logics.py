import streamlit as st
import pandas as pd
import altair as alt

from src.database.logics import PostgresConnector
from src.serie_numeric.queries import get_negative_number_query, get_std_query, get_unique_query
from src.serie_date.queries import get_column_query


class NumericColumn:
    """
    --------------------
    Description
    --------------------
    -> NumericColumn (class): Class that manages a column loaded from Postgres

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
    -> col_mean (int): Average value of a serie (optional)
    -> col_std (int): Standard deviation value of a serie (optional)
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> col_median (int): Median value of a serie (optional)
    -> n_zeros (int): Number of times a serie has values equal to 0 (optional)
    -> n_negatives (int): Number of times a serie has negative values (optional)
    -> histogram (int): Altair histogram displaying the count for each bin value of a serie (optional)
    -> frequent (int): Datframe containing the most frequest value of a serie (optional)

    """    
    def __init__(self, schema_name=None, table_name=None, column_name=None, db=PostgresConnector(), ds=pd.Series()):
        self.schema_name = schema_name
        self.table_name = table_name
        self.column_name = column_name
        self.db = db
        self.serie = ds
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = None
        self.frequent = None

    def set_data(self):
        """
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that computes all requested information from self.serie to be displayed in the Numeric section of Streamlit app 

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> open connection and cursor to the database
        -> extract content of selected Postgres table's column and load into class attribute as pandas series
        -> close cursor and connection to the database

        --------------------
        Returns
        --------------------
        -> None

        """
        # self.db.open_connection()
        self.db.open_cursor()
        df = self.db.run_query(get_column_query(self.schema_name, self.table_name, self.column_name))
        if not df.empty:
            self.serie = df[0].squeeze()
        self.db.close_cursor()
        # self.db.close_connection()

        if (not self.is_serie_none()):
            self.set_unique()
            self.set_missing()
            self.set_mean()
            self.set_std()
            self.set_min()
            self.set_max()
            self.set_median()
            self.set_zeros()
            self.set_negatives()
            self.set_histogram()
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
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Returns a boolean value indicating whether the Pandas series is empty or none

        --------------------
        Returns
        --------------------
        -> (boolean): True if series is empty

        """
        return self.serie.empty

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a column using a SQL query (get_unique_query())

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Open a connection and a cursor for the passed database
        -> Retreive the sql query to extract the number of unique values of the selected column of the Postgres table
        -> Pass the result to corresponding class attribute

        --------------------
        Returns
        --------------------
        -> None

        """
        # self.db.open_connection() 
        self.db.open_cursor()
        self.n_unique = self.db.run_query(get_unique_query(self.schema_name, self.table_name, self.column_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Use Pandas series function to set the number of missing values in the selected column of the Postgres table

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_missing = self.serie.isna().sum()

    def set_zeros(self):
        """
        --------------------
        Description
        --------------------
        -> set_zeros (method): Class method that computes the number of times a serie has values equal to 0

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Use Pandas series function to set the number of zero values in the selected column of the Postgres table

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_zeros = self.serie.isin([0]).sum()

    def set_negatives(self):
        """
        --------------------
        Description
        --------------------
        -> set_negatives (method): Class method that computes the number of times a serie has negative values using a SQL query (get_negative_number_query())

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Open a connection and a cursor for the passed database
        -> Retreive the sql query to extract the number of negative values of the selected column of the Postgres table
        -> Pass the result to corresponding class attribute

        --------------------
        Returns
        --------------------
        -> None

        """
        # self.db.open_connection() 
        self.db.open_cursor()
        self.n_negatives = self.db.run_query(get_negative_number_query(self.schema_name, self.table_name, self.column_name))[0][0]
        self.db.close_cursor()
        # self.db.close_connection()
        
    def set_mean(self):
        """
        --------------------
        Description
        --------------------
        -> set_mean (method): Class method that computes the average value of a serie

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Use Pandas series function to set the mean of the values in the selected column of the Postgres table

        --------------------
        Returns
        --------------------
        -> None

        """
        self.col_mean = self.serie.mean() 

    def set_std(self):
        """
        --------------------
        Description
        --------------------
        -> set_std (method): Class method that computes the standard deviation value of a serie using a SQL query (get_std_query)

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Open a connection and a cursor for the passed database
        -> Retreive the sql query to extract the standard deviation of the values of the selected column of the Postgres table
        -> Pass the result to corresponding class attribute

        --------------------
        Returns
        --------------------
        -> None

        """
        # self.db.open_connection() 
        self.db.open_cursor()
        self.col_std = self.db.run_query(get_std_query(self.schema_name, self.table_name, self.column_name))[0][0]
        # self.col_std = self.serie.std()
        self.db.close_cursor()
        # self.db.close_connection()
    
    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Use Pandas series function to set the minimum of the values in the selected column of the Postgres table

        --------------------
        Returns
        --------------------
        -> None

        """
        self.col_min = self.serie.min()

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the maximum value of a serie

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Use Pandas series function to set the maximum of the values in the selected column of the Postgres table

        --------------------
        Returns
        --------------------
        -> None

        """
        self.col_max = self.serie.max()

    def set_median(self):
        """
        --------------------
        Description
        --------------------
        -> set_median (method): Class method that computes the median value of a serie

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Use Pandas series function to set the median of the values in the selected column of the Postgres table

        --------------------
        Returns
        --------------------
        -> None

        """
        self.col_median = self.serie.median()

    def set_histogram(self):
        """
        --------------------
        Description
        --------------------
        -> set_histogram (method): Class method that computes the Altair histogram displaying the count for each bin value of a serie

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Open a database connection and cursor 
        -> Retreive the values counts from the Pandas series and convert to a Pandas dataframe
        -> Create a Pandas dataframe and load values and value count
        -> Create an Altair barchart using the dataframe
        -> Store barchart in the corresponding class attribute
        -> Close the cursor and connection to the database

        --------------------
        Returns
        --------------------
        -> None

        """
        # self.db.open_connection()
        self.db.open_cursor()
        counts = self.serie.value_counts().to_frame()
        value_count = pd.DataFrame()
        value_count['id'] = pd.to_numeric(counts.index)
        value_count['Count of Records'] = counts.values
        self.histogram = alt.Chart(value_count).mark_bar().encode(alt.X("id", bin=alt.Bin(maxbins=50)), y='Count of Records').interactive()
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
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Open a database connection and cursor 
        -> Retreive the top 20 values occurences from the Pandas series and convert to a Pandas dataframe
        -> Calculate the percentages and retreive the top 20 percentage values from the Pandas series and convert to a Pandas dataframe
        -> Create a Pandas dataframe and load values, occurences and percentages
        -> Store dataframe in the corresponding class attribute
        -> Close the cursor and connection to the database

        --------------------
        Returns
        --------------------
        -> None

        """
        # self.db.open_connection()
        self.db.open_cursor()
        counts = self.serie.value_counts().to_frame().head(end)
        percentages = round(self.serie.value_counts(normalize=True).to_frame().head(end), 4)
        value_count = pd.DataFrame()
        value_count['value'] = pd.to_numeric(counts.index)
        value_count['occurrence'] = counts.values
        value_count['percentage'] = percentages.values
        self.frequent = value_count
        self.db.close_cursor()
        # self.db.close_connection()

    def get_summary_df(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary_df (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        -> self: Reference to the current instance of the class

        --------------------
        Pseudo-Code
        --------------------
        -> Create an empty Pandas datframe
        -> Add row descriptions and values of class attributes

        --------------------
        Returns
        --------------------
        -> summary(Pandas.dataframe): A dataset containing two columns which can be used in a streamlit table function  

        """
        summary = pd.DataFrame()
        summary['Description'] = ['Number of Unique Values', 
                                  'Number of Rows with Missing Values', 
                                  'Number of Rows with 0', 
                                  'Number of Rows with Negative Values', 
                                  'Average Value', 
                                  'Standard Deviation Value', 
                                  'Minimum Value', 
                                  'Maximum Value', 
                                  'Median Value',]
        summary['Value'] = ['{:,.0f}'.format(self.n_unique), 
                            '{:,.0f}'.format(self.n_missing), 
                            '{:,.0f}'.format(self.n_zeros), 
                            '{:,.0f}'.format(self.n_negatives), 
                            '{:,.3f}'.format(self.col_mean),
                            '{:,.3f}'.format(self.col_std), 
                            '{:,.3f}'.format(self.col_min), 
                            '{:,.3f}'.format(self.col_max), 
                            '{:,.3f}'.format(self.col_median)]
        return summary
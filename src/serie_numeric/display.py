import streamlit as st
import pandas as pd

from src.dataframe.logics import Dataset
from src.serie_numeric.logics import NumericColumn

def display_numerics():
    """
    --------------------
    Description
    --------------------
    -> display_numerics (function): Function that displays all the relevant information for every numerical column of a table

    --------------------
    Parameters
    --------------------
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Define the required database information from the streamlit session state
    -> Retreive a list of all tables containing numeric fields
    -> Cycle through table list to display table name in streamlit expander container and display numerical information

    --------------------
    Returns
    --------------------
    -> None

    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    Data_all = Dataset(schema_name, table_name, db=st.session_state['db'])
    Data_all.set_data()
    if (Data_all.num_cols != None):
        for idx, column in enumerate(Data_all.num_cols):
            with st.expander(f"{idx+1}. column: {column}"):
                display_numeric(column, idx)

def display_numeric(col_name, i):
    """
    --------------------
    Description
    --------------------
    -> display_numeric (function): Function that instantiates a NumericColumn class from a dataframe column and displays all the relevant information for a single numerical column of a table

    --------------------
    Parameters
    --------------------
    -> col_name(str): name of processed column
    -> i(int): index of processed column

    --------------------
    Pseudo-Code
    --------------------
    -> Retreive required database information from the streamlit session state
    -> Instantiate a NumericColumn object and set its values
    -> Display an information table for the column parameter, an interctive bar chart of the numeric count and an interactive chart of the frequency of the top 20 numerical elements

    --------------------
    Returns
    --------------------
    -> None

    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    db = st.session_state['db']
    numeric_data = NumericColumn(schema_name, table_name, col_name, db)
    numeric_data.set_data()

    if not numeric_data.is_serie_none():
        st.table(data=numeric_data.get_summary_df())
        st.subheader('Bar Chart')
        st.altair_chart(numeric_data.histogram, use_container_width=True)
        st.subheader('Most Frequent Values')
        st.dataframe(data=numeric_data.frequent)
    else:
        st.write('No data in table')
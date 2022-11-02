import streamlit as st

from src.dataframe.logics import Dataset
from src.serie_date.logics import DateColumn


def display_dates():
    """
    --------------------
    Description
    --------------------
    display_dates (function): Function that displays all the relevant information for every datetime column of a table

    --------------------
    Parameters
    --------------------
    none

    --------------------
    Pseudo-Code
    --------------------
    get required information from session state
    get table data from instantiated Dataset class
    extract date columns from table data, display column name and call display_date() frunction

    --------------------
    Returns
    --------------------
    none

    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    Data_all = Dataset(schema_name, table_name, db=st.session_state['db'])
    Data_all.set_data()
    if (Data_all.date_cols != None):
        date_cols = Data_all.date_cols
        for idx, column in enumerate(date_cols):
            with st.expander(f"{idx+1}. column: {column}"):
                display_date(column, idx)


def display_date(col_name, i):
    """
    --------------------
    Description
    --------------------
    display_date (function): Function that instantiates a DateColumn class from a dataframe column and displays all the relevant information for a single datetime column of a table

    --------------------
    Parameters
    --------------------
    col_name(str): name of selected column
    i(int): index of selected column

    --------------------
    Pseudo-Code
    --------------------
    get required information from session state
    instantiats DateColumn class with acquired inforamtion and compute required inforamtion
    display barchart and frequent values from the instantiated class with streamlit

    --------------------
    Returns
    --------------------
    none 
    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    Data = DateColumn(schema_name, table_name, col_name, db=st.session_state['db'])
    Data.set_data()
    st.table(data=Data.get_summary_df())
    st.subheader('Bar Chart')
    st.altair_chart(Data.barchart, use_container_width=True)
    st.subheader('Most Frequent Values')
    st.dataframe(data=Data.frequent)

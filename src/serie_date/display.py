import streamlit as st

from src.dataframe.logics import Dataset
from src.serie_date.logics import DateColumn


def display_dates():
    """
    --------------------
    Description
    --------------------
    -> display_dates (function): Function that displays all the relevant information for every datetime column of a table

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
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    Data_all = Dataset(schema_name, table_name, db=st.session_state['db'])
    Data_all.set_data()
    date_cols = Data_all.date_cols
    for idx, column in enumerate(date_cols):
        with st.expander(f"{idx+1}. column: {column}"):
            display_date(schema_name, table_name, column)

def display_date(col_name, i):
    """
    --------------------
    Description
    --------------------
    -> display_date (function): Function that instantiates a DateColumn class from a dataframe column and displays all the relevant information for a single datetime column of a table

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
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    Data = DateColumn(schema_name, table_name, col_name)
    Data.set_data()
    st.table(data=Data.get_summary_df())
    st.subheader('Bar Chart')
    st.altair_chart(Data.barchart, use_container_width=True)
    st.subheader('Most Frequent Values')
    st.dataframe(data=Data.frequent)

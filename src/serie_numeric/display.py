import streamlit as st
import pandas as pd

from src.serie_numeric.logics import NumericColumn
from src.dataframe.queries import get_numeric_tables_query

# from src.config import set_session_states, display_session_state

def display_numerics():
    """
    --------------------
    Description
    --------------------
    -> display_numerics (function): Function that displays all the relevant information for every numerical column of a table

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
    db = st.session_state['db']
    db.open_cursor()
    columns = db.run_query(get_numeric_tables_query(schema_name, table_name))[0]
    db.close_cursor()
    for idx, column in enumerate(columns):
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
    db = st.session_state['db']
    NC = NumericColumn(schema_name, table_name, col_name, db)
    NC.set_data()

    if not NC.is_serie_none():
        st.table(data=NC.get_summary_df(col_name))
        ### test code
        st.altair_chart(NC.histogram, use_container_width=True)
        ### end test code
    
    else:
        st.write('No data in table')

    
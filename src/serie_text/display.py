import streamlit as st

from src.serie_text.logics import TextColumn
from src.dataframe.logics import Dataset
from src.dataframe.queries import get_text_tables_query

def display_texts():
    """
    --------------------
    Description
    --------------------
    -> display_texts (function): Function that displays all the relevant information for every text column of a table

    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    db = st.session_state['db']
    Data_all = Dataset(schema_name, table_name, db=db)
    Data_all.set_data()
    text_cols = Data_all.text_cols
    if text_cols is not None:
        for idx, column in enumerate(text_cols):
            with st.expander(f"{idx+1}. column: {column}"):
                display_text(column, idx)


def display_text(col_name, i):
    """
    --------------------
    Description
    --------------------
    -> display_text (function): Function that instantiates a TextColumn class from a dataframe column and displays all the relevant information for a single text column of a table


    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    db = st.session_state['db']
    Data = TextColumn(schema_name, table_name, col_name, db=db)
    Data.set_data()
    st.table(data=Data.get_summary_df())
    st.subheader('Bar Chart')
    st.altair_chart(Data.barchart, use_container_width=True)
    st.subheader('Most Frequent Values')
    st.dataframe(data=Data.frequent)
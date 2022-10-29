import streamlit as st
import os
import pandas as pd
from src.database.logics import PostgresConnector
from src.dataframe.display import read_data
from src.config import set_session_states, display_session_state

def display_db_connection_menu():
    """
    --------------------
    Description
    --------------------
    -> display_db_connection_menu (function): Function that displays the menu for connecting to a database and triggers the database connection

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
    st.header("Database Connection Details")
    db_user = st.text_input("Username:", value=os.getenv('POSTGRES_USER'))
    db_password = st.text_input("Password:", type="password", value=os.getenv('POSTGRES_PASSWORD'))
    db_host = st.text_input("Database Host:", value=os.getenv('POSTGRES_HOST'))
    db_name = st.text_input("Database Name:", value=os.getenv('POSTGRES_DB'))
    db_port = st.text_input("Database Port:", value=os.getenv('POSTGRES_PORT'))
    dict_args = {
        'keys': ['db_host', 'db_name', 'db_port', 'db_user', 'db_pass'],
        'value': [db_host, db_name, db_port, db_user, db_password]
    }
    if st.button("Connect", on_click=set_session_states, kwargs=dict_args):
        connect_db()

def connect_db():
    """
    --------------------
    Description
    --------------------
    -> connect_db (function): Function that connects to a database and instantiate a PostgresConnector class accordingly

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
    #=> To be filled by student
    postgresConnector = PostgresConnector(database=st.session_state['db_name'], 
                                          user=st.session_state['db_user'], 
                                          password=st.session_state['db_pass'], 
                                          host=st.session_state['db_host'], 
                                          port=st.session_state['db_port'])
    conn_object = postgresConnector.open_connection()
    if conn_object is None:
        st.error(f"connection to server at \"{st.session_state['db_host']}\", port {st.session_state['db_port']} failed: FATAL: password authentication failed for user \"{st.session_state['db_user']}\"")
    elif conn_object.status == 1:
        st.success('Connection to database established', icon="ℹ️")
        set_session_states(['db_status', 'db'], [conn_object.status, postgresConnector])

def display_table_selection():
    """
    --------------------
    Description
    --------------------
    -> display_table_selection (function): Function that displays the selection box for selecting the table to be analysed and triggers the loading of data (read_data())

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
    st.session_state['db'].open_cursor()
    extract_list_tables_and_schemas = st.session_state['db'].list_tables()
    list_schemas = []
    list_tables = []
    for tuples in extract_list_tables_and_schemas:
        list_schemas.append(tuples[0])
        list_tables.append(tuples[1])
    selected_table = st.selectbox(label='Select a table name', options=list_tables)
    for tuples in extract_list_tables_and_schemas:
        if tuples[1] == selected_table:
            selected_schema = tuples[0]
    set_session_states(['schema_selected', 'table_selected'], [selected_schema, selected_table])
    st.session_state['db'].close_cursor()
    st.session_state['data'] = read_data()
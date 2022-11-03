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
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Create a header for the Database menu by calling the streamlit header function
    -> Generate a text input box for database user by calling the streamlit text_input function and set the default value to the value retrieved from the environment variable
    -> Generate a text input box for database password by calling the streamlit text_input function and set the default value to the value retrieved from the environment variable
    -> Generate a text input box for database host by calling the streamlit text_input function and set the default value to the value retrieved from the environment variable
    -> Generate a text input box for database name by calling the streamlit text_input function and set the default value to the value retrieved from the environment variable
    -> Generate a text input box for database port by calling the streamlit text_input function and set the default value to the value retrieved from the environment variable
    -> Create a dictionary with all the keys as the database user, password, host, name & port and set the values to their respective text inputs
    -> Create a Connect button by calling the streamlit button function and on click, set the session states of the database user, password, host, name & port
        -> If Connect button is clicked, call the connect_db() function

    --------------------
    Returns
    --------------------
    -> None

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
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Instantiate a PostgresConnector() class by passing the database name, user, password, host and port from the streamlit session states
    -> Open an active database connection by calling the open_connection() function
    -> If connection object returned from open_connection() function is None:
        -> Show an error message stating that the connection failed
    -> Else if the status of the connection is 1:
        -> Show a successful message stating that a database connection has been established
        -> Set the session states for database connection status and PostgresConnector object
    -> Close the active database connection by calling close_connection() function

    --------------------
    Returns
    --------------------
    -> None

    """
    postgresConnector = PostgresConnector(database=st.session_state['db_name'], 
                                          user=st.session_state['db_user'], 
                                          password=st.session_state['db_pass'], 
                                          host=st.session_state['db_host'], 
                                          port=st.session_state['db_port'])
    conn_object = postgresConnector.open_connection()
    if conn_object is None:
        st.error(f"connection to server at \"{st.session_state['db_host']}\", port {st.session_state['db_port']} failed: FATAL: password authentication failed for user \"{st.session_state['db_user']}\"")
        st.stop()
    elif conn_object.status == 1:
        st.success('Connection to database established', icon="ℹ️")
        set_session_states(['db_status', 'db'], [conn_object.status, postgresConnector])
    postgresConnector.close_connection()

def display_table_selection():
    """
    --------------------
    Description
    --------------------
    -> display_table_selection (function): Function that displays the selection box for selecting the table to be analysed and triggers the loading of data (read_data())

    --------------------
    Parameters
    --------------------
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Open an active database connection by calling the open_connection() function for the PostgresConnector object stored in streamlit session states
    -> Open an active cursor by calling the open_cursor() function for the PostgresConnector object stored in streamlit session states
    -> Retrieve the list of tables from the database by calling the list_tables() function
    -> Create a streamlit selectbox widget by passing the list of tables as the options for the selectbox
    -> Retrieve the selected table and from it retrieve the selected schema and table
    -> Set the streamlit session states for schema selected and table selected
    -> Close the active cursor
    -> Close the active database connection
    -> Call the read_data() function to retrieve the Dataset() object for the selected schema and table
    -> Set the session state for the Dataset() object

    --------------------
    Returns
    --------------------
    -> None
    """
    st.session_state['db'].open_connection()
    st.session_state['db'].open_cursor()
    list_schema_tables = st.session_state['db'].list_tables()
    selected_schema_table = st.selectbox(label='Select a table name', options=list_schema_tables)
    split_schema_table = selected_schema_table.split(".")
    selected_schema = split_schema_table[0]
    selected_table = split_schema_table[1]
    set_session_states(['schema_selected', 'table_selected'], [selected_schema, selected_table])
    st.session_state['db'].close_cursor()
    st.session_state['db'].close_connection()
    data = read_data()
    set_session_states(['data'], [data])

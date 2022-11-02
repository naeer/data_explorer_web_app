import streamlit as st

from src.dataframe.logics import Dataset

def read_data():
    """
    --------------------
    Description
    --------------------
    read_data (function): Function that loads the content of the Postgres table selected, extract its schema information and instantiate a Dataset class accordingly

    --------------------
    Parameters
    --------------------
    none

    --------------------
    Pseudo-Code
    --------------------
    using database connection status to get relevant information to instantiate a Dataset class
    get relevant data and informtiaon fo the Dataset class

    --------------------
    Returns
    --------------------
    instantiated Dataset class

    """
    schema_name = st.session_state['schema_selected']
    table_name = st.session_state['table_selected']
    db = st.session_state['db']
    Data = Dataset(schema_name, table_name, db=db)
    Data.set_data()
    return Data

def display_overall():
    """
    --------------------
    Description
    --------------------
    display_overall (function): Function that displays all the information on the Overall section of the streamlit app

    --------------------
    Parameters
    --------------------
    none

    --------------------
    Pseudo-Code
    --------------------
    get data from session session state
    display overll and schema information for selected table

    --------------------
    Returns
    --------------------
    none

    """
    Data = st.session_state['data']
    st.header('Overall Information')
    st.table(data=Data.get_summary_df())
    st.header('Table Schema')
    st.dataframe(data=Data.get_schema())

def display_dataframes():
    """
    --------------------
    Description
    --------------------
    display_dataframes (function): Function that displays all the information on the Explore section of the streamlit app

    --------------------
    Parameters
    --------------------
    none

    --------------------
    Pseudo-Code
    --------------------
    get data from session session state
    setup slider and radio selection with streamlit
    display relevant information of table data based on user choice

    --------------------
    Returns
    --------------------
    none

    """
    Data = st.session_state['data']
    nrow = st.slider('Select the number of rows to be displayed', 5, 50)
    logic = st.radio('Exploration Method', ('Head', 'Tail', 'Sample'))
    if logic == 'Head':
        st.header('Top Rows of Selected Table')
        st.write(Data.get_head(nrow))
    elif logic == 'Tail':
        st.header('Bottom Rows of Selected Table')
        st.write(Data.get_tail(nrow))
    else:
        st.header('Random Sample Rows of Selected Table')
        st.write(Data.get_sample(nrow))

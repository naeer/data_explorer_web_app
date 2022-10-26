import streamlit as st

from src.dataframe.logics import Dataset

def read_data(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> read_data (function): Function that loads the content of the Postgres table selected, extract its schema information and instantiate a Dataset class accordingly

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
    Data = Dataset(schema_name, table_name)
    Data.set_data()
    return Data

def display_overall(schema_name, table_name):
    """
    --------------------
    Description
    --------------------
    -> display_overall (function): Function that displays all the information on the Overall section of the streamlit app

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
    Data = read_data(schema_name, table_name)
    st.header('Overall Information')
    st.table(data=Data.get_summary_df())
    st.header('Table Schema')
    st.dataframe(data=Data.get_schema())

def display_dataframes():
    """
    --------------------
    Description
    --------------------
    -> display_dataframes (function): Function that displays all the information on the Explore section of the streamlit app

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
    Data = read_data(schema_name, table_name)
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

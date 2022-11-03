import streamlit as st

def set_app_config():
    """
    --------------------
    Description
    --------------------
    -> set_app_config (function): Function that sets the configuration of the Streamlit app

    --------------------
    Parameters
    --------------------
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Set the page config by passing the page title, icon, layout and the initial sidebar state

    --------------------
    Returns
    --------------------
    -> None

    """
    st.set_page_config(
        page_title="Database Explorer",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

def set_session_state(key, value):
    """
    --------------------
    Description
    --------------------
    -> set_session_state (function): Function that saves a key-value pair to the Streamlit session state

    --------------------
    Parameters
    --------------------
    -> key (str): Key of the session state
    -> value (str): Value to be stored for that key of the session state

    --------------------
    Pseudo-Code
    --------------------
    -> If the value for the key is None:
        -> If the key is not already in session state, that is it has not been initialized:
            -> Set the session state for that key to that value, which is None
    -> Else:
        -> Store the value to the key of the session state

    --------------------
    Returns
    --------------------
    -> None

    """
    if value is None:
        if key not in st.session_state:
            st.session_state[key] = value
    else:
        st.session_state[key] = value

def set_session_states(keys, value=None):
    """
    --------------------
    Description
    --------------------
    -> set_session_states (function): Function that saves a list of key-value pairs to the Streamlit session state using set_session_state() (default value: None)

    --------------------
    Parameters
    --------------------
    => To be filled by student
    -> name (type): description
    -> keys (list): List of keys of the session state
    -> value (list): By default, the value is None, otherwise a list of values corresponding to the list of keys

    --------------------
    Pseudo-Code
    --------------------
    -> If the value is None:
        -> For each key in keys:
            -> Store the value to the key of the session state
    -> Else:
        -> For all the keys:
            -> Store the key-value pairs in the session state

    --------------------
    Returns
    --------------------
    -> None

    """
    #=> To be filled by student
    if value is None:
        for key in keys:
            set_session_state(key, value)
    else:
        for i in range(len(keys)):
            set_session_state(key=keys[i], value=value[i])

def display_session_state():
    """
    --------------------
    Description
    --------------------
    -> display_session_state (function): Function that displays the current values of Streamlit session state

    --------------------
    Parameters
    --------------------
    -> None

    --------------------
    Pseudo-Code
    --------------------
    -> Display the session state by passing the session_state object to the streamlit write() function

    --------------------
    Returns
    --------------------
    -> None

    """
    st.write(st.session_state)




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
    st.write(st.session_state)




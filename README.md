# Data Explorer Web Application

## Authors
| Name | Student ID |
| --- | --- |
| Naeer Amin | 14203071 |
| Dan Hansen | 24718999 |
| Yifei Zhi | 13269410 |
| Todd Hunt | 00080349 |

## Description
This application was built to perform exploratory data analysis on the data stored in a database. The application performs exploratory data analysis on a per-table basis and shows summary statistics of each table column. It also gives an overview of the selected table by showing the table's number of rows and columns, among other things.
The application was containerised with the help of docker for ease of deployment and comprised two services, Streamlit and Postgres. The Streamlit app framework was used to build the application's web interface, and the Postgres instance was used to connect to the database and retrieve data. 

##### Challenges faced while building the application: 
- Ensuring that the Streamlit Session states are instantly reflected on the Session state debugger.
- Debugging the code was a challenge for the developers as it was not possible to step through code and monitor variables in Visual Studio Code due to the use of Streamlit objects. Visual Studio code could not recongnize function calls in the code if they are referenced through Streamlit Sessions state objects.

##### Future implementations:
- Move the Streamlit Session state debugger to a different page with the help of the streamlit-menu-option. This would mean that the users will only view the session states when they want to.
- Implement a new tab as part of the exploratory analysis that would show a scatter plot between two numeric columns selected by the user.

## How to Setup
- Clone the repository from Github using the following link: https://github.com/naeer/dsp_at3_project
- Run the following command to get the docker container up and running
    ```shell
    docker compose up -d
     ```
     This should download all the required services and packages and have the environment setup to run the web application


**Python version used:** Python 3.8.2

**Packages used:** 
- streamlit - 1.13.0
- pandas - 1.5.1
- psycopg2-binary - 2.9.5


## How to Run the Program
- Execute the following command (if not executed before):
    ```shell
    docker compose up -d
     ```
- Once the docker container is set up and running, open a web browser and paste the following link:
    - http://localhost:8501
- Once the application is successfully loaded, connect to the database by clicking on the Connect button and then explore the app
- To close the application, close the browser tab and stop the docker container by running the following command:
    ```shell
    docker compose down
     ```

## Project Structure
The project root directory contains the following folders and files:
- *app/*
    - *streamlit_app.py*: a streamlit script defining the interface of the web application
- *src/*
    - *config.py*: python script that sets the page level configurations of the streamlit app and also updates the streamlit session states
    - *database/*
        - *display.py*: python script that displays the database connection menu and allows the user to connect to the database
        - *logics.py*: python script that contains the class that initiates a connection to the Postgres database and subsequently carries out all the database operations
        - *queries.py*: python script that contains the sql queries for getting tables list, table data and table schema
    - *dataframe/*
        - *display.py*: python script that allows the application to give an overview of the selected table to the user
        - *logics.py*: python class that manages a dataset loaded from the Postgres database
        - *queries.py*: python script that contains sql queries to get numeric, date and text columns of a table
    - *serie_date/*
        - *display.py*: python script used to display all the relevant information about the date columns of a table
        - *logics.py*: python class that manages a column loaded from Postgres
        - *queries.py*: python script that contains all the sql queries relevant to the date columns of a table
    - *serie_numeric/*
        - *display.py*: python script used to display all the relevant information about the numeric columns of a table
        - *logics.py*: python class that manages a column loaded from Postgres
        - *queries.py*: python script that contains all the sql queries relevant to the numeric columns of a table
    - *serie_text/*
        - *display.py*: python script used to display all the relevant information about the text columns of a table
        - *logics.py*: python class that manages a column loaded from Postgres
        - *queries.py*: python script that contains all the sql queries relevant to the text columns of a table
    - *test/*
        - *test_database_queries.py*: python script for testing code from database/queries.py
        - *test_database_logics.py*: python script for testing code from database/logics.py
        - *test_dataframe_queries.py*: python script for testing code from dataframe/queries.py
        - *test_dataframe_logics.py*: python script for testing code from dataframe/logics.py
        - *test_serie_date_queries.py*: python script for testing code from serie_date/queries.py
        - *test_serie_date_logics.py*: python script for testing code from serie_date/logics.py
        - *test_serie_numeric_queries.py*: python script for testing code from serie_numeric/queries.py
        - *test_serie_numeric_logics.py*: python script for testing code from serie_numeric/logics.py
        - *test_serie_text_queries.py*: python script for testing code from serie_text/queries.py
        - *test_serie_text_logics.py*: python script for testing code from serie_text/logics.py
- *README.md*: a markdown file containing the details about the authors, a description of the project, a listing of all the files and instructions for running the code 
- *requirements.txt*: text file listing all the dependencies for this project
- *Dockerfile*: file containing the code to assemble a Python image and install all the required packages for this project
- *docker-compose.yml*: file containing the code to run a multi-container application consisting of two different services, namely Streamlit and Postgres

## Citations
1. (2022). Streamlit: A faster way to build and share data apps. Streamlit. https://docs.streamlit.io
2. (2021). Psycopg. psycopg. https://www.psycopg.org/docs/

import unittest
import pandas as pd
import unittest
import pandas as pd
import sqlalchemy as db

from src.database.logics import PostgresConnector

db_name = "postgres"
db_host = "localhost"
db_user = "postgres"
db_password = "9142"
db_port = "5432"

def setup_local():
    engine = db.create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    return engine

def get_data_local(engine, table_name):
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    ResultProxy = connection.execute(db.select([table]))
    ResultSet = ResultProxy.fetchall()
    return pd.DataFrame(ResultSet)

def run_sql_query(engine, sql_query):
    connection = engine.connect()
    resultSet = connection.execute(sql_query)
    return pd.DataFrame(resultSet)

class TestPostgresConnectorInstantiation(unittest.TestCase):
    """
    Class used for testing the instanciation of the PostgresConnector class from database/logics.py
    """
    def setUp(self) -> None:
        """
        Method used to initiate the attributes or parameters that are going to be used in the test cases
        """
        self.database = "db"
        self.user = "user"
        self.password = "password"
        self.host = "host"
        self.port = "port"
        self.excluded_schemas = ['information_schema', 'pg_catalog']

    def test_postgres_connector_instantiated_with_correct_attribute_values(self):
        """
        Test case to check that the PostgresConnector class is instantiated wit the correct attribute values
        """
        postgresConnector = PostgresConnector(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        self.assertEqual(postgresConnector.database, self.database)
        self.assertEqual(postgresConnector.user, self.user)
        self.assertEqual(postgresConnector.password, self.password)
        self.assertEqual(postgresConnector.host, self.host)
        self.assertEqual(postgresConnector.port, self.port)
        self.assertEqual(postgresConnector.excluded_schemas, self.excluded_schemas)

    def test_postgres_connector_do_not_get_instantiated_with_empty_or_none_values(self):
        """
        Test case to check that the PostgresConnector do not get instantiated with empty or none values for passing correct values
        """
        postgresConnector = PostgresConnector(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        self.assertNotEqual(postgresConnector.database, "")
        self.assertNotEqual(postgresConnector.user, "")
        self.assertNotEqual(postgresConnector.password, "")
        self.assertNotEqual(postgresConnector.host, "")
        self.assertNotEqual(postgresConnector.port, "")
        self.assertNotEqual(postgresConnector.excluded_schemas, "")
        self.assertNotEqual(postgresConnector.database, None)
        self.assertNotEqual(postgresConnector.user, None)
        self.assertNotEqual(postgresConnector.password, None)
        self.assertNotEqual(postgresConnector.host, None)
        self.assertNotEqual(postgresConnector.port, None)
        self.assertNotEqual(postgresConnector.excluded_schemas, None)

    def tearDown(self) -> None:
        """
        Method used to clean the parameters after they have been used while running the test cases
        """
        del self.database
        del self.user
        del self.password
        del self.host
        del self.port
        del self.excluded_schemas

class TestOpenConnection(unittest.TestCase):
    """
    Class used for testing the open_connection method of the PostgresConnector class from database/logics.py
    """
    def test_open_connection_function_successfully_opens_database_connection(self):
        """
        Test case to check that open connection function successfully opens a database connection
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        conn_object = postgresConnector.open_connection()
        self.assertEqual(1, conn_object.status)
        postgresConnector.close_connection()

    def test_open_connection_returns_none_if_connection_fails(self):
        """
        Test case to check that open connection function returns None if connection fails
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password='91422', host=db_host, port=db_port)
        conn_object = postgresConnector.open_connection()
        self.assertEqual(None, conn_object)

class TestCloseConnection(unittest.TestCase):
    """
    Class used for testing the close_connection method of the PostgresConnector class from database/logics.py
    """
    def test_close_connection_function_successfully_closes_database_connection(self):
        """
        Test case to check that close connection function successfully closes a database connection
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        conn_object = postgresConnector.open_connection()
        self.assertEqual(1, conn_object.status)
        postgresConnector.close_connection()
        self.assertEqual(1, conn_object.closed)

    def test_close_connection_function_does_not_throw_error_if_connection_none(self):
        """
        Test case to check that close connection function does not throw error if connection does not exist
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password='91422', host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.close_connection()

class TestOpenCursor(unittest.TestCase):
    """
    Class used for testing the open_cursor method of the PostgresConnector class from database/logics.py
    """
    def test_open_cursor_function_successfully_opens_database_cursor(self):
        """
        Test case to check that open cursor function successfully opens database cursor
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        conn_object = postgresConnector.open_connection()
        postgresConnector.open_cursor()
        self.assertEqual(0, postgresConnector.cursor.closed)
        postgresConnector.close_cursor()
        postgresConnector.close_connection()

    def test_open_cursor_function_does_not_throw_error_if_connection_none(self):
        """
        Test case to check that open cursor function does not throw error if connection does not exist
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password='91422', host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()

class TestCloseCursor(unittest.TestCase):
    """
    Class used for testing the close_cursor method of the PostgresConnector class from database/logics.py
    """
    def test_close_cursor_function_successfully_opens_database_cursor(self):
        """
        Test case to check that close cursor function successfully closes database cursor
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        self.assertEqual(0, postgresConnector.cursor.closed)
        postgresConnector.close_cursor()
        self.assertEqual(1, postgresConnector.cursor.closed)
        postgresConnector.close_connection()

    def test_close_cursor_function_does_not_throw_error_if_cursor_none(self):
        """
        Test case to check that close cursor function does not throw error if cursor does not exist
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password='91422', host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        postgresConnector.close_cursor()

class TestRunQuery(unittest.TestCase):
    """
    Class used for testing the run_query method of the PostgresConnector class from database/logics.py
    """
    def test_run_query_function_returns_correct_values(self):
        """
        Test case to check that the run_query function returns correct values
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        engine = setup_local()
        df = run_sql_query(engine=engine, sql_query="Select * from employees;")
        df_db = postgresConnector.run_query("Select * from employees;")
        self.assertTrue(df.values.all() == df_db.values.all())
        postgresConnector.close_cursor()
        postgresConnector.close_connection()

    def test_run_query_function_returns_None_for_empty_or_none_query(self):
        """
        Test case to check that run_query function returns None for empty or None query
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password=db_password, host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        result = postgresConnector.run_query(sql_query="")
        self.assertIsNone(result)
        result = postgresConnector.run_query(sql_query=None)
        self.assertIsNone(result)
        postgresConnector.close_cursor()
        postgresConnector.close_connection()

    def test_run_query_function_returns_None_for_no_database_connection(self):
        """
        Test case to check that run_query function returns None for no database connection
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password=db_password, host=db_host, port=db_port)
        result = postgresConnector.run_query(sql_query="Select * from employees;")
        self.assertIsNone(result)

class TestListTables(unittest.TestCase):
    """
    Class used for testing the list_tables method of the PostgresConnector class from database/logics.py
    """
    def test_list_tables_function_returns_correct_list(self):
        """
        Test case to check that the list_tables function returns the correct list of tables
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        engine = setup_local()
        df = run_sql_query(engine=engine, sql_query="SELECT table_schema || '.' || table_name AS table_name FROM information_schema.tables;")
        list_tables_query_local = df['table_name']
        list_tables_local = []
        for elements in list_tables_query_local:
            result = elements.split(".")
            if result[0] not in ['information_schema', 'pg_catalog']:
                list_tables_local.append(elements)
        result = postgresConnector.list_tables()
        self.assertEqual(list_tables_local, result)
        postgresConnector.close_cursor()
        postgresConnector.close_connection()

    def test_list_tables_function_returns_None_for_no_database_connection(self):
        """
        Test case to check that run_query function returns None for no database connection
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password=db_password, host=db_host, port=db_port)
        result = postgresConnector.list_tables()
        self.assertIsNone(result)

class TestLoadTable(unittest.TestCase):
    """
    Class used for testing the load_table method of the PostgresConnector class from database/logics.py
    """
    def test_load_table_function_returns_correct_content_of_the_table(self):
        """
        Test case to check that the list_tables function returns the correct list of tables
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        schema_name = "public"
        table_name = "employees"
        engine = setup_local()
        df_local = run_sql_query(engine=engine, sql_query=f"SELECT * FROM {schema_name}.{table_name}")
        resutl_df = postgresConnector.load_table(schema_name=schema_name, table_name=table_name)
        pd.testing.assert_frame_equal(df_local, resutl_df)
        postgresConnector.close_cursor()
        postgresConnector.close_connection()

    def test_load_table_function_returns_None_for_no_database_connection(self):
        """
        Test case to check that list_tables function returns None for no database connection
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password=db_password, host=db_host, port=db_port)
        schema_name = "public"
        table_name = "employees"
        result = postgresConnector.load_table(schema_name=schema_name, table_name=table_name)
        self.assertIsNone(result)

class TestGetTableSchema(unittest.TestCase):
    """
    Class used for testing the get_table_schema method of the PostgresConnector class from database/logics.py
    """
    def test_get_table_schema_function_returns_correct_schema_of_the_table(self):
        """
        Test case to check that the get_table_schema function returns the correct schema of the table
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        postgresConnector.open_connection()
        postgresConnector.open_cursor()
        schema_name = "public"
        table_name = "employees"
        engine = setup_local()
        df_local = run_sql_query(engine=engine, sql_query=f"SELECT c.table_name, c.column_name, c.data_type, CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k WHERE c.table_name = k.table_name and k.column_name = c.column_name) THEN true ELSE false END as primary_key, c.is_nullable, c.character_maximum_length, c.numeric_precision FROM INFORMATION_SCHEMA.COLUMNS c WHERE c.table_schema='{schema_name}' AND c.table_name='{table_name}'")
        resutl_df = postgresConnector.get_table_schema(schema_name=schema_name, table_name=table_name)
        pd.testing.assert_frame_equal(df_local, resutl_df)
        postgresConnector.close_cursor()
        postgresConnector.close_connection()

    def test_get_table_schema_function_returns_None_for_no_database_connection(self):
        """
        Test case to check that get_table_schema function returns None for no database connection
        """
        postgresConnector = PostgresConnector(database=db_name, user=db_password, password=db_password, host=db_host, port=db_port)
        schema_name = "public"
        table_name = "employees"
        result = postgresConnector.get_table_schema(schema_name=schema_name, table_name=table_name)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
import unittest
import pandas as pd

from src.database.queries import *

class TestTablesListQuery(unittest.TestCase):
    """
    Class used for testing the get_tables_list_query() function of the database/queries.py file
    """
    def setUp(self) -> None:
        """
        Method used to initiate the attributes or parameters that are going to be used in the test cases
        """
        self.correct_query = "SELECT table_schema || '.' || table_name AS table_name FROM information_schema.tables;"
        self.empty_query = ""
        self.none_query = None
        self.incorrect_query = "SELECT * FROM information_schema.tables;" 

    def test_get_tables_list_query_returns_correct_query(self):
        """
        Test case to check that the get_tables_list_query function returns the correct query
        """
        query = get_tables_list_query()
        self.assertEqual(self.correct_query, query)

    def test_get_tables_list_query_does_not_return_incorrect_query(self):
        """
        Test case to check that the get_tables_list_query function does not return incorrect query
        """
        query = get_tables_list_query()
        self.assertNotEqual(self.incorrect_query, query)

    def test_get_tables_list_query_does_not_return_none_or_empty_query(self):
        """
        Test case to check that the get_tables_list_query function does not return none or empty query
        """
        query = get_tables_list_query()
        self.assertNotEqual(self.empty_query, query)
        self.assertNotEqual(self.none_query, query)

    def tearDown(self) -> None:
        """
        Method used to clean the parameters after they have been used while running the test cases
        """
        del self.correct_query
        del self.empty_query
        del self.none_query
        del self.incorrect_query

class TestTableDataQuery(unittest.TestCase):
    """
    Class used for testing the get_table_data_query() function of the database/queries.py file
    """
    def setUp(self) -> None:
        """
        Method used to initiate the attributes or parameters that are going to be used in the test cases
        """
        self.schema_name = "public"
        self.table_name = "employees"
        self.correct_query = "SELECT * FROM public.employees"
        self.empty_schema = ""
        self.empty_table = ""

        self.none_schema = None
        self.none_table = None
        self.incorrect_schema = "pub"
        self.incorrect_table = "emp" 

    def test_get_table_data_query_returns_correct_query(self):
        """
        Test case to check that the get_table_data_query function returns the correct query
        """
        query = get_table_data_query(schema_name=self.schema_name, table_name=self.table_name)
        self.assertEqual(self.correct_query, query)

    def test_get_table_data_query_returns_None_for_empty_schema_table(self):
        """
        Test case to check that the get_table_data_query returns None for empty schema or empty table
        """
        query = get_table_data_query(schema_name=self.empty_schema, table_name=self.empty_table)
        self.assertEqual(None, query)

    def test_get_table_data_query_returns_None_for_none_schema_table(self):
        """
        Test case to check that the get_table_data_query returns None for None schema or table
        """
        query = get_table_data_query(schema_name=self.none_schema, table_name=self.none_schema)
        self.assertEqual(None, query)

    def test_get_table_data_query_does_not_return_incorrect_query(self):
        """
        Test case to check that the get_table_data_query function does not return incorrect query
        """
        query = get_table_data_query(schema_name=self.incorrect_schema, table_name=self.incorrect_table)
        self.assertNotEqual(self.correct_query, query)

    def tearDown(self) -> None:
        """
        Method used to clean the parameters after they have been used while running the test cases
        """
        del self.schema_name
        del self.table_name
        del self.correct_query
        del self.empty_schema
        del self.empty_table
        del self.none_schema
        del self.none_table
        del self.incorrect_schema
        del self.incorrect_table

class TestTableSchemaQuery(unittest.TestCase):
    """
    Class used for testing the get_table_schema_query() function of the database/queries.py file
    """
    def setUp(self) -> None:
        """
        Method used to initiate the attributes or parameters that are going to be used in the test cases
        """
        self.schema_name = "public"
        self.table_name = "employees"
        self.correct_query = "SELECT c.table_name, c.column_name, c.data_type, CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k WHERE c.table_name = k.table_name and k.column_name = c.column_name) THEN true ELSE false END as primary_key, c.is_nullable, c.character_maximum_length, c.numeric_precision FROM INFORMATION_SCHEMA.COLUMNS c WHERE c.table_schema='public' AND c.table_name='employees'"
        self.empty_schema = ""
        self.empty_table = ""

        self.none_schema = None
        self.none_table = None
        self.incorrect_schema = "pub"
        self.incorrect_table = "emp" 

    def test_get_table_schema_query_returns_correct_query(self):
        """
        Test case to check that the get_table_schema_query function returns the correct query
        """
        query = get_table_schema_query(schema_name=self.schema_name, table_name=self.table_name)
        self.assertEqual(self.correct_query, query)

    def test_get_table_schema_query_returns_None_for_empty_schema_table(self):
        """
        Test case to check that the get_table_schema_query returns None for empty schema or empty table
        """
        query = get_table_schema_query(schema_name=self.empty_schema, table_name=self.empty_table)
        self.assertEqual(None, query)

    def test_get_table_schema_query_returns_None_for_none_schema_table(self):
        """
        Test case to check that the get_table_schema_query returns None for None schema or table
        """
        query = get_table_schema_query(schema_name=self.none_schema, table_name=self.none_schema)
        self.assertEqual(None, query)

    def test_get_table_schema_query_does_not_return_incorrect_query(self):
        """
        Test case to check that the get_table_schema_query function does not return incorrect query
        """
        query = get_table_schema_query(schema_name=self.incorrect_schema, table_name=self.incorrect_table)
        self.assertNotEqual(self.correct_query, query)

    def tearDown(self) -> None:
        """
        Method used to clean the parameters after they have been used while running the test cases
        """
        del self.schema_name
        del self.table_name
        del self.correct_query
        del self.empty_schema
        del self.empty_table
        del self.none_schema
        del self.none_table
        del self.incorrect_schema
        del self.incorrect_table

if __name__ == '__main__':
    unittest.main(verbosity=2)
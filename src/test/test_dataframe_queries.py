import unittest
import pandas as pd

from src.dataframe.queries import *

class TestDataFrameQueries(unittest.TestCase):
    def test_numeric_query(self):
        schema_name = 'schema'
        table_name = 'table'
        test_query = get_numeric_tables_query(schema_name, table_name)
        expected_query = f"select column_name from information_schema.columns where table_schema = '{schema_name}' and table_name = '{table_name}' and data_type in ('smallint', 'integer', 'bigint', 'decimal', 'numeric', 'real', 'double precision', 'smallserial', 'serial', 'bigserial', 'money')"
        self.assertEqual(test_query, expected_query)

    def test_text_query(self):
        schema_name = 'schema'
        table_name = 'table'
        test_query = get_numeric_tables_query(schema_name, table_name)
        expected_query = f"select column_name from information_schema.columns where table_schema = '{schema_name}' and table_name = '{table_name}' and data_type in ('character varying', 'character', 'text', 'char', 'name', 'bytea')"
        self.assertEqual(test_query, expected_query)

    def test_date_query(self):
        schema_name = 'schema'
        table_name = 'table'
        test_query = get_numeric_tables_query(schema_name, table_name)
        expected_query = f"select column_name from information_schema.columns where table_schema = '{schema_name}' and table_name = '{table_name}' and data_type in ('timestamp without time zone', 'timestamp with time zone', 'time with time zone', 'time without time zone', 'interval', 'date')"
        self.assertEqual(test_query, expected_query)

if __name__ == '__main__':
    unittest.main(verbosity=2)

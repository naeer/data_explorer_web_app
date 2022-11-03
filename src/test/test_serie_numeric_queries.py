import unittest
import pandas as pd

from src.serie_numeric.queries import *

class TestSerieNumericQueries(unittest.TestCase):
    def test_get_negative_number_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_negative_number_query(schema_name, table_name, col_name)
        expected_query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} < 0"
        self.assertEqual(test_query, expected_query)

    def test_get_std_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_std_query(schema_name, table_name, col_name)
        expected_query = f"select stddev({col_name}) from {schema_name}.{table_name}"
        self.assertEqual(test_query, expected_query)

    def test_get_unique_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_unique_query(schema_name, table_name, col_name)
        expected_query = f"select count(distinct {col_name}) from {schema_name}.{table_name}"
        self.assertEqual(test_query, expected_query)

if __name__ == '__main__':
    unittest.main(verbosity=2)
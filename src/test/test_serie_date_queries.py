import unittest
import pandas as pd

from src.serie_date.queries import *

class TestSerieDateQueries(unittest.TestCase):
    def test_get_column_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_column_query(schema_name, table_name, col_name)
        expected_query = f"select {col_name} from {schema_name}.{table_name}"
        self.assertEqual(test_query, expected_query)

    def test_min_date_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_min_date_query(schema_name, table_name, col_name)
        expected_query = f"select min({col_name}) from {schema_name}.{table_name}"
        self.assertEqual(test_query, expected_query)

    def test_weekend_count_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_weekend_count_query(schema_name, table_name, col_name)
        expected_query = f"select count({col_name}) from {schema_name}.{table_name} where extract(isodow from {col_name}) in (6, 7)"
        self.assertEqual(test_query, expected_query)

    def test_weekday_count_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_weekday_count_query(schema_name, table_name, col_name)
        expected_query = f"select count({col_name}) from {schema_name}.{table_name} where extract(isodow from {col_name}) in (1, 2, 3, 4, 5)"
        self.assertEqual(test_query, expected_query)

    def test_future_count_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_future_count_query(schema_name, table_name, col_name)
        expected_query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} > current_date"
        self.assertEqual(test_query, expected_query)

    def test_1900_count_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_1900_count_query(schema_name, table_name, col_name)
        expected_query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} = '1900-01-01'"
        self.assertEqual(test_query, expected_query)

    def test_1970_count_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_1970_count_query(schema_name, table_name, col_name)
        expected_query = f"select count({col_name}) from {schema_name}.{table_name} where {col_name} = '1970-01-01'"
        self.assertEqual(test_query, expected_query)


if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import pandas as pd

from src.serie_text.queries import *

class TestSerieDateQueries(unittest.TestCase):
    def test_get_missing_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_missing_query(schema_name, table_name, col_name)
        expected_query  = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name}  is NULL"
        self.assertEqual(test_query, expected_query)
        
    def test_get_mode_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_mode_query(schema_name, table_name, col_name)
        expected_query = f"select mode() within group (order by {col_name}) from {schema_name}.{table_name}"
        self.assertEqual(test_query, expected_query)

    def test_get_alpha_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_alpha_query(schema_name, table_name, col_name)
        expected_query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:alpha:]]'" 
        self.assertEqual(test_query, expected_query)

    def test_get_whitespace(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_whitespace(schema_name, table_name, col_name)
        expected_query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:space:]]'" 
        self.assertEqual(test_query, expected_query)

    def test_get_lowercase(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_lowercase(schema_name, table_name, col_name)
        expected_query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:lower:]]'" 
        self.assertEqual(test_query, expected_query)
        
    def test_get_uppercase(self):    
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_uppercase(schema_name, table_name, col_name)
        expected_query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:upper:]]'" 
        self.assertEqual(test_query, expected_query)

    def test_get_digit(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_digit(schema_name, table_name, col_name)
        expected_query = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} ~ '[[:digit:]]'" 
        self.assertEqual(test_query, expected_query)

    def get_missing_query(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        test_query = get_missing_query(schema_name, table_name, col_name)
        expected_query  = f"SELECT count(*) FROM {schema_name}.{table_name} where {col_name} is NULL"
        self.assertEqual(test_query, expected_query)

if __name__ == '__main__':
    unittest.main(verbosity=2)
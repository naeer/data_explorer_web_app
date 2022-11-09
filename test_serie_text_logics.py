import unittest
import pandas as pd
import sqlalchemy as db
import numpy as np

from src.database.logics import PostgresConnector
from src.serie_text.logics import TextColumn
from src.serie_date.logics import DateColumn

def setup_local():
    engine = db.create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres") 
    return engine

def get_data_local(engine, table_name):
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    ResultProxy = connection.execute(db.select([table]))
    ResultSet = ResultProxy.fetchall()
    return pd.DataFrame(ResultSet)

class TestSerie(unittest.TestCase):
    def test_init(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        text = TextColumn(schema_name, table_name, col_name)
        self.assertEqual(text.schema_name, schema_name)
        self.assertEqual(text.table_name, table_name)
        self.assertEqual(text.col_name, col_name)
        self.assertIsNone(text.db)
        pd.testing.assert_series_equal(text.serie, pd.Series())
        self.assertIsNone(text.n_unique)
        self.assertIsNone(text.n_missing)
        self.assertIsNone(text.n_mode)
        self.assertIsNone(text.n_whitespace)
        self.assertIsNone(text.n_lower)
        self.assertIsNone(text.n_upper)
        self.assertIsNone(text.n_alpha)
        self.assertIsNone(text.n_empty)
        self.assertIsNone(text.n_digit)        
        self.assertIsNone(text.barchart)
        self.assertIsNone(text.frequent)

    def test_set_data(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'last_name'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = str(result['last_name'])

        text = TextColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        text.set_data()
        text.serie = str(text.serie)
        text.serie.name = 'last_name'

        counts = result_serie.value_counts().to_frame()
        counts_perc = round(result_serie.value_counts(normalize=True).to_frame().head(20), 4)
        counts_df = pd.DataFrame()
        counts_df['value'] = counts.index
        counts_df['occurrence'] = counts.values
        counts_df['percentage'] = counts_perc.values

        pd.testing.assert_series_equal(text.serie, result_serie)
        self.assertEqual(text.n_unique, result_serie.nunique())
        self.assertEqual(text.n_missing, result_serie.isna().sum())
        self.assertEqual(text.n_mode, result_serie.mode())
        self.assertEqual(text.n_whitespace, result_serie.whitespace)
        self.assertEqual(text.n_lower, result_serie.lower)
        self.assertEqual(text.n_upper, result_serie.upper)
        self.assertEqual(text.n_alpha, result_serie.alpha)
        self.assertEqual(text.n_empty, result_serie.empty)
        self.assertEqual(text.n_digit, result_serie.digit)
        pd.testing.assert_frame_equal(text.frequent, counts_df)


    def test_empty(self):
        empty_serie = pd.Series()
        text= TextColumn(serie = empty_serie)
        self.assertTrue(text.is_serie_none())
        matrix = {'text':[str(x) for x in list(range(1, 10))]}
        df = pd.DataFrame(matrix)  
        data_1 = TextColumn(df)
        self.assertTrue(data_1.is_serie_none()) 

    def test_unique(self):
        matrix = {'a','b','c','d','e','f'}
        df_1 = pd.DataFrame(matrix)
        data = TextColumn(serie = df_1)
        data.set_unique()
        self.assertFalse(data.n_unique, df_1.nunique())


    def test_missing(self):
        matrix = {'text':[str(x) for x in list(range(1, 10))]}
        df = pd.DataFrame(matrix)  
        data_1 = TextColumn(df)
        self.assertTrue(data_1.is_serie_none()) 

    def test_summary(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'last_name'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = str(result['last_name'])

        text = TextColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        text.set_data()

        actual = pd.DataFrame()
        summary['Description'] = ['Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Empty values', 'Number of Whitespaces', 'Mode of Values','Number of lowercase', 'Number of uppercase', 'Number of Series with alphabetical characters', 'Number of Series with digit characters']      
        actual['Value'] = [str(result_serie.nunique()), str(result_serie.isna().sum()), str(result_serie.isna().sum()), str(result_serie.space()), str(result_serie.mode()), str(result_serie.lower()), str(result_serie.upper()), str(result_serie.alpha()), str(result_serie.digit())]
        return summary

        pd.testing.assert_frame_equal(date.get_summary_df(), actual)



if __name__ == '__main__':
    unittest.main(verbosity=2)
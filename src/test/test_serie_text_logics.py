import unittest
import pandas as pd
import sqlalchemy as db
import numpy as np

from src.database.logics import PostgresConnector
from src.serie_text.logics import TextColumn

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
        result_serie = pd.Series(result['last_name'])
        apple = result_serie.mode()

        text_data = TextColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        text_data.set_data()
        text_data.serie = pd.Series(text_data.serie)
        text_data.serie.name = 'last_name'

        counts = result_serie.value_counts().to_frame()
        counts_perc = round(result_serie.value_counts(normalize=True).to_frame().head(20), 4)
        counts_df = pd.DataFrame()
        counts_df['value'] = counts.index
        counts_df['occurrence'] = counts.values
        counts_df['percentage'] = counts_perc.values

        pd.testing.assert_series_equal(text_data.serie, result_serie)
        self.assertEqual(text_data.n_unique, result_serie.nunique())
        self.assertEqual(text_data.n_missing, result_serie.isna().sum())
        self.assertEqual(text_data.n_mode, result_serie.mode()[0])
        self.assertEqual(text_data.n_whitespace, sum(result_serie.str.isspace() == True))
        self.assertEqual(text_data.n_lower, sum(result_serie.str.islower() == True))
        self.assertEqual(text_data.n_upper, sum(result_serie.str.isupper() == True))
        self.assertEqual(text_data.n_alpha, sum(result_serie.str.isalpha() == True))
        self.assertEqual(text_data.n_empty, result_serie.isna().sum())
        self.assertEqual(text_data.n_digit, sum(result_serie.str.isdigit() == True))
        pd.testing.assert_frame_equal(text_data.frequent, counts_df)


    def test_empty(self):
        empty_serie = pd.Series()
        text= TextColumn(serie = empty_serie)
        self.assertTrue(text.is_serie_none())
        matrix = {'text':[str(x) for x in list(range(1, 10))]}
        df = pd.DataFrame(matrix)  
        data_1 = TextColumn(df)
        self.assertFalse(pd.isna(data_1)) 

    def test_unique(self):
        matrix = {'text':[str(x) for x in list(range(1, 10))]}
        df_1 = pd.DataFrame(matrix)
        data = TextColumn(serie = df_1)
        self.assertFalse(pd.isna(data))

    def test_missing(self):
        matrix = {'text':[str(x) for x in list(range(1, 10))]}
        df = pd.DataFrame(matrix)  
        data_1 = TextColumn(df)
        self.assertFalse(pd.isnull(data_1)) 

    def test_summary(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'last_name'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = pd.Series(result['last_name'])

        text_data = TextColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        text_data.set_data()

        actual = pd.DataFrame()
        actual['Description'] = ['Number of Unique Values', 
                                    'Number of Rows with Missing Values', 
                                    'Number of Empty values', 
                                    'Number of Whitespaces', 
                                    'Mode of Values',
                                    'Number of lowercase', 
                                    'Number of uppercase', 
                                    'Number of Series with alphabetical characters', 
                                    'Number of Series with digit characters']      
        
        actual['Value'] = [str(result_serie.nunique()), 
                           str(result_serie.isna().sum()), 
                           str(result_serie.isna().sum()),  
                           str(sum(result_serie.str.isspace() == True)), 
                           result_serie.mode()[0], 
                           str(sum(result_serie.str.islower() == True)), 
                           str(sum(result_serie.str.isupper() == True)), 
                           str(sum(result_serie.str.isalpha() == True)),
                           str(sum(result_serie.str.isdigit() == True))]


        pd.testing.assert_frame_equal(text_data.get_summary_df(), actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)
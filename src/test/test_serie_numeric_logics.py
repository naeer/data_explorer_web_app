import unittest
import pandas as pd
import sqlalchemy as db
import numpy as np

from src.database.logics import PostgresConnector
from src.serie_numeric.logics import NumericColumn

def setup_local():
    engine = db.create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")
    return engine

def get_data_local(engine, table_name):
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    res_proxy = connection.execute(db.select([table]))
    res_df = res_proxy.fetchall()
    return pd.DataFrame(res_df)

class TestSerie(unittest.TestCase):
    def test_init(self):
        schema_name = 'schema'
        table_name = 'table'
        col_name = 'column'
        numeric_data = NumericColumn(schema_name, table_name, col_name)
        self.assertEqual(numeric_data.schema_name, schema_name)
        self.assertEqual(numeric_data.table_name, table_name)
        self.assertEqual(numeric_data.column_name, col_name)
        self.assertIsNone(numeric_data.db)
        pd.testing.assert_series_equal(numeric_data.serie, pd.Series())
        self.assertIsNone(numeric_data.n_unique)
        self.assertIsNone(numeric_data.n_missing)
        self.assertIsNone(numeric_data.col_mean)
        self.assertIsNone(numeric_data.col_std)
        self.assertIsNone(numeric_data.col_min)
        self.assertIsNone(numeric_data.col_max)
        self.assertIsNone(numeric_data.col_median)
        self.assertIsNone(numeric_data.n_zeros)
        self.assertIsNone(numeric_data.n_negatives)
        self.assertIsNone(numeric_data.histogram)
        self.assertIsNone(numeric_data.frequent)

    def test_set_data(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'employee_id'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = pd.to_numeric(result['employee_id'])

        numeric_data = NumericColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        numeric_data.set_data()
        numeric_data.serie = pd.to_numeric(numeric_data.serie)
        numeric_data.serie.name = 'employee_id'

        counts = result_serie.value_counts().to_frame()
        percentages = round(result_serie.value_counts(normalize=True).to_frame().head(20), 4)
        counts_df = pd.DataFrame()
        counts_df['value'] = pd.to_numeric(counts.index)
        counts_df['occurrence'] = counts.values
        counts_df['percentage'] = percentages.values

        pd.testing.assert_series_equal(numeric_data.serie, result_serie)
        self.assertEqual(numeric_data.n_unique, result_serie.nunique())
        self.assertEqual(numeric_data.n_missing, result_serie.isna().sum())
        self.assertEqual(numeric_data.col_mean, result_serie.mean)
        self.assertEqual(numeric_data.col_std, result_serie.std)
        self.assertEqual(numeric_data.col_min, result_serie.min)
        self.assertEqual(numeric_data.col_max, result_serie.max)
        self.assertEqual(numeric_data.col_median, result_serie.median)
        self.assertEqual(numeric_data.n_negatives, (result_serie == 0).sum())
        self.assertEqual(numeric_data.n_zeros, (result_serie < 0).sum())
        pd.testing.assert_frame_equal(numeric_data.frequent, counts_df)

    def test_empty(self):
        empty_serie = pd.Series()
        empty_numeric_data = NumericColumn(ds = empty_serie)
        self.assertTrue(empty_numeric_data.is_serie_none())
        rand_data = pd.Series(np.random.randint(0,10,size=(9)))
        test_numeric_data = NumericColumn(ds = rand_data)
        self.assertFalse(test_numeric_data.is_serie_none())

    def test_missing(self):
        data = [None]*9
        result_serie = pd.Series(data)
        test_numeric_data = NumericColumn(serie = result_serie)
        test_numeric_data.set_missing()
        self.assertEqual(test_numeric_data.n_missing, result_serie.isna().sum())

    def test_summary(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'employee_id'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = pd.to_numeric(result['employee_id'])

        test_numeric_data = NumericColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        test_numeric_data.set_data()

        actual = pd.DataFrame()
        actual['Description'] = ['Number of Unique Values', 
                                  'Number of Rows with Missing Values', 
                                  'Number of Rows with 0', 
                                  'Number of Rows with Negative Values', 
                                  'Average Value', 
                                  'Standard Deviation Value', 
                                  'Minimum Value', 
                                  'Maximum Value', 
                                  'Median Value',]
        actual['Value'] = ['{:,.0f}'.format(result_serie.nunique()), 
                           '{:,.0f}'.format(result_serie.isna().sum()), 
                           '{:,.0f}'.format((result_serie < 0).sum()), 
                           '{:,.0f}'.format((result_serie == 0).sum()), 
                           '{:,.3f}'.format(result_serie.mean()), 
                           '{:,.3f}'.format(result_serie.std()), 
                           '{:,.3f}'.format(result_serie.min()), 
                           '{:,.3f}'.format(result_serie.max()), 
                           '{:,.3f}'.format(result_serie.median())]
        pd.testing.assert_frame_equal(test_numeric_data.get_summary_df(), actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)
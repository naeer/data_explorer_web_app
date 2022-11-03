import unittest
import pandas as pd
import sqlalchemy as db
from datetime import datetime

from src.database.logics import PostgresConnector
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
        date = DateColumn(schema_name, table_name, col_name)
        self.assertEqual(date.schema_name, schema_name)
        self.assertEqual(date.table_name, table_name)
        self.assertEqual(date.col_name, col_name)
        self.assertIsNone(date.db)
        pd.testing.assert_series_equal(date.serie, pd.Series())
        self.assertIsNone(date.n_unique)
        self.assertIsNone(date.n_missing)
        self.assertIsNone(date.col_min)
        self.assertIsNone(date.col_max)
        self.assertIsNone(date.n_weekend)
        self.assertIsNone(date.n_weekday)
        self.assertIsNone(date.n_future)
        self.assertIsNone(date.n_empty_1900)
        self.assertIsNone(date.n_empty_1970)
        self.assertIsNone(date.barchart)
        self.assertIsNone(date.frequent)

    def test_set_date(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'birth_date'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = pd.to_datetime(result['birth_date'])

        date = DateColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        date.set_data()
        date.serie = pd.to_datetime(date.serie)
        date.serie.name = 'birth_date'

        counts = result_serie.value_counts().to_frame()
        counts_perc = round(result_serie.value_counts(normalize=True).to_frame().head(20), 4)
        counts_df = pd.DataFrame()
        counts_df['value'] = pd.to_datetime(counts.index)
        counts_df['occurrence'] = counts.values
        counts_df['percentage'] = counts_perc.values

        pd.testing.assert_series_equal(date.serie, result_serie)
        self.assertEqual(date.n_unique, result_serie.nunique())
        self.assertEqual(date.n_missing, result_serie.isna().sum())
        self.assertEqual(date.col_min, min(result_serie))
        self.assertEqual(date.col_max, max(result_serie))
        self.assertEqual(date.n_weekend, (result_serie.dt.weekday > 5).sum())
        self.assertEqual(date.n_weekday, (result_serie.dt.weekday <= 5).sum())
        self.assertEqual(date.n_future, (result_serie > pd.to_datetime('today')).sum())
        self.assertEqual(date.n_empty_1900, (result_serie == pd.to_datetime('1900/01/01')).sum())
        self.assertEqual(date.n_empty_1970, (result_serie == pd.to_datetime('1970/01/01')).sum())
        pd.testing.assert_frame_equal(date.frequent, counts_df)

    def test_empty(self):
        empty_serie = pd.Series()
        date = DateColumn(serie = empty_serie)
        self.assertTrue(date.is_serie_none())
        data = pd.date_range(datetime.today(), periods=9).tolist()
        result_serie = pd.Series(data)
        date_1 = DateColumn(serie = result_serie)
        self.assertFalse(date_1.is_serie_none())

    def test_unique(self):
        data = pd.date_range(datetime.today(), periods=9).tolist()
        serie = pd.Series(data)
        result_serie = serie.append(serie)
        date = DateColumn(serie = result_serie)
        date.set_unique()
        self.assertEqual(date.n_unique, result_serie.nunique())

    def test_missing(self):
        data = [None]*9
        result_serie = pd.Series(data)
        date = DateColumn(serie = result_serie)
        date.set_missing()
        self.assertEqual(date.n_missing, result_serie.isna().sum())

    def test_summary(self):
        schema_name = 'public'
        table_name = 'employees'
        col_name = 'birth_date'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        result_serie = pd.to_datetime(result['birth_date'])

        date = DateColumn(schema_name, table_name, col_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        date.set_data()

        actual = pd.DataFrame()
        actual['Description'] = ['Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Weekend Dates', 'Number of Weekday Dates', 'Number of Dates in Future', 'Number of Rows with 1900-01-01', 'Number of Rows with 1970-01-01', 'Minimum Value', 'Maximum Value']
        actual['Value'] = [str(result_serie.nunique()), str(result_serie.isna().sum()), str((result_serie.dt.weekday > 5).sum()), str((result_serie.dt.weekday <= 5).sum()), str((result_serie > pd.to_datetime('today')).sum()), str((result_serie == pd.to_datetime('1900/01/01')).sum()), str((result_serie == pd.to_datetime('1970/01/01')).sum()), str(min(result_serie))[:-9], str(max(result_serie))[:-9]]

        pd.testing.assert_frame_equal(date.get_summary_df(), actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)

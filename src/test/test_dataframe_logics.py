import re
import unittest
import pandas as pd
import sqlalchemy as db
from datetime import datetime
from sqlalchemy.engine import reflection

from src.database.logics import PostgresConnector
from src.dataframe.logics import Dataset

def setup(df, table_name):
    engine = db.create_engine('sqlite://')
    df.to_sql(table_name, con=engine)
    return engine

def setup_local():
    engine = db.create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")
    return engine

def get_data(engine, table_name):
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    ResultProxy = connection.execute(db.select([table]))
    ResultSet = ResultProxy.fetchall()
    return pd.DataFrame(ResultSet)

def get_data_local(engine, table_name):
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    ResultProxy = connection.execute(db.select([table]))
    ResultSet = ResultProxy.fetchall()
    return pd.DataFrame(ResultSet)

def testnumeric(engine, table_name):
    numeric_cols = ['SMALLINT', 'INTEGER', 'BIGINT', 'DECIMAL', 'NUMERIC', 'REAL', 'DOUBLE PRECISION', 'SMALLSERIAL', 'SERIAL', 'BIGSERIAL', 'MONEY']
    connection = engine.connect()
    metadata = db.MetaData()
    inspector = reflection.Inspector.from_engine(engine)
    col_list = list()
    for column in inspector.get_columns(table_name):
        if (str(column['type']) in numeric_cols):
            col_list.append(column['name'])
    return col_list

def testtext(engine, table_name):
    text_cols = ['CHARACTER VARYING', 'VARCHAR', 'CHARACTER', 'TEXT', 'CHAR', 'NAME', 'BYTEA']
    connection = engine.connect()
    metadata = db.MetaData()
    inspector = reflection.Inspector.from_engine(engine)
    col_list = list()
    for column in inspector.get_columns(table_name):
        if (re.sub(r'\([^)]*\)', '', str(column['type'])) in text_cols):
            col_list.append(column['name'])
    return col_list

def testdate(engine, table_name):
    date_cols = ['TIMESTAMP WITHOUT TIME ZONE', 'TIMESTAMP WITH TIME ZONE', 'TIME WITH TIME ZONE', 'TIME WITHOUT TIME ZONE', 'INTERVAL', 'DATE']
    connection = engine.connect()
    metadata = db.MetaData()
    inspector = reflection.Inspector.from_engine(engine)
    col_list = list()
    for column in inspector.get_columns(table_name):
        if (re.sub(r'\([^)]*\)', '', str(column['type'])) in date_cols):
            col_list.append(column['name'])
    return col_list

def testschema(engine, table_name):
    name_list = list()
    connection = engine.connect()
    metadata = db.MetaData()
    inspector = reflection.Inspector.from_engine(engine)
    for column in inspector.get_columns(table_name):
        name_list.append(column['name'])
    df = pd.DataFrame(list(name_list), columns =['column_name'])
    return df

class TestDataFrame(unittest.TestCase):
    def test_init(self):
        schema_name = 'schema'
        table_name = 'table'
        data = Dataset(schema_name, table_name)
        self.assertEqual(data.schema_name, schema_name)
        self.assertEqual(data.table_name, table_name)
        self.assertIsNone(data.db)
        pd.testing.assert_frame_equal(data.df, pd.DataFrame())
        self.assertIsNone(data.n_rows)
        self.assertIsNone(data.n_cols)
        self.assertIsNone(data.n_duplicates)
        self.assertIsNone(data.n_missing)
        self.assertIsNone(data.num_cols)
        self.assertIsNone(data.text_cols)
        self.assertIsNone(data.date_cols)

    def test_set_data(self):
        schema_name = 'public'
        table_name = 'employees'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        data = Dataset(schema_name, table_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        data.set_data()

        data.df['birth_date'] = data.df['birth_date'].dt.tz_localize(None)
        data.df['hire_date'] = data.df['hire_date'].dt.tz_localize(None)
        
        result['birth_date'] = pd.to_datetime(result['birth_date'])
        result['hire_date'] = pd.to_datetime(result['hire_date'])

        pd.testing.assert_frame_equal(data.df, result)
        self.assertEqual(data.n_rows, result.shape[0])
        self.assertEqual(data.n_cols, result.shape[1])
        self.assertEqual(data.n_duplicates, result.duplicated().sum())
        self.assertEqual(data.n_missing, result.isna().sum().sum())
        numeric_cols = testnumeric(engine, table_name)
        text_cols = testtext(engine, table_name)
        date_cols = testdate(engine, table_name)
        self.assertEqual(data.num_cols, numeric_cols)
        self.assertEqual(data.text_cols, text_cols)
        self.assertEqual(data.date_cols, date_cols)

    def test_empty(self):
        df_empty = pd.DataFrame()
        data = Dataset(df=df_empty)
        self.assertTrue(data.is_df_none())
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df_mock = pd.DataFrame(matrix)
        data_1 = Dataset(df=df_mock)
        self.assertFalse(data_1.is_df_none())

    def test_duplicates(self):
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df = pd.DataFrame(matrix)
        df_dup = df.append(df)
        data = Dataset(df=df_dup)
        data.set_duplicates()
        self.assertEqual(data.n_duplicates, df_dup.duplicated().sum())

    def test_missing(self):
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df = pd.DataFrame(matrix)
        data = Dataset(df=df)
        data.set_missing()
        self.assertEqual(data.n_missing, df.isna().sum().sum())

    def test_get_head(self):
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df = pd.DataFrame(matrix)
        data = Dataset(df=df)
        pd.testing.assert_frame_equal(data.get_head(5), df.head(5))

    def test_get_tail(self):
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df = pd.DataFrame(matrix)
        data = Dataset(df=df)
        pd.testing.assert_frame_equal(data.get_tail(5), df.tail(5))

    def test_get_sample(self):
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df = pd.DataFrame(matrix)
        data = Dataset(df=df)
        self.assertEqual(data.get_sample(5).shape[0], df.sample(5).shape[0])
        self.assertEqual(data.get_sample(5).shape[1], df.sample(5).shape[1])

    def test_summary(self):
        matrix = {'numeric':list(range(1, 10)), 'text':[str(x) for x in list(range(1, 10))], 'date':pd.date_range(datetime.today(), periods=9).tolist(), 'none':[None]*9}
        df = pd.DataFrame(matrix)
        data = Dataset(table_name='table', df=df)
        data.set_dimensions()
        data.set_duplicates()
        data.set_missing()
        actual = pd.DataFrame()
        actual['Description'] = ['Name of Table', 'Number of Rows', 'Number of Columns', 'Number of Duplicated Rows', 'Number of Rows with Missing Values']
        actual['Value'] = ['table', df.shape[0], df.shape[1], df.duplicated().sum(), df.isna().sum().sum()]
        pd.testing.assert_frame_equal(data.get_summary_df(), actual)

    def test_schema(self):
        schema_name = 'public'
        table_name = 'employees'
        engine = setup_local()
        result = get_data_local(engine, table_name)
        data = Dataset(schema_name, table_name, db=PostgresConnector(database='postgres', user='postgres', password='password', host='localhost', port='5432'))
        result = data.get_schema()['column_name']
        actual = testschema(engine, table_name)['column_name']
        s1 = result.sort_values(ignore_index=True)
        s2 = actual.sort_values(ignore_index=True)
        pd.testing.assert_series_equal(s1, s2)

if __name__ == '__main__':
    unittest.main(verbosity=2)

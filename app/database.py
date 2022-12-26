import os
import csv
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SQLALCHEMY_DB_URL = os.getenv('SQLALCHEMY_DB_URL')
connection_args = {'sslmode': os.getenv('SSLMODE'),
                   'target_session_attrs': os.getenv('TARGET_SESSION_ATTRS')}

engine = create_engine(SQLALCHEMY_DB_URL, connect_args=connection_args)


def delete_duplicates_from_data_analytics_bydays_main_table(engine):
    delete_query = """DELETE FROM data_analytics_bydays_main 
                       WHERE ctid IN 
                            (SELECT ctid 
                               FROM (SELECT ctid,
                                            row_number() OVER (PARTITION BY api_id, sku_id, date, region_id
                                            ORDER BY id DESC) AS row_num
                                       FROM data_analytics_bydays_main
                                    ) t
                              WHERE t.row_num > 1
                            );"""
    with engine.connect() as conn:
        conn.execute(text(delete_query))


def psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute SQL statement inserting data

    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join(['"{}"'.format(k) for k in keys])
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

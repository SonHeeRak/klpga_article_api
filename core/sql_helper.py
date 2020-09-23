import pymysql
import pandas as pd
from core.log_helper import LogHelper


class SqlHelper:
    def __init__(self, host, port, db_name, user, password):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password

    def execute(self, query):
        data_frame = None
        conn = None

        try:
            # Open database connection
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db_name
                                   , charset="utf8", autocommit=True, cursorclass=pymysql.cursors.DictCursor)
            cursor = conn.cursor()
            cursor.execute(query)

            result = cursor.fetchall()
            data_frame = pd.DataFrame(result)
            data_frame.columns = map(str.lower, data_frame.columns)
        except Exception as e:
            LogHelper.instance().e(e)
        finally:
            if conn is not None:
                # disconnect from server
                conn.close()

        return data_frame

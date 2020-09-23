import sys
import config as c
from core.sql_helper import SqlHelper
from core.log_helper import LogHelper

r_host = c.DB_ARTICLE_CONFIG['host']
r_port = c.DB_ARTICLE_CONFIG['port']
r_db_name = c.DB_ARTICLE_CONFIG['db_name']
r_user = c.DB_ARTICLE_CONFIG['user']
r_password = c.DB_ARTICLE_CONFIG['password']


class DbTemplate:

    def __init__(self):
        self.sql_helper = SqlHelper(r_host, r_port, r_db_name, r_user, r_password)

    def base_template(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT T_INDEX, T_GROUP, T_NAME, T_RANK, T_USE, T_CONDITION, T_EVAL, T_SENTENCE, T_TEMPLATE_TAB '
                'FROM BASE_TEMPLATE')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def common_dynamic_variable(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT T_INDEX, T_GROUP, T_NAME, T_RANK, T_USE, T_CONDITION, T_EVAL, T_SENTENCE '
                'FROM COMMON_DYNAMIC_VARIABLE')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def method_info(self, name=None):
        data_frame = None
        try:
            if name is None:
                data_frame = self.sql_helper.execute('SELECT T_INDEX, T_NAME, T_KOR, T_METHOD FROM METHOD_INFO')
            else:
                data_frame = self.sql_helper\
                    .execute("SELECT T_INDEX, T_NAME, T_KOR, T_METHOD FROM METHOD_INFO "
                             "WHERE `T_NAME` = '{name}'".format(name=name))

            if len(data_frame) > 0:
                data_frame = data_frame.astype({'t_index': 'int'})
        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def player_test_sentence(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT T_INDEX, T_GROUP, T_NAME, T_RANK, T_USE, T_CONDITION, T_EVAL, T_SENTENCE '
                'FROM PLAYER_TEST_SENTENCE')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def round_dynamic_variable(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT T_INDEX, T_GROUP, T_NAME, T_RANK, T_USE, T_CONDITION, T_EVAL, T_SENTENCE '
                'FROM ROUND_DYNAMIC_VARIABLE')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def shot_dynamic_variable(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT T_INDEX, T_GROUP, T_NAME, T_RANK, T_USE, T_CONDITION, T_EVAL, T_SENTENCE '
                'FROM SHOT_DYNAMIC_VARIABLE')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

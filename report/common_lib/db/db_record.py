import sys
import config as c
from core.sql_helper import SqlHelper
from core.log_helper import LogHelper

r_host = c.DB_KLPGA_CONFIG['host']
r_port = c.DB_KLPGA_CONFIG['port']
r_db_name = c.DB_KLPGA_CONFIG['db_name']
r_user = c.DB_KLPGA_CONFIG['user']
r_password = c.DB_KLPGA_CONFIG['password']


class DbRecord:

    def __init__(self):
        self.sql_helper = SqlHelper(r_host, r_port, r_db_name, r_user, r_password)

    def cd_master(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT CD_GROUP, CD_SE, GROUP_NM, CD_ID, CD_NM '
                'FROM CD_MASTER')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def player_list(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT SEASON_ID, MEMBER_TYPE, P_ID, P_NM, REG_DT '
                'FROM PLAYER_LIST')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def player_profile(self, p_id=None):
        data_frame = None
        try:
            if p_id is None:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, MEMBER_TYPE, P_ID, P_NM, P_NM_ENG, P_NM_CHN, BIRTH_DATE, BIRTH_DATE_ORIGINAL, '
                    'HEIGHT, HEIGHT_ORIGINAL, BLOOD_TYPE, ADMISSION_DATE, ADMISSION_DATE_ORIGINAL, MEMBER_ID, '
                    'SPONSOR, USE_BALL, SELF_INTRODUCTION, REG_DT '
                    'FROM PLAYER_PROFILE')
            else:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, MEMBER_TYPE, P_ID, P_NM, P_NM_ENG, P_NM_CHN, BIRTH_DATE, BIRTH_DATE_ORIGINAL, '
                    'HEIGHT, HEIGHT_ORIGINAL, BLOOD_TYPE, ADMISSION_DATE, ADMISSION_DATE_ORIGINAL, MEMBER_ID, '
                    'SPONSOR, USE_BALL, SELF_INTRODUCTION, REG_DT '
                    'FROM PLAYER_PROFILE '
                    'WHERE P_ID = {p_id}'.format(p_id=p_id))

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def player_shot(self, tour_id=None):
        data_frame = None
        try:
            if tour_id is None:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_ID, P_ID, ROUND_CN, HOLE_CN, SHOT_CN, SHOT_TEXT, DISTANCE, '
                    'REST_DISTANCE, REG_DT FROM PLAYER_SHOT')
            else:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_ID, P_ID, ROUND_CN, HOLE_CN, SHOT_CN, SHOT_TEXT, DISTANCE, '
                    'REST_DISTANCE, REG_DT FROM PLAYER_SHOT '
                    'WHERE TOUR_ID={tour_id}'.format(tour_id=tour_id))

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def tour_course_hole_info(self, tour_id=None):
        data_frame = None
        try:
            if tour_id is None:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_ID, HOLE_TYPE, HOLE_NO, YARD, METER, PAR, GREEN, REG_DT '
                    'FROM TOUR_COURSE_HOLE_INFO')
            else:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_ID, HOLE_TYPE, HOLE_NO, YARD, METER, PAR, GREEN, REG_DT '
                    'FROM TOUR_COURSE_HOLE_INFO '
                    'WHERE TOUR_ID={tour_id}'.format(tour_id=tour_id))

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def tour_list(self, tour_id=None):
        data_frame = None
        try:
            if tour_id is None:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_TYPE, TOUR_ID, MONTH_ID, TOUR_NAME, START_DATE, END_DATE, '
                    'START_WEEK, END_WEEK, START_DATE_ORIGINAL, END_DATE_ORIGINAL, PLACE, COURSE, TOTAL_PRIZE_MONEY, '
                    'TOTAL_PRIZE_MONEY_UNIT, TOTAL_PRIZE_MONEY_ORIGINAL, WINNER, REG_DT '
                    'FROM TOUR_LIST')
            else:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_TYPE, TOUR_ID, MONTH_ID, TOUR_NAME, START_DATE, END_DATE, '
                    'START_WEEK, END_WEEK, START_DATE_ORIGINAL, END_DATE_ORIGINAL, PLACE, COURSE, TOTAL_PRIZE_MONEY, '
                    'TOTAL_PRIZE_MONEY_UNIT, TOTAL_PRIZE_MONEY_ORIGINAL, WINNER, REG_DT '
                    'FROM TOUR_LIST '
                    'WHERE TOUR_ID = {tour_id}'.format(tour_id=tour_id))

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def tour_participant(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT SEASON_ID, TOUR_ID, PARTICIPANT_TYPE, P_ID, REG_DT '
                'FROM TOUR_PARTICIPANT')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def tour_player_group(self):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                'SELECT SEASON_ID, TOUR_ID, ROUND_NO, GROUP_NO, P_ID, REG_DT '
                'FROM TOUR_PLAYER_GROUP')

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def tour_total_score(self, tour_id=None):
        data_frame = None
        try:
            if tour_id is None:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_ID, P_ID, TOTAL_RANK, TOTAL_RANK_NO, TOTAL_SCORE, ROUND_1_STROKE, '
                    'ROUND_1_RANK, ROUND_2_STROKE, ROUND_2_RANK, ROUND_3_STROKE, ROUND_3_RANK, ROUND_4_STROKE,'
                    'ROUND_4_RANK, TOTAL_STROKE, PRIZE_MONEY, REG_DT '
                    'FROM TOUR_TOTAL_SCORE')
            else:
                data_frame = self.sql_helper.execute(
                    'SELECT SEASON_ID, TOUR_ID, P_ID, TOTAL_RANK, TOTAL_RANK_NO, TOTAL_SCORE, ROUND_1_STROKE, '
                    'ROUND_1_RANK, ROUND_2_STROKE, ROUND_2_RANK, ROUND_3_STROKE, ROUND_3_RANK, ROUND_4_STROKE,'
                    'ROUND_4_RANK, TOTAL_STROKE, PRIZE_MONEY, REG_DT '
                    'FROM TOUR_TOTAL_SCORE '
                    'WHERE TOUR_ID={tour_id}'.format(tour_id=tour_id))

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def player_best_last_shot(self, tour_id, p_id, round_no, hole_list_text):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                """
                SELECT season_id, tour_id, p_id, round_cn, hole_cn, shot_cn, `distance`, rest_distance
                FROM
                (
                    SELECT season_id, tour_id, p_id, round_cn, hole_cn, shot_cn, `distance`, rest_distance, (`distance` - rest_distance) AS shot_distance,
                            ROW_NUMBER() OVER (PARTITION BY season_id, tour_id, p_id, round_cn ORDER BY (`distance` - rest_distance) DESC) AS ROW_NUM
                    FROM player_shot
                    WHERE season_id = 2020 AND tour_id = {tour_id} and p_id = {p_id} AND round_cn = {round_no}
                        AND rest_distance = 0 AND `distance` > 0
                        AND hole_cn IN ({hole_list_text})
                ) AS A
                WHERE ROW_NUM = 1
                """.format(tour_id=tour_id, p_id=p_id, round_no=round_no, hole_list_text=hole_list_text))
        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame

    def player_bad_last_shot(self, tour_id, p_id, round_no, hole_list_text):
        data_frame = None
        try:
            data_frame = self.sql_helper.execute(
                """
                SELECT season_id, tour_id, p_id, round_cn, hole_cn, shot_cn, `distance`, rest_distance
                FROM
                (
                    SELECT season_id, tour_id, p_id, round_cn, hole_cn, shot_cn, `distance`, rest_distance, shot_distance,
                        ROW_NUMBER() OVER (PARTITION BY season_id, tour_id, p_id, round_cn ORDER BY `shot_distance` ASC) AS ROW_NUM_2
                    FROM
                    (
                        SELECT season_id, tour_id, p_id, round_cn, hole_cn, shot_cn, `distance`, rest_distance, (`distance` - rest_distance) AS shot_distance,
                            ROW_NUMBER() OVER (PARTITION BY season_id, tour_id, p_id, round_cn, hole_cn ORDER BY `distance` ASC) AS ROW_NUM
                        FROM player_shot
                        WHERE season_id = 2020 AND tour_id = {tour_id} and p_id = {p_id} AND round_cn = {round_no}
                            AND rest_distance > 0
                            AND hole_cn IN ({hole_list_text})
                    ) AS A
                    WHERE ROW_NUM = 1
                ) AS A
                WHERE ROW_NUM_2 = 1
                """.format(tour_id=tour_id, p_id=p_id, round_no=round_no, hole_list_text=hole_list_text))
        except Exception as ex:
            LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                                   func_name=sys._getframe().f_code.co_name)
        return data_frame
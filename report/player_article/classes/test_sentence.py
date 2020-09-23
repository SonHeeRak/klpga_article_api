from report.common_lib import globals as g
import pandas as pd
import sys
from core.log_helper import LogHelper

import random
import datetime


class PlayerTestVariables(object):

    def __init__(self, player_info=None, tour_info=None):
        self.player_info = player_info
        self.tour_info = tour_info
        self.competition_round = 3
        self.season = self.tour_info.get_season()

    def get_var(self):
        """
        선수_테스트문장
        :return:
        """
        var = NamedVariable()
        try:
            setattr(var, '공통', self.get_common_sentence())
            setattr(var, '첫문단', self.get_1st_sentence())
        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)
        return var

    def get_common_sentence(self):
        var = NamedVariable()
        try:
            # 선수프로필관련
            birth_date = self.player_info.get_birth_date()
            age = self.season - int(birth_date[0:4])
            admission_date = self.player_info.get_admission_date()
            player_year = self.season - int(admission_date[0:4])

            setattr(var, '선수나이', age)
            setattr(var, '선수연차', player_year)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return var

    def get_1st_sentence(self):
        """
        첫문단
        :return:
        """
        var = NamedVariable()
        try:
            start_date = self.tour_list_df.iloc[-1].start_date
            current = datetime.datetime.strptime(start_date, '%Y%m%d') + \
                      datetime.timedelta(days=self.competition_round - 1)
            current_date = datetime.datetime.strftime(current, '%Y%m%d')
            tour_place = self.tour_list_df.iloc[-1].place
            tour_course = self.tour_list_df.iloc[-1].course
            tour_total_prize = self.get_won(self.tour_list_df.iloc[-1].total_prize_money)

            setattr(var, '경기일자', current_date[-2:])
            setattr(var, '경기장소', tour_place)
            setattr(var, '경기코스', tour_course)
            setattr(var, '상금', tour_total_prize)
            setattr(var, '라운드', self.competition_round)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return var


class NamedVariable:
    pass

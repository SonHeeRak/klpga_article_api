import sys
from core.log_helper import LogHelper
import datetime

from report.common_lib.db.db_record import DbRecord
from report.common_lib import globals as g


class Tour(object):
    def __init__(self, tour_id, round_no):
        try:
            self.tour_id = tour_id
            self.round_no = round_no
            self.tour_df = DbRecord().tour_list(tour_id=self.tour_id)

            self.is_first_major()

            g.define_method(self, g.method_info_tour)
        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

    def get_season(self):
        """
        시즌
        :return:
        """
        return self.tour_df.season_id.values.sum()

    def get_type(self):
        """
        타입
        :return:
        """
        return self.tour_df.tour_type.values.sum()

    def get_month(self):
        """
        달
        :return:
        """
        return self.tour_df.month_id.values.sum()

    def get_name(self):
        """
        대회명
        :return:
        """
        return self.tour_df.tour_name.values.sum()

    def get_start_date(self):
        """
        시작일자
        :return:
        """
        return self.tour_df.start_date.values.sum()

    def get_end_date(self):
        """
        종료일자
        :return:
        """
        return self.tour_df.end_date.values.sum()

    def get_start_week(self):
        """
        시작요일
        :return:
        """
        return self.tour_df.start_week.values.sum()

    def get_end_week(self):
        """
        종료요일
        :return:
        """
        return self.tour_df.end_week.values.sum()

    def get_place(self):
        """
        장소
        :return:
        """
        return self.tour_df.place.values.sum()

    def get_course(self):
        """
        코스
        :return:
        """
        return self.tour_df.course.values.sum()

    def get_prize(self):
        """
        상금
        :return:
        """
        return g.get_won(self.tour_df.total_prize_money.values.sum())

    def get_prize_unit(self):
        """
        화폐단위
        :return:
        """
        return self.tour_df.total_prize_money_unit.values.sum()

    def get_winner(self):
        """
        우승자
        :return:
        """
        return self.tour_df.winner.values.sum()

    def is_major(self):
        """
        is_메이저
        :return:
        """
        name = self.get_name()
        is_major = False
        for c in g.major_competition:
            if c in name:
                is_major = True

        return is_major

    def get_date(self):
        """
        일자
        :return:
        """
        start_date = self.tour_df.start_date.values.sum()
        round_date = datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=self.round_no - 1)
        round_date = datetime.datetime.strftime(round_date, '%Y%m%d')
        round_date = round_date[-2:]
        return round_date

    def is_first_major(self):
        """
        is_첫_메이저
        :return:
        """
        season_tour_df = DbRecord().tour_list()
        season = self.get_season()
        season_tour_df = season_tour_df[season_tour_df.season_id == season]
        is_first_major = False
        if len(season_tour_df) == 1:
            is_first_major = True
        return is_first_major

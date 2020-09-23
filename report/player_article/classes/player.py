import sys
from core.log_helper import LogHelper

from report.common_lib.db.db_record import DbRecord
from report.common_lib import globals as g


class Player(object):
    def __init__(self, p_id):
        try:
            self.p_id = p_id
            self.player_df = DbRecord().player_profile(p_id=self.p_id)

            g.define_method(self, g.method_info_player)
        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

    def get_member_type(self):
        """
        회원타입
        :return:
        """
        return self.player_df.member_type.values.sum()

    def get_p_nm(self):
        """
        이름
        :return:
        """
        return self.player_df.p_nm.values.sum()

    def get_birth_year(self):
        """
        생일연도
        :return:
        """
        birth_date = self.player_df.birth_date.values.sum()
        birth_year = birth_date[0:4]
        return birth_year

    def get_height(self):
        """
        키
        :return:
        """
        return self.player_df.height.values.sum()

    def get_admission_year(self):
        """
        등록연도
        :return:
        """
        admission_date = self.player_df.admission_date.values.sum()
        admission_year = admission_date[0:4]
        return admission_year

    def get_sponsor(self):
        """
        스폰서
        :return:
        """
        return self.player_df.sponsor.values.sum()

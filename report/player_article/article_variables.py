import sys
from core.log_helper import LogHelper
from report.common_lib.db.db_record import DbRecord
from report.player_article.classes.test_sentence import PlayerTestVariables
from report.player_article.classes.tour import Tour
from report.player_article.classes.player import Player
from report.player_article.classes.round import Round
from report.player_article.classes.shot import Shot
from report.common_lib import globals as g


class PlayerArticleVariables(object):
    def __init__(self, p_id, tour_id, round_no):
        try:
            self.tour_id = tour_id
            self.p_id = p_id
            self.round_no = round_no

            self.tour_info = None
            self.player_info = None
            self.round_info = None
            self.shot_info = None

            self.set_class_variables()

            self.article_type = 'player'

            # player_test_var = PlayerTestVariables(player_info=self.player_info,
            #                                       tour_info=self.tour_info)
            # setattr(self, '선수_테스트문장', player_test_var.get_var())

            g.define_method(self, g.method_info_common)

            for k, v in g.VARIABLE_DICT['common_dynamic_variable'].items():
                setattr(self, k, v)
            for k, v in g.VARIABLE_DICT['shot_dynamic_variable'].items():
                setattr(self, k, v)
            for k, v in g.VARIABLE_DICT['round_dynamic_variable'].items():
                setattr(self, k, v)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

    def get_dict_var(self):
        return self.__dict__

    def get_article_type(self):
        """
        기사타입
        :return:
        """
        return self.article_type

    def is_player_article(self):
        """
        is_플레이어
        :return:
        """
        return True if self.article_type == 'player' else False

    def set_class_variables(self):
        """
        변수 셋팅
        :return:
        """
        self.tour_info = Tour(tour_id=self.tour_id, round_no=self.round_no)
        self.player_info = Player(p_id=self.p_id)
        self.round_info = Round(tour_id=self.tour_id, p_id=self.p_id, round_no=self.round_no)
        self.shot_info = Shot(tour_id=self.tour_id, p_id=self.p_id, round_no=self.round_no)

    def tour(self):
        """
        투어
        :return:
        """
        return self.tour_info

    def player(self):
        """
        선수
        :return:
        """
        return self.player_info

    def round(self):
        """
        라운드
        :return:
        """
        return self.round_info

    def shot(self):
        """
        샷
        :return:
        """
        return self.shot_info

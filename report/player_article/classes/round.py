import sys
from core.log_helper import LogHelper

from report.common_lib.db.db_record import DbRecord
from report.common_lib import globals as g


class Round(object):
    def __init__(self, tour_id, p_id, round_no):
        self.tour_id = tour_id
        self.p_id = p_id
        self.round_no = round_no
        self.round_df = DbRecord().tour_total_score(tour_id=self.tour_id)
        self.player_round_df = self.round_df[self.round_df.p_id == self.p_id]

        g.define_method(self, g.method_info_round)

    def get_round(self):
        """
        기준라운드
        :return:
        """
        return self.round_no

    def is_tie(self):
        """
        is_공동순위
        :return:
        """
        total_rank = self.player_round_df.total_rank.values.sum()
        is_tie = False
        if total_rank[-1] == 'T':
            is_tie = True
        return is_tie

    def get_total_rank_no(self):
        """
        대회순위
        :return:
        """
        return self.player_round_df.total_rank_no.values.sum()

    def get_round_1_stroke(self):
        """
        1라운드스트로크
        :return:
        """
        return self.player_round_df.round_1_stroke.values.sum()

    def get_round_1_rank(self):
        """
        1라운드순위
        :return:
        """
        return self.player_round_df.round_1_rank.values.sum()

    def get_round_2_stroke(self):
        """
        2라운드스트로크
        :return:
        """
        return self.player_round_df.round_2_stroke.values.sum()

    def get_round_2_rank(self):
        """
        2라운드순위
        :return:
        """
        return self.player_round_df.round_2_rank.values.sum()

    def get_round_3_stroke(self):
        """
        3라운드스트로크
        :return:
        """
        return self.player_round_df.round_3_stroke.values.sum()

    def get_round_3_rank(self):
        """
        3라운드순위
        :return:
        """
        return self.player_round_df.round_3_rank.values.sum()

    def get_round_4_stroke(self):
        """
        4라운드스트로크
        :return:
        """
        return self.player_round_df.round_4_stroke.values.sum()

    def get_round_4_rank(self):
        """
        4라운드순위
        :return:
        """
        return self.player_round_df.round_4_rank.values.sum()

    def get_total_stroke(self):
        """
        총스트로크
        :return:
        """
        return self.player_round_df.total_stroke.values.sum()

    def get_prize_money(self):
        """
        상금
        :return:
        """
        return self.player_round_df.prize_money.values.sum()

    def is_first(self):
        """
        is_1등
        :return:
        """
        return True if self.get_total_rank_no() == 1 else False

    def get_after_finish_round(self):
        """
        라운드후
        :return:
        """
        var = NamedVariable()
        try:
            round_columns = ['round_1_stroke', 'round_2_stroke', 'round_3_stroke', 'round_4_stroke']
            round_columns = round_columns[:self.round_no]
            round_df = self.round_df[['tour_id', 'p_id'] + round_columns]
            round_df = round_df[round_df[round_columns[self.round_no-1]] != '']

            # 순위
            total_stroke = []
            for col in round_columns:
                round_df = round_df.astype({'{column}'.format(column=col): 'int64'})
                total_stroke.append(round_df['{columns}'.format(columns=col)].values)
            round_df['total_stroke'] = sum(total_stroke)
            round_df['rank'] = round_df.total_stroke.rank(method='min')
            round_df = round_df.sort_values('rank')
            finish_round_rank = int(round_df[round_df.p_id == self.p_id]['rank'].values.min())
            setattr(var, '순위', finish_round_rank)

            # 탑5 여부
            is_top5 = False
            if finish_round_rank <= 5:
                is_top5 = True
            setattr(var, 'is_탑5', is_top5)

            # 1등 여부
            is_first = False
            if finish_round_rank == 1:
                is_first = True
            setattr(var, 'is_1등', is_first)

            # 스코어차이
            score_gap = None
            finish_round_first_score = round_df[round_df['rank'] == 1].total_stroke.values.min()
            if is_first:
                finish_round_2nd_rank = round_df['rank'].unique().tolist()[1]
                finish_round_2nd_score = round_df[round_df['rank'] == finish_round_2nd_rank].total_stroke.values.min()
                score_gap = abs(finish_round_first_score - finish_round_2nd_score)
            else:
                finish_round_score = round_df[round_df['rank'] == finish_round_rank].total_stroke.values.min()
                score_gap = abs(finish_round_first_score - finish_round_score)
            setattr(var, '스코어차이', score_gap)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return var

    def get_before_finish_round(self):
        """
        이전라운드
        :return:
        """
        var = NamedVariable()
        try:
            if self.round_no != 1:
                round_columns = ['round_1_stroke', 'round_2_stroke', 'round_3_stroke', 'round_4_stroke']
                round_columns = round_columns[:self.round_no-1]
                round_df = self.round_df[['tour_id', 'p_id'] + round_columns]
                round_df = round_df[round_df[round_columns[self.round_no-2]] != '']

                # 순위
                total_stroke = []
                for col in round_columns:
                    round_df = round_df.astype({'{column}'.format(column=col): 'int64'})
                    total_stroke.append(round_df['{columns}'.format(columns=col)].values)
                round_df['total_stroke'] = sum(total_stroke)
                round_df['rank'] = round_df.total_stroke.rank(method='min')
                finish_round_rank = int(round_df[round_df.p_id == self.p_id]['rank'].values.min())
                setattr(var, '순위', finish_round_rank)

                # 탑5 여부
                is_top5 = False
                if finish_round_rank <= 5:
                    is_top5 = True
                setattr(var, 'is_탑5', is_top5)

                # 1등 여부
                is_first = False
                if finish_round_rank == 1:
                    is_first = True
                setattr(var, 'is_1등', is_first)

                # 스코어차이
                score_gap = None
                finish_round_first_score = round_df[round_df['rank'] == 1].total_stroke.values.min()
                if is_first:
                    finish_round_2nd_rank = round_df['rank'].unique().tolist()[1]
                    finish_round_2nd_score = round_df[round_df['rank'] == finish_round_2nd_rank].total_stroke.values.min()
                    score_gap = abs(finish_round_first_score - finish_round_2nd_score)
                else:
                    finish_round_score = round_df[round_df['rank'] == finish_round_rank].total_stroke.values.min()
                    score_gap = abs(finish_round_first_score - finish_round_score)
                setattr(var, '스코어차이', score_gap)
            else:
                setattr(var, '순위', 0)
                setattr(var, 'is_탑5', False)
                setattr(var, 'is_1등', False)
                setattr(var, '스코어차이', 0)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return var


class NamedVariable:
    pass

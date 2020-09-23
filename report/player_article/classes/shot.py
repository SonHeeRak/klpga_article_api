import sys
from core.log_helper import LogHelper
import pandas as pd

from report.common_lib.db.db_record import DbRecord
from report.common_lib import globals as g
from report.player_article.classes.hole import Hole


class Shot(object):
    def __init__(self, tour_id, p_id, round_no):
        try:
            self.tour_id = tour_id
            self.p_id = p_id
            self.round_no = round_no
            self.db_record = DbRecord()
            self.shot_df = self.db_record.player_shot(tour_id=self.tour_id)
            self.player_shot_df = self.shot_df[self.shot_df.p_id == self.p_id]

            self.hole_df = Hole(tour_id=self.tour_id).get_hole_par_no().astype({'hole_no': 'int64', 'par': 'int64'})

            g.define_method(self, g.method_info_shot)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

    def get_record(self):
        """
        기록
        :return:
        """
        var = NamedVariable()
        try:
            hole_shot_df = self.player_shot_df[self.player_shot_df.round_cn == self.round_no][['hole_cn', 'shot_cn']]
            hole_shot_df = hole_shot_df.drop_duplicates(subset=['hole_cn'], keep='last')
            hole_shot_df = pd.merge(self.hole_df, hole_shot_df, left_on='hole_no', right_on='hole_cn')
            hole_shot_df['score'] = hole_shot_df['shot_cn'] - hole_shot_df['par']

            # 스코어
            score = hole_shot_df.score.values.sum()
            setattr(var, '스코어', score)

            # 스코어절대값
            abs_score = abs(score)
            setattr(var, '절대값스코어', abs_score)

            # 스트로크수
            stroke_cn = hole_shot_df.shot_cn.values.sum()
            setattr(var, '스트로크수', stroke_cn)

            # 오스트리치개수
            ostrich_cn = len(hole_shot_df[hole_shot_df.score == -5])
            setattr(var, '오스트리치개수', ostrich_cn)

            # 콘도르개수
            condor_cn = len(hole_shot_df[hole_shot_df.score == -4])
            setattr(var, '콘도르개수', condor_cn)

            # 알바트로스개수
            albatross_cn = len(hole_shot_df[hole_shot_df.score == -3])
            setattr(var, '알바트로스개수', albatross_cn)

            # 이글개수
            eagle_cn = len(hole_shot_df[hole_shot_df.score == -2])
            setattr(var, '이글개수', eagle_cn)

            # 버디개수
            birdie_cn = len(hole_shot_df[hole_shot_df.score == -1])
            setattr(var, '버디개수', birdie_cn)

            # 파개수
            par_cn = len(hole_shot_df[hole_shot_df.score == 0])
            setattr(var, '파개수', par_cn)

            # 보기개수
            bogey_cn = len(hole_shot_df[hole_shot_df.score == 1])
            setattr(var, '보기개수', bogey_cn)

            # 더블보기개수
            double_bogey_cn = len(hole_shot_df[hole_shot_df.score == 2])
            setattr(var, '더블보기개수', double_bogey_cn)

            # 트리플보기개수
            triple_bogey_cn = len(hole_shot_df[hole_shot_df.score == 3])
            setattr(var, '트리플보기개수', triple_bogey_cn)

            # 쿼드러플보기개수
            quadruple_bogey_cn = len(hole_shot_df[hole_shot_df.score == 4])
            setattr(var, '쿼드러플보기개수', quadruple_bogey_cn)

            # 첫 보기 홀 번호
            first_bogey_hole_no = hole_shot_df[hole_shot_df.score > 0]["hole_no"].min()
            setattr(var, '첫보기홀번호', first_bogey_hole_no)

            # 첫 보기 홀 파
            first_bogey_hole_par = hole_shot_df[hole_shot_df.hole_cn == first_bogey_hole_no]["par"].min()
            setattr(var, '첫보기홀파', first_bogey_hole_par)

            # 첫 보기 전 홀
            setattr(var, '첫보기전홀번호', first_bogey_hole_no-1)

            # 첫 보기 전 버디 개수
            first_bogey_buddy_cn = len(hole_shot_df[(hole_shot_df.hole_cn < first_bogey_hole_no) & (hole_shot_df.score < 0)])
            setattr(var, '첫보기전버디', first_bogey_buddy_cn)

            # 홀 리스트
            buddy_holes = hole_shot_df[hole_shot_df.score == -1]["hole_no"].to_list()
            buddy_strs = []
            for index, buddy_hole in enumerate(buddy_holes):
                buddy_strs.append('{hole_no}번 홀'.format(hole_no=buddy_hole))
            buddy_str = ', '.join(buddy_strs)

            bogey_holes = hole_shot_df[hole_shot_df.score == 1]["hole_no"].to_list()
            bogey_strs = []
            for index, bogey_hole in enumerate(bogey_holes):
                bogey_strs.append('{hole_no}번 홀'.format(hole_no=bogey_hole))
            bogey_str = ', '.join(bogey_strs)

            eagle_holes = hole_shot_df[hole_shot_df.score == -2]["hole_no"].to_list()
            eagle_strs = []
            for index, eagle_hole in enumerate(eagle_holes):
                eagle_strs.append('{hole_no}번 홀'.format(hole_no=eagle_hole))
            eagle_str = ', '.join(eagle_strs)

            doublebogey_holes = hole_shot_df[hole_shot_df.score == 2]["hole_no"].to_list()
            doublebogey_strs = []
            for index, doublebogey_hole in enumerate(doublebogey_holes):
                doublebogey_strs.append('{hole_no}번 홀'.format(hole_no=doublebogey_hole))
            doublebogey_str = ', '.join(doublebogey_strs)

            hole_total_str = []

            if len(doublebogey_holes) > 0:
                hole_total_str.insert(0, '{doublebugey_str}에서 더블보기를 기록'.format(doublebugey_str=doublebogey_str))

            if len(eagle_holes) > 0:
                if len(hole_total_str) > 0:
                    hole_total_str.insert(0, '{eagle_str}에서 이글을 기록했고, '.format(eagle_str=eagle_str))
                else:
                    hole_total_str.insert(0, '{eagle_str}에서 이글을 기록'.format(eagle_str=eagle_str))

            if len(bogey_holes) > 0:
                if len(hole_total_str) > 0:
                    hole_total_str.insert(0, '{bogey_str}에서 보기를 기록했고, '.format(bogey_str=bogey_str))
                else:
                    hole_total_str.insert(0, '{bogey_str}에서 보기를 기록'.format(bogey_str=bogey_str))

            if len(buddy_holes) > 0:
                if len(hole_total_str) > 0:
                    hole_total_str.insert(0, '{buddy_str}에서 버디를 기록했고, '.format(buddy_str=buddy_str))
                else:
                    hole_total_str.insert(0, '{buddy_str}에서 버디를 기록 '.format(buddy_str=buddy_str))

            setattr(var, '홀리스트', ''.join(hole_total_str))

            hole_cn = 0
            if len(bogey_holes) > 0:
                # 아쉬운 샷
                df = self.db_record.player_bad_last_shot(tour_id=self.tour_id, p_id=self.p_id, round_no=self.round_no
                                                         , hole_list_text=str(bogey_holes).replace('[', '').replace(']',
                                                                                                                    ''))
                shot_cn = int(df.iloc[0].shot_cn)
                distance = df.iloc[0].distance
                rest_distance = df.iloc[0].rest_distance
                hole_cn = int(df.iloc[0].hole_cn)
            if len(eagle_holes) > 0:
                # 인상깊은 마지막 샷
                df = self.db_record.player_best_last_shot(tour_id=self.tour_id, p_id=self.p_id, round_no=self.round_no
                                                          ,
                                                          hole_list_text=str(eagle_holes).replace('[', '').replace(']',
                                                                                                                   ''))
                shot_cn = int(df.iloc[0].shot_cn) # 당장 미사용
                distance = df.iloc[0].distance
                rest_distance = df.iloc[0].rest_distance # 당장 미사용
                hole_cn = int(df.iloc[0].hole_cn)

            if hole_cn > 0:
                setattr(var, '언급샷_횟수', shot_cn)
                setattr(var, '언급샷_목표거리', distance)
                setattr(var, '언급샷_남은거리', rest_distance)
                setattr(var, '언급샷_진행홀', hole_cn)


        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)
        return var

    def get_last_record(self):
        """
        이전라운드기록
        :return:
        """
        var = NamedVariable()
        try:
            if self.round_no > 1:
                last_round_no = self.round_no - 1
                hole_shot_df = self.player_shot_df[self.player_shot_df.round_cn == last_round_no][['hole_cn', 'shot_cn']]
                hole_shot_df = hole_shot_df.drop_duplicates(subset=['hole_cn'], keep='last')
                hole_shot_df = pd.merge(self.hole_df, hole_shot_df, left_on='hole_no', right_on='hole_cn')
                hole_shot_df['score'] = hole_shot_df['shot_cn'] - hole_shot_df['par']

                # 스코어
                score = hole_shot_df.score.values.sum()
                setattr(var, '스코어', score)

                # 스코어절대값
                abs_score = abs(score)
                setattr(var, '절대값스코어', abs_score)

                # 스트로크수
                stroke_cn = hole_shot_df.shot_cn.values.sum()
                setattr(var, '스트로크수', stroke_cn)

                # 오스트리치개수
                ostrich_cn = len(hole_shot_df[hole_shot_df.score == -5])
                setattr(var, '오스트리치개수', ostrich_cn)

                # 콘도르개수
                condor_cn = len(hole_shot_df[hole_shot_df.score == -4])
                setattr(var, '콘도르개수', condor_cn)

                # 알바트로스개수
                albatross_cn = len(hole_shot_df[hole_shot_df.score == -3])
                setattr(var, '알바트로스개수', albatross_cn)

                # 이글개수
                eagle_cn = len(hole_shot_df[hole_shot_df.score == -2])
                setattr(var, '이글개수', eagle_cn)

                # 버디개수
                birdie_cn = len(hole_shot_df[hole_shot_df.score == -1])
                setattr(var, '버디개수', birdie_cn)

                # 파개수
                par_cn = len(hole_shot_df[hole_shot_df.score == 0])
                setattr(var, '파개수', par_cn)

                # 보기개수
                bogey_cn = len(hole_shot_df[hole_shot_df.score == 1])
                setattr(var, '보기개수', bogey_cn)

                # 더블보기개수
                double_bogey_cn = len(hole_shot_df[hole_shot_df.score == 2])
                setattr(var, '더블보기개수', double_bogey_cn)

                # 트리플보기개수
                triple_bogey_cn = len(hole_shot_df[hole_shot_df.score == 3])
                setattr(var, '트리플보기개수', triple_bogey_cn)

                # 쿼드러플보기개수
                quadruple_bogey_cn = len(hole_shot_df[hole_shot_df.score == 4])
                setattr(var, '쿼드러플보기개수', quadruple_bogey_cn)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)
        return var

    def get_total_record(self):
        """
        전체기록
        :return:
        """
        var = NamedVariable()
        try:
            hole_shot_df = self.player_shot_df[self.player_shot_df.round_cn <= self.round_no]
            hole_shot_df = hole_shot_df[['round_cn', 'hole_cn', 'shot_cn']]
            hole_shot_df = hole_shot_df.drop_duplicates(subset=['round_cn', 'hole_cn'], keep='last')
            hole_shot_df = pd.merge(self.hole_df, hole_shot_df, left_on='hole_no', right_on='hole_cn')
            hole_shot_df['score'] = hole_shot_df['shot_cn'] - hole_shot_df['par']

            # 스코어
            score = hole_shot_df.score.values.sum()
            setattr(var, '스코어', score)

            # 스코어절대값
            abs_score = abs(score)
            setattr(var, '절대값스코어', abs_score)

            # 스트로크수
            stroke_cn = hole_shot_df.shot_cn.values.sum()
            setattr(var, '스트로크수', stroke_cn)

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)
        return var


class NamedVariable:
    pass

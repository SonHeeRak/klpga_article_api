import sys
from core.log_helper import LogHelper

from report.common_lib.parent_controllers import ParentControllers
from report.common_lib.sentence_template import SentenceTemplate
from report.player_article.article_variables import PlayerArticleVariables

from core.cache_helper import CacheHelper


class PlayerControllers(ParentControllers):
    def __init__(self, p_id, tour_id, round_no):
        super().__init__()
        self.p_id = p_id
        self.tour_id = tour_id
        self.round_no = round_no

    def generate_article(self):
        print('>>>>>>>>')
        print(CacheHelper.get_cache_dict())
        result = super().success_result()

        try:
            result['article_type'] = 'player'
            article_var = PlayerArticleVariables(p_id=self.p_id, tour_id=self.tour_id, round_no=self.round_no)

            template_sentence = SentenceTemplate(article_var)
            sentence_list = template_sentence.set_sentence()

            contents = ''
            if len(sentence_list) > 0:
                contents = '\n\n'.join(sentence_list)

            result['contents'] = contents

        except Exception as ex:
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)
            result = super().failure_result()
            result['result_msg'] = str(ex)

        return result

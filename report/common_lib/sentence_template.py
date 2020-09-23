import sys
from core.log_helper import LogHelper

from . import globals as g
from report.common_lib.sentence_generator import SentenceGenerator


class SentenceTemplate(object):
    def __init__(self, article_var):
        self.article_var = article_var

    def set_sentence(self):
        print('set_sentence')
        sentence_list = []

        try:
            active_tab_list = []
            base_temp = g.MODEL_DICT['base_template']

            sg = SentenceGenerator()

            if base_temp is None:
                return sentence_list

            for i, bt in base_temp.iterrows():
                if bt['t_use'] != 'F':
                    condition_string = sg.get_result_string(
                        sg.main_dict, bt['t_condition'], self.article_var, final=True)

                    if eval(condition_string):
                        if bt['t_template_tab'] not in active_tab_list:
                            active_tab_list.append(bt['t_template_tab'])
                            sg.set_variable(self.article_var, bt['t_template_tab'])

                        sg.set_used_arguments_for_log(bt['t_sentence'], self.article_var.__dict__)
                        paragraph = bt['t_sentence'].format(**self.article_var.__dict__).strip()
                        sentences = paragraph.split('\n\n')
                        sentence_list.extend(sentences)

        except Exception as ex:
            sentence_list = []
            sentences = 'error! msg : ' + str(ex) + ' \nplease generate report instead'
            sentence_list.append(sentences)
            '\n\n'.join(sentence_list)
            LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return sentence_list

import sys
import random
import time

from report.common_lib.db.db_template import DbTemplate
from core.log_helper import LogHelper


MODEL_DICT = {}
DYNAMIC_MODEL_DICT = {}
DF_GROUP_DICT = {}
VARIABLE_DICT = {}
method_info_common = None
method_info_player = None
method_info_tour = None
method_info_round = None
method_info_shot = None
major_competition = []


def initialize():
    try:
        starttime = time.time()

        global MODEL_DICT
        global DYNAMIC_MODEL_DICT

        global DF_GROUP_DICT
        global VARIABLE_DICT

        global method_info_common
        global method_info_player
        global method_info_tour
        global method_info_round
        global method_info_shot

        global major_competition

        # region Clear Values
        MODEL_DICT = {}
        DYNAMIC_MODEL_DICT = {}
        DF_GROUP_DICT = {}
        VARIABLE_DICT = {}
        method_info_common = None
        method_info_player = None
        method_info_tour = None
        method_info_round = None
        method_info_shot = None
        major_competition = []
        # endregion Clear Values

        MODEL_DICT = {
            'method_info': DbTemplate().method_info(),
            'base_template': DbTemplate().base_template(),
            'player_test_sentence': DbTemplate().player_test_sentence(),
        }
        DYNAMIC_MODEL_DICT = {
            'common_dynamic_variable': DbTemplate().common_dynamic_variable(),
            'shot_dynamic_variable': DbTemplate().shot_dynamic_variable(),
            'round_dynamic_variable': DbTemplate().round_dynamic_variable(),
        }

        for (name, model) in DYNAMIC_MODEL_DICT.items():
            VARIABLE_DICT[name] = init_dynamic_variable(model)

        method_info_common = get_dict_method(DbTemplate().method_info('common'))
        method_info_player = get_dict_method(DbTemplate().method_info('player'))
        method_info_tour = get_dict_method(DbTemplate().method_info('tour'))
        method_info_round = get_dict_method(DbTemplate().method_info('round'))
        method_info_shot = get_dict_method(DbTemplate().method_info('shot'))

        major_competition = ['한국여자오픈', '한화 클래식', 'KLPGA 챔피언십', 'KB금융 스타챔피언십', '하이트진로 챔피언십']

        LogHelper.instance().d('globals initialize')

        endtime = time.time()
        print('초기화 걸리는 시간 : ', endtime - starttime)
    except Exception as ex:
        LogHelper.instance().e(ex, file_name=sys._getframe().f_code.co_filename,
                               func_name=sys._getframe().f_code.co_name)


def init_dynamic_variable(model):
    df_dynamic_group = model.groupby(['t_group', 't_name', 't_rank'])

    var_dict = {}
    for d in df_dynamic_group:
        var_name = d[0][1]  # name key
        var_list = d[1].to_dict('record')  # data value list

        selected_var_dict = random.choice(var_list)
        if selected_var_dict['t_use'] == 'F':
            continue

        if var_name in var_dict:
            var_dict[var_name].append(selected_var_dict)
        else:
            var_dict[var_name] = [selected_var_dict]

    return var_dict


def get_dict_method(object_value):
    return {row['t_kor']: row['t_method'] for i, row in object_value.iterrows()}


def define_method(obj, method_dict):
    for k, v in method_dict.items():
        setattr(obj, k, getattr(obj, v))


def get_random_sentence(text):
    temp_list = [d.strip() for d in text.split('@') if d]
    if not temp_list:
        temp_list.append('')
    return random.choice(temp_list)


def get_won(prize):
    result = None
    try:
        length = len(prize)
        if length >= 9:
            result = int(prize) // 100000000
            if str(int(prize) % 100000000) != '0':
                result = str(result) + '억' + str(int(prize) % 100000000)[0] + '천만'
            else:
                result = str(result) + '억'
        elif length == 8:
            result = int(prize) // 10000000
            result = str(result) + '천만'
    except Exception as ex:
        LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)
    return result

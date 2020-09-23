from report.common_lib import globals as g
from report.common_lib import lab2ai_linguistic as linguistic
import re
import random
from core.log_helper import LogHelper


class SentenceGenerator(object):

    def __init__(self):
        self.main_dict = {}

    def set_variable(self, var, table_name):
        if table_name in g.DF_GROUP_DICT:
            df_dynamic_group = g.DF_GROUP_DICT[table_name]
        else:
            model = g.MODEL_DICT[table_name]
            df_dynamic_group = model.groupby(['t_group', 't_name', 't_rank'])
            g.DF_GROUP_DICT[table_name] = df_dynamic_group

        for d in df_dynamic_group:
            var_name = d[0][1]  # name key
            var_list = d[1].to_dict('record')  # data value list

            if var_name in var.__dict__:
                continue

            var_dict = random.choice(var_list)
            if var_dict['t_use'] == 'F':
                continue

            condition = self.get_global_condition(var_dict['t_condition'], var)
            if condition:
                str_sentence = self.get_result_string(self.main_dict, var_dict['t_sentence'], var)
                if var_dict['t_eval'] == 'T':
                    text = eval(str_sentence)
                    setattr(var, var_dict['t_name'], text)
                else:
                    text = str_sentence
                    text = self.get_josa(text)
                    setattr(var, var_dict['t_name'], text)

    def get_global_condition(self, condition, val):
        cond_list = condition.split('and')
        for cond in cond_list:
            split_condition = cond
            reg = r"\{(.+?)\}"
            param_list = re.findall(reg, cond)

            if not param_list:
                continue

            for param in param_list:
                if param not in self.main_dict:
                    p = param.split('.')
                    value = self.get_attr(val, p)
                    if value == '':
                        value = False

                    setattr(val, param, value)
                    self.main_dict.update({param: value})

            for param in param_list:
                split_condition = split_condition.replace("{%s}" % param, "%s" % self.main_dict[param])

            if eval(split_condition):
                continue
            else:
                return False
        return True

    def get_result_string(self, param_dict, sentence, var, final=False):
        result = sentence
        reg = r"\{(.+?)\}"
        param_list = re.findall(reg, result)
        if param_list:
            for param in param_list:
                p = param.split('.')

                if param == '생략':
                    param_dict.update({param: ''})
                else:
                    param_dict.update({param: self.get_attr(var, p)})
            if final and result != '{생략}':
                LogHelper.instance().d("{0}: {1}".format(result, param_dict))
            for param in param_list:
                result = result.replace("{%s}" % param, "%s" % param_dict[param])
        if final:
            LogHelper.instance().d("[Condition]: {0}: {1}".format(result, param_dict))
        return result

    def get_josa(self, text):
        result = linguistic.get_josa(text)
        return result

    def get_attr(self, variable, str_list):
        if str_list:
            s = str_list.pop(0)

            if s[0] == '_':
                attr_value = self.get_dynamic_variable(variable, s)
            else:
                attr_value = getattr(variable, s, '')

            if callable(attr_value):
                val = attr_value()
                if not callable(val):
                    setattr(variable, s, val)
            else:
                val = attr_value

            if str_list:
                return self.get_attr(val, str_list)
            else:
                return val

    def get_dynamic_variable(self, val, variable):
        variable_result = getattr(val, variable, '')
        param_dict = {}
        if type(variable_result) != list:
            return variable_result

        for var_dict in variable_result:
            cond = self.get_condition(var_dict['t_condition'], val)
            if cond:
                str_sentence = self.get_result_string(param_dict, var_dict['t_sentence'], val)

                if str_sentence:
                    if var_dict['t_eval'] == 'T':
                        text = eval(str_sentence)
                    else:
                        text = str_sentence
                        text = self.get_josa(text)
                else:
                    text = str_sentence

                setattr(val, var_dict['t_name'], text)
                return text
        return ''

    def get_condition(self, condition, val):
        split_condition = cond = condition
        reg = r"\{(.+?)\}"
        param_list = re.findall(reg, cond)
        param_dict = {}

        if not param_list and condition != 'True':
            return False

        for param in param_list:
            p = param.split('.')
            value = self.get_attr(val, p)
            if value == '':
                value = False

            param_dict.update({param: value})

        for param in param_list:
            split_condition = split_condition.replace("{%s}" % param, "%s" % param_dict[param])

        if eval(split_condition):
            return True
        else:
            return False

    def set_used_arguments_for_log(self, str_string, var_args):
        reg = r"\{(.+?)\}"
        param_list = re.findall(reg, str_string)

        for param in param_list:
            LogHelper.instance().d("[문장]: {0}=> {0}".format(param, var_args[param]))

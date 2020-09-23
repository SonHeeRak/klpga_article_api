import sys
from flask_caching import Cache

from core.log_helper import LogHelper


class CacheHelper:

    _dict_cache = None

    class Time:
        SEC_10 = 1 * 10
        MIN_1 = 1 * 60
        MIN_5 = MIN_1 * 5
        MIN_10 = MIN_1 * 10
        HOUR_1 = MIN_10 * 6
        DEFAULT = MIN_1

    @staticmethod
    def init(app):
        CacheHelper._dict_cache = dict()

        def set_init_cache_object(cache_time):
            cache_config = dict()
            cache_config['DEBUG'] = False
            cache_config['CACHE_TYPE'] = 'simple'
            cache_config['CACHE_DEFAULT_TIMEOUT'] = cache_time
            CacheHelper._dict_cache[cache_time] = Cache(app, config=cache_config)

        set_init_cache_object(CacheHelper.Time.SEC_10)
        set_init_cache_object(CacheHelper.Time.MIN_1)
        set_init_cache_object(CacheHelper.Time.MIN_5)
        set_init_cache_object(CacheHelper.Time.MIN_10)
        set_init_cache_object(CacheHelper.Time.HOUR_1)

    @staticmethod
    def get_cache_dict(time=None):
        result = None

        if CacheHelper._dict_cache is not None:
            if time is None:
                time = CacheHelper.Time.DEFAULT

            result = CacheHelper._dict_cache[time]

        return result

    @staticmethod
    def get(cache_key=None, time=None):
        result = None

        if CacheHelper._dict_cache is not None and cache_key is not None:
            if time is None:
                time = CacheHelper.Time.DEFAULT

            try:
                result = CacheHelper.get_cache_dict(time).get(cache_key)
            except Exception as ex:
                LogHelper.instance().e(ex, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return result

    @staticmethod
    def set(cache_key=None, cache_value=None, time=None):
        result = None

        if CacheHelper._dict_cache is not None and cache_key is not None:
            if time is None:
                time = CacheHelper.Time.DEFAULT

            CacheHelper.get_cache_dict(time).set(cache_key, cache_value)
        else:
            message = 'CacheHelper is not initialize or cache_key is None > {cache_key}'.format(cache_key=cache_key)
            LogHelper.instance().d(message, file_name=__name__, func_name=sys._getframe().f_code.co_name)

        return result

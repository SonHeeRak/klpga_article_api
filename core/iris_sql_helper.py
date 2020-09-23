#! /bin/env python3
# coding:utf-8

import time
import signal
import core.API.M6_IRIS2_PY3 as M6
import core.Mobigen.Common.Log_PY3 as Log
import os
import sys
import pandas as pd

Log.Init()


class IRIS_PRD:
    HOST = '192.168.70.2'
    PORT = 5050
    DIRECT_PORT = 5000
    DB_NAME = 'KOTRABP'
    USER = 'kotrabp'
    PASSWORD = 'kotrabp123'


class IRIS_DEV:
    HOST = '192.168.70.3'
    PORT = 5050
    DIRECT_PORT = 5000
    DB_NAME = 'KOTRABP'
    USER = 'kotrabp'
    PASSWORD = 'kotrabp123'


def handler(sigNum, frame):
    sys.stderr.write('Catch Signal Number : %s \n' % sigNum)
    sys.stderr.flush()
    os.kill(os.getpid(), signal.SIGKILL)


# sigNum 15 : Terminate
signal.signal(signal.SIGTERM, handler)
# sigNum  2 : Keyboard Interrupt
signal.signal(signal.SIGINT, handler)
# sigNum  1 : Hangup detected
try:
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
except:
    pass
# sigNum 13 : Broken Pipe
try:
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except:
    pass


class Client:

    def __init__(self, config_name, direct=False):

        config = globals().get(config_name)

        if direct:
            self.conn = M6.Connection('%s:%s' % (config.HOST, config.DIRECT_PORT), config.USER, config.PASSWORD,
                                      Direct=direct, Database=config.DB_NAME)
        else:
            self.conn = M6.Connection('%s:%s' % (config.HOST, config.PORT), config.USER, config.PASSWORD, Direct=direct,
                                      Database=config.DB_NAME)
        self.curs = self.conn.Cursor()

    def execute(self, sql):

        SUCCESS_FLAG = False

        while not SUCCESS_FLAG:

            try:
                self.curs.Execute2(sql)
                meta_data = self.curs.Metadata()

                data_frame = pd.DataFrame(self.curs)

                if len(data_frame) > 0:
                    data_frame.columns = map(str.lower, meta_data['ColumnName'])

                SUCCESS_FLAG = True

                return data_frame

            except Exception as err:
                if 'locked' in str(err):
                    #__LOG__.Trace("database is locked. sleep 10 sec and try again!")
                    print("database is locked. sleep 10 sec and try again!")
                    time.sleep(10)
                else:
                    raise

    # __LOG__.Trace( 'Done %s sec' % ( time.time() - stime ) )

    def setSep(self, field, record):

        self.curs.SetFieldSep(field)
        self.curs.SetRecordSep(record)

        #__LOG__.Trace('Set field %s, record %s' % (field, record))
        print("database is locked. sleep 10 sec and try again!");

    def load(self, table, key, parttion, ctl, load_file):

        return self.curs.Load(table, key, parttion, ctl, load_file)

    def __del__(self):
        if self.curs: self.curs.Close()
        if self.conn: self.conn.close()


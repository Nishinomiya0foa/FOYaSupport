import sqlite3
import traceback


class Engine:
    def __init__(self, path="data/qqfo.db"):
        self.path = path
        self.engine = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)

    def execute(self, **kwargs):
        query = kwargs['query']
        params = kwargs.get('params')
        res = self.engine.execute(query)
        return res

    def truncate_table(self):
        query = """delete from t_bank;"""
        self.engine.execute(query)
        query = """update sqlite_sequence SET seq = 0 where name ='t_bank';"""
        self.engine.execute(query)

        query = """delete from t_config;"""
        self.engine.execute(query)
        query = """update sqlite_sequence SET seq = 0 where name ='t_config';"""
        self.engine.execute(query)

    def check_table_exist(self, table):
        exist = True
        try:
            query = "select * from {} limit 1".format(table)
        except sqlite3.OperationalError:
            traceback.print_exc()
            exist = False
        return exist

    def update_panel_pot(self, left_top, right_bottom):
        query = "update t_config set left_top = '{}', right_bottom = '{}'".format(str(left_top), str(right_bottom))
        self.engine.execute(query)

    def update_auto_apply(self, auto=1):
        query = "update t_config set auto_apply = '{}'".format(auto)
        self.engine.execute(query)

engine = Engine()

if __name__ == '__main__':
    sql = """create table t_bank(
                              pno INTEGER primary key autoincrement, 
                              ques VARCHAR not null,
                              ans VARCHAR not null
                                    )"""
    # engine.execute(query=sql)
    engine.truncate_table()

import sqlite3
import json
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
            self.engine.execute(query)
        except sqlite3.OperationalError:
            traceback.print_exc()
            exist = False
        return exist

    def batch_update_config(self, params: dict):
        query_part = []
        for k, v in params.items():
            query_part.append(" {} = '{}'".format(k, str(v)))
        query = "update t_config set" + ",".join(query_part)
        print(query)
        self.engine.execute(query)

    def update_auto_apply(self, auto=1):
        query = "update t_config set auto_apply = '{}'".format(auto)
        self.engine.execute(query)

    def update_or_insert(self, pno=0, ques="", ans="", wrong_ans=None):
        if wrong_ans is None:
            wrong_ans = []
        if pno:  # exist
            query = "select * from t_bank where pno = '{}'".format(pno)
            res = self.engine.execute(query).fetchone()
            wrong_ans_origin = res[3]
            wrong: list = json.loads(wrong_ans_origin)
            wrong.extend(wrong_ans)
            wrong_ans = json.dumps(wrong)
            new_query = "update t_bank set ans = '{}', wrong_ans = '{}' where pno = {}".format(ans, wrong_ans, pno)
        else:
            wrong_ans = json.dumps(wrong_ans)
            new_query = "insert into t_bank(ques, ans, wrong_ans) values('{}', '{}', '{}')".format(ques, ans, wrong_ans)
        self.engine.execute(new_query)


engine = Engine()

if __name__ == '__main__':
    sql = """create table t_bank(
                              pno INTEGER primary key autoincrement, 
                              ques VARCHAR not null,
                              ans VARCHAR not null
                                    )"""
    # engine.execute(query=sql)
    # engine.truncate_table()
    # engine.update_or_insert(0, "周星驰no在大陆被称作:", "", ["星哥"])
    # r = engine.execute(query="select * from t_bank where pno = 68896").fetchone()
    # w = r[3]
    # w = json.loads(w)
    # print(w)

    engine.batch_update_config({"left_top": (333,555), "right_bottom": (111,111)})

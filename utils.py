import jieba
import jieba.analyse

from db_handler import engine



def init_database():
    bank_exist = engine.check_table_exist("t_bank")
    if not bank_exist:
        sql = """create table t_bank(
                                  pno INTEGER primary key autoincrement, 
                                  ques VARCHAR not null,
                                  ans VARCHAR,
                                  wrong_ans VARCHAR 
                                        )"""
        engine.execute(query=sql)

    config_exist = engine.check_table_exist("t_config")
    if not config_exist:
        config_sql = """create table t_config(
                                  pno INTEGER primary key autoincrement, 
                                  left_top VARCHAR,
                                  right_bottom VARCHAR,
                                  auto_apply INTEGER
                                        )"""
        engine.execute(query=config_sql)


def init_data(ques, ans, wrong_ans=""):
    sql = "insert into t_bank(ques, ans, wrong_ans) values (\"{}\", \"{}\", \"{}\")".format(ques, ans, wrong_ans)
    engine.execute(query=sql)


def init_config():
    sql = "insert into t_config(auto_apply) values (\"{}\")".format(1)
    engine.execute(query=sql)


def init_all_data(file_url):
    count = 0
    print("start initial base data...")
    with open(file_url,"r", encoding="gb18030") as f:
        for line in f.readlines():
            if len(line.split("\",\"")) == 3:
                line_list = line.split("\",\"")[:2]
                ques = line_list[0].strip("\"")
                ans = line_list[1]
                init_data(ques, ans)
                count += 1
                if count % 1000 == 0:
                    print("have initial {} datas".format(count))

    print("start initial config...")
    init_config()


def handle_words(res):
    words = res.get("words_result")
    words_r = "".join([r.get("words") for r in words])
    return words_r


def search_related_records(word_list):
    params = "%"
    for word in word_list:
        params += word[:3]
        params += "%"
    print(params)
    sql = "select * from t_bank where ques like '{}'".format(params)
    res = engine.execute(query=sql).fetchall()
    print(res)
    return res


def get_keywords(content):
    tags = jieba.analyse.extract_tags(content, topK=10)  # error sorted

    tags = list(tags)
    tags.sort(key=lambda x: content.index(x))
    return list(tags)


def get_user_config():
    config_exist = engine.check_table_exist("t_config")
    if config_exist:
        config_exist = config = engine.execute(query="select * from t_config limit 1").fetchone()
    return config_exist


if __name__ == '__main__':
    # init_database()
    # print(engine.execute(query="select count(1) from t_bank").fetchall())
    # sql = "select * from t_bank where ques like \"%皮肤哪一部分受损%\""
    # print(engine.execute(query=sql).fetchall())
    ...

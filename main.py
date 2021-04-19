import re
import json
import time

from utils import init_database,  init_all_data, handle_words, search_related_records, get_keywords, get_user_config
from pic_handler import pic_handle
from related_words import get_equal_rate
from db_handler import engine
from gui_printer import window


filt_path = "data/qqfo.dat"
pic_path = "data/test_pic.png"


def set_pic_area(left_top="", right_bottom=""):
    query = "insert into t_config(left_top, right_bottom) values ({}, {})".format(left_top, right_bottom)
    print(query)
    engine.execute(query=query)


def add_unknown_record():
    ...


def initial():
    ...



def main():

    # TODO 判断节选到的是有效字符

    # get user config
    user_config_exist = get_user_config()
    if not user_config_exist:
        print("initial database")
        init_database()
        print("table not exist, initialing tables")
        init_all_data(filt_path)
    else:
        pno, left_top, right_bottom, auto_apply = user_config_exist
        print("left_top", left_top)
        print("right_bottom", right_bottom)
        print("auto_apply", auto_apply)

        # set_pic_area(new_left_top, new_right_bottom)

    raise

    r = pic_handle(pic_path)
    # r = 1
    if r:
        res: dict = r.json()
        words_content = handle_words(res)
        # words_content = "海"

        keywords = get_keywords(words_content)
        print(keywords)
        data_res = search_related_records(keywords)
        print(data_res)
        if len(data_res) == 1:
            real_ans = data_res[0][2]
        elif len(data_res) == 0:
            # TODO add
            real_ans = "题目可能未收录"
        else:
            similar = 0
            final_index = 0
            for index, r in enumerate(data_res):
                tmp = get_equal_rate(words_content, r[1])
                if tmp > similar:
                    similar = tmp
                    final_index = index
            real_ans = data_res[final_index][2]
        print(real_ans)


def app():
    window.show()


if __name__ == '__main__':
    main()
    ...


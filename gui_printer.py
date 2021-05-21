import PySimpleGUI as sg
import json
import time

from utils import init_database,  init_all_data, handle_words, search_related_records, get_keywords, get_user_config
from db_handler import engine
from screan_getter import grab_screen
from pic_handler import pic_handle, get_key
from related_words import get_equal_rate, get_the_most_similar
from monitor import get_panel_size, mouse_click_
from const import ConstCode


filt_path = "data/qqfo.dat"
pic_path = "data/test_pic.png"


def auto_choose_answer(wrong_answer: str, ans_content: list):
    if wrong_answer:
        wrong_answer: list = json.loads(wrong_answer)
    else:
        wrong_answer = []

    # 找到其中不在错题中出现的那个答案, 也就是相似度最低的
    similar_list = []
    for ind in range(len(ans_content)):
        words, index, similar = get_the_most_similar(ans_content[ind], wrong_answer, need_similar=True)
        similar_list.append({similar: ind+1})
    similar_list.sort(key=lambda d: list(d.keys())[0], reverse=False)
    return list(similar_list[0].values())[0]


class MyWindow():
    def __init__(self, title):
        self.pic_area_btn = sg.Button("问题区域")
        self.left_top = sg.Text("")
        self.right_bottom = sg.Text("")

        self.ans_area_btn = sg.Button("答案区域")
        self.left_top_ans = sg.Text("")
        self.right_bottom_ans = sg.Text("")

        self.ans_click_1_btn = sg.Button("选项1")
        self.ans_click_1 = sg.Text("")
        self.ans_click_2_btn = sg.Button("选项2")
        self.ans_click_2 = sg.Text("")
        self.ans_click_3_btn = sg.Button("选项3")
        self.ans_click_3 = sg.Text("")
        self.ans_click_4_btn = sg.Button("选项4")
        self.ans_click_4 = sg.Text("")

        self.choose_text = sg.Text("是否自动作答:")
        self.auto_apply_Y = sg.Radio("是:", "1", change_submits=True)
        self.auto_apply_N = sg.Radio("否:", "1", change_submits=True)
        self.output_area = sg.Output((50, 5))
        self.output_text = sg.Text("shuchu", size=(60, 7), text_color="red")
        self.clear_btn = sg.Button("clear")
        self.start_btn = sg.Button("start")
        self.stop_btn = sg.Button("stop", disabled=True)
        self.auto_apply = 1
        self.init_data()
        self.layout = [[self.pic_area_btn, self.left_top, self.right_bottom],
                       [self.ans_area_btn, self.left_top_ans, self.right_bottom_ans],
                       [self.ans_click_1_btn, self.ans_click_1, self.ans_click_2_btn, self.ans_click_2],
                       [self.ans_click_3_btn, self.ans_click_3, self.ans_click_4_btn, self.ans_click_4],
                       [self.choose_text, self.auto_apply_Y, self.auto_apply_N],
                       [self.start_btn, self.stop_btn],
                       # [self.output_area, self.clear_btn]
                       ]
        print(self.layout[0][1].get())

        self.window = sg.Window(title, self.layout, keep_on_top=True)

    def init_data(self):
        user_config_exist = get_user_config()
        if not user_config_exist:
            print("initial database")
            init_result = init_database()
            print("table not exist, initialing tables")
            init_all_data(filt_path, init_result)
        else:
            pno, left_top_pot, right_bottom_pot, auto_apply, left_top_ans, right_bottom_ans, \
                ans_1, ans_2, ans_3, ans_4 = user_config_exist
            self.left_top = sg.Text(left_top_pot, size=ConstCode.TEXT_SIZE)
            self.right_bottom = sg.Text(right_bottom_pot, size=ConstCode.TEXT_SIZE)
            if auto_apply:
                self.auto_apply_Y = sg.Radio("是:", "1", default=True, change_submits=True)  # 0
            else:
                self.auto_apply_N = sg.Radio("否:", "1", default=True, change_submits=True)  # 1
            self.auto_apply = auto_apply
            self.left_top_ans = sg.Text(left_top_ans, size=ConstCode.TEXT_SIZE)
            self.right_bottom_ans = sg.Text(right_bottom_ans, size=ConstCode.TEXT_SIZE)
            self.ans_click_1 = sg.Text(ans_1, size=ConstCode.TEXT_SIZE)
            self.ans_click_2 = sg.Text(ans_2, size=ConstCode.TEXT_SIZE)
            self.ans_click_3 = sg.Text(ans_3, size=ConstCode.TEXT_SIZE)
            self.ans_click_4 = sg.Text(ans_4, size=ConstCode.TEXT_SIZE)

    def find_position_by_index(self, index):
        index = min(index, 4)
        ans_click_obj = getattr(self, "ans_click_"+str(index))
        return ans_click_obj.get()

    def apply_(self, p1, p2, key):
        grab_screen(p1, p2)
        r = pic_handle("data/test.png", key)
        if r:
            res = r
            print(res)
            ques_content, ans_content = handle_words(res)
            keywords = get_keywords(ques_content)
            data_res = search_related_records(keywords)
            print(data_res, "data_res", len(data_res))

            if len(data_res) >= 1:  # 数据库中存在该题目
                real_ans, final_index = get_the_most_similar(ques_content, [r[1] for r in data_res])
                real_ans = data_res[final_index][2]
                pno = data_res[final_index][0]
                if real_ans:  # find correct answer
                    given_ans, index = get_the_most_similar(real_ans, ans_content)
                    position: str = self.find_position_by_index(index+1)
                    print(real_ans)
                    if self.auto_apply:
                        mouse_click_(position)
                else:  # not find correct answer but find wrong answer
                    wrong_ans = data_res[final_index][3]
                    print("题目尚无正确答案,进行随即作答")
                    index = auto_choose_answer(wrong_ans, ans_content)
                    print("index: ", index)
                    position = self.find_position_by_index(index)
                    mouse_click_(position)
                    wrong_ans = json.loads(wrong_ans)
                    correct = sg.popup_yes_no("选择对了吗?", keep_on_top=True)
                    if correct == "Yes":
                        engine.update_or_insert(pno=pno, ques=ques_content, ans=ans_content[len(wrong_ans)])
                    else:
                        engine.update_or_insert(pno=pno, ques=ques_content, wrong_ans=[ans_content[len(wrong_ans)]])

            else:  # 未收录的情况进行顺序作答,记录正确错误
                print("题目可能未收录, 进行随机作答")
                real_ans = ""
                # index = self.auto_choose_answer("", ans_content)
                position = self.find_position_by_index(1)
                mouse_click_(position)
                correct = sg.popup_yes_no("选择对了吗?", keep_on_top=True)  # 百度文字识别每日字数限制,这里选择手动识别
                if correct == "Yes":
                    engine.update_or_insert(ques=ques_content, ans=ans_content[0])  # first time apply 0
                else:
                    engine.update_or_insert(ques=ques_content, wrong_ans=ans_content[:1])  # wrong_ans must be a list
            print(real_ans)
            # return real_ans

    def show(self):
        key = get_key()
        while True:
            event, values = self.window.read()
            print(event, values)
            if event in ["问题区域"]:
                self.left_top.update(get_panel_size(desc="题目左上角"))
                self.right_bottom.update(get_panel_size(desc="题目右下角"))
                engine.batch_update_config({"left_top": self.left_top.get(),
                                            "right_bottom": self.right_bottom.get()})
            elif event in ["选项1", "选项2", "选项3", "选项4"]:
                ans_pot_obj: sg.Text = getattr(self, "ans_click_"+event[-1])
                ans_pot_obj.update(get_panel_size(desc="答案第{}个选项处".format(event[-1])))
                engine.batch_update_config({"ans_"+event[-1]: ans_pot_obj.get()})

            elif event in ["答案区域"]:
                self.left_top_ans.update(get_panel_size(desc="答案区域左上角"))
                self.right_bottom_ans.update(get_panel_size(desc="答案区域右下角"))
                engine.batch_update_config({"left_top_ans": self.left_top_ans.get(),
                                            "right_bottom_ans": self.right_bottom_ans.get()})
            elif event in [0]:  # auto-apply
                engine.update_auto_apply(1)
                self.auto_apply = 1
            elif event in [1]:  # hand-apply
                engine.update_auto_apply(0)
                self.auto_apply = 0
            elif event in ["clear"]:
                self.output_text.update("")
            elif event in ["start"]:
                self.start_btn.update(disabled=True)
                self.stop_btn.update(disabled=False)
                p1_origin_ques_left_top = self.left_top.get().split(",")
                # p2_origin = self.right_bottom.get().split(",")
                # TODO get whole ques_area and ans_area
                p2_origin_ans_right_bottom = self.right_bottom_ans.get().split(",")
                p1, p2 = tuple(int(x) for x in p1_origin_ques_left_top), tuple(int(y) for y in p2_origin_ans_right_bottom)
                self.apply_(p1, p2, key)
            elif event in ["stop"]:
                self.stop_btn.update(disabled=True)
                self.start_btn.update(disabled=False)

            elif event in [None]:
                break
        self.window.close()


if __name__ == '__main__':
    window = MyWindow("apply")
    window.show()
    # print(1 >> 0)
    # print(0 >> 0)
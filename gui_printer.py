import PySimpleGUI as sg
import time
from threading import Thread, Timer

from utils import init_database,  init_all_data, handle_words, search_related_records, get_keywords, get_user_config
from db_handler import engine
from screan_getter import grab_screen
from pic_handler import pic_handle, get_key
from related_words import get_equal_rate
from monitor import get_panel_size


filt_path = "data/qqfo.dat"
pic_path = "data/test_pic.png"



def apply_(p1, p2, key):
    grab_screen(p1, p2)
    r = pic_handle("data/test.png", key)
    if r:
        res = r
        print(res)
        words_content = handle_words(res)
        keywords = get_keywords(words_content)
        print(keywords)
        data_res = search_related_records(keywords)

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
        return real_ans


class MyWindow():
    def __init__(self, title):
        self.pic_area_btn = sg.Button("选择区域")
        self.left_top = sg.Text("123")
        self.right_bottom = sg.Text("456")
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
                       [self.choose_text, self.auto_apply_Y, self.auto_apply_N],
                       [self.start_btn, self.stop_btn],
                       [self.output_area, self.clear_btn]
                       ]
        print(self.layout[0][1].get())

        self.window = sg.Window(title, self.layout, keep_on_top=True)

    def init_data(self):
        user_config_exist = get_user_config()
        if not user_config_exist:
            print("initial database")
            init_database()
            print("table not exist, initialing tables")
            init_all_data(filt_path)
        else:
            pno, left_top_pot, right_bottom_pot, auto_apply = user_config_exist
            self.left_top = sg.Text(left_top_pot)
            self.right_bottom = sg.Text(right_bottom_pot)
            if auto_apply:
                self.auto_apply_Y = sg.Radio("是:", "1", default=True, change_submits=True)  # 0
            else:
                self.auto_apply_N = sg.Radio("否:", "1", default=True, change_submits=True)  # 1
            self.auto_apply = auto_apply

    def show(self):
        key = get_key()
        while True:
            event, values = self.window.read()
            print(event)
            if event in ["选择区域"]:
                self.left_top.update(get_panel_size(position="left_top"))
                self.right_bottom.update(get_panel_size(position="right_bottom"))
                engine.update_panel_pot(self.left_top.get(), self.right_bottom.get())
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
                # TODO main process
                p1_origin = self.left_top.get().split(",")
                p2_origin = self.right_bottom.get().split(",")
                p1, p2 = tuple(int(x) for x in p1_origin), tuple(int(y) for y in p2_origin)
                # t = Thread(target=apply_, args=(p1, p2, ))
                # t.setDaemon(True)
                # t.start()
                # t.join()
                res = apply_(p1, p2, key)
                print(res)
            elif event in ["stop"]:
                self.stop_btn.update(disabled=True)
                self.start_btn.update(disabled=False)
                # TODO main process

            elif event in [None]:
                break
        self.window.close()


if __name__ == '__main__':
    window = MyWindow("apply")
    window.show()
    # print(1 >> 0)
    # print(0 >> 0)
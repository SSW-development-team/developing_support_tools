import PySimpleGUI as sg
import glob
import shutil
import re

Bar_MAX = 5

sg.theme("Default1")
layout = [
    [sg.Text("テキスト作成対象",size=(15,1)),sg.Input(), sg.FileBrowse("ファイルを選択", key="inputFilePath")],
    [sg.Frame("行",[
        [sg.Text("開始行",size=(6,1)), sg.InputText(default_text="0",key="start_line",size=(8,1))],
        [sg.Text("終了行",size=(6,1)), sg.InputText(default_text="0",key="end_line",size=(8,1))]
    ])],
    [sg.Frame("モード",[
        [sg.Radio("focus",group_id="mode_set",default=True,key="focus_mode")],
        [sg.Radio("event",group_id="mode_set",key="event_mode")]
    ])],
    [sg.Button("実行",key="do_button",button_color=("white","blue"))],
    [sg.Output(size=(80,20),key="out_block")]
]

window = sg.Window("Localization maker",layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "do_button":
        if values["inputFilePath"] == "":
            sg.popup_error("テキスト作成対象のファイルが指定されていません",title="エラー")
        elif (not re.search(r'[0-9]',values["start_line"][-1])) or (not re.search(r'[0-9]',values["end_line"][-1])):
            sg.popup_error("いずれかの行数入力が数字ではありません",title="エラー")
        elif (int(values["start_line"]) < 0 or int(values["start_line"]) == 0 or int(values["end_line"]) < 0 or int(values["end_line"]) == 0):
            sg.popup_error("いずれかの行数入力が負の数もしくは0です",title="エラー")
        elif (int(values["start_line"]) > int(values["end_line"]) or int(values["start_line"]) == int(values["end_line"])):
            sg.popup_error("開始位置が終了位置より後ろ、もしくは等しいです",title="エラー")
        else:
            window["out_block"].update("")
            start_line = int(values["start_line"])
            end_line = int(values["end_line"])
            fi = open(values["inputFilePath"],"r",encoding='UTF-8')
            line_list = fi.readlines()
            if values["focus_mode"]:
                #fo = open("./outputfile_goal.txt","w")
                target_index = 0
                targetting = False
                loc_text = ""
                for i in range(start_line-1,end_line):
                    if (not targetting):
                        target_index = line_list[i].find("focus = { #")
                        if (target_index == -1):
                            target_index = line_list[i].find("focus = {#")
                            if (target_index == -1):
                                continue
                            else:
                                targetting = True
                                target_index += 10
                        else:
                            targetting = True
                            target_index += 11
                        loc_text = line_list[i][target_index:-1]
                    else:
                        target_index = line_list[i].find("id = ")
                        if (target_index == -1):
                            continue
                        else:
                            targetting = False
                        target_index += 5
                        print(' ' + line_list[i][target_index:-1] + ':0 "' + loc_text + '"')
                        print(' ' + line_list[i][target_index:-1] + '_desc:0 ""')
                #fo.write(window.find_element("out_block").Get())
                #fo.close()
            elif values["event_mode"]:
                target_index = 0
                targetting = False
                loc_text = []
                loc_key = []
                for i in range(start_line-1,end_line):
                    if (targetting and (len(line_list[i]) == 2 or line_list[i] == "}")):
                        for j in range(len(loc_text)):
                            print(' ' + loc_key[j] + ':0 "' + loc_text[j] + '"')
                        loc_text.clear()
                        loc_key.clear()
                        targetting = False
                    if (not targetting):
                        target_index = line_list[i].find("country_event = { #")
                        if (target_index == -1):
                            target_index = line_list[i].find("country_event = {#")
                            if (target_index == -1):
                                target_index = line_list[i].find("news_event = { #")
                                if (target_index == -1):
                                    target_index = line_list[i].find("news_event = {#")
                                    if (target_index == -1):
                                        continue
                                    else:
                                        targetting = True
                                        target_index += 15
                                else:
                                    targetting = True
                                    target_index += 16
                            else:
                                targetting = True
                                target_index += 18
                        else:
                            targetting = True
                            target_index += 19
                        loc_text.append(line_list[i][target_index:-1])
                    else:
                        target_index = line_list[i].find("title = ")
                        if (target_index != -1):
                            target_index += 8
                            loc_key.insert(0,line_list[i][target_index:-1])
                        target_index = line_list[i].find("desc = ")
                        if (target_index != -1):
                            target_index += 7
                            loc_key.append(line_list[i][target_index:-1])
                            loc_text.append("")
                        target_index = line_list[i].find("option = { #")
                        if (target_index != -1):
                            target_index += 12
                            loc_text.append(line_list[i][target_index:-1])
                        else:
                            target_index = line_list[i].find("option = {#")
                            if (target_index != -1):
                                target_index += 11
                                loc_text.append(line_list[i][target_index:-1])
                        target_index = line_list[i].find("name = ")
                        if (target_index != -1):
                            target_index += 7
                            loc_key.append(line_list[i][target_index:-1])
            sg.popup("処理が完了しました",title="インフォ")

window.close()
import PySimpleGUI as sg
import glob
import shutil

Bar_MAX = 5

sg.theme("Default1")
layout = [
    [sg.Text("元画像フォルダパス",size=(13,1)),sg.Input(), sg.FolderBrowse("フォルダを選択", key="inputFolderPath")],
    [sg.Text("gfxフォルダパス\n",size=(13,1)),sg.Input(),sg.FolderBrowse("フォルダを選択", key="outputFolderPath")],
    [sg.Text("接頭字(name)",size=(10,1)),sg.InputText('', size=(10, 1), key='head'),sg.Text("接頭字(file)",size=(10,1)),sg.InputText('', size=(10, 1), key='head_f')],
    [sg.Text("接尾字(name)",size=(10,1)),sg.InputText('', size=(10, 1), key='tail'),sg.Text("接尾字(file)",size=(10,1)),sg.InputText('', size=(10, 1), key='tail_f')],
    [sg.Frame("ファイル形式",[
        [sg.Checkbox("png",default=True,key="check_png")],
        [sg.Checkbox("jpg",default=False,key="check_jpg")],
        [sg.Checkbox("dds",default=True,key="check_dds")],
        [sg.Checkbox("gif",default=False,key="check_gif")]
    ]),
    sg.Frame("出力形式",[
        [sg.Text("name = 接頭字(name) + 接頭字(file) + ファイル名 + 接尾字(file) + 接尾字(name)")],
        [sg.Text("texturefile = gfxパス + 接頭字(file) + ファイル名 + 接尾字(file) + 拡張子")]
    ])
    ],
    [sg.Frame("完了後の設定",[
        [sg.Radio("元ファイルを削除する(移動)",group_id="setting",key="set_delete")],
        [sg.Radio("元ファイルを残す(コピー)",group_id="setting",default=True,key="set_copy")],
        [sg.Checkbox("テキストファイルの出力(既に出力ファイルがある時、上書きされます。)",default=False,key="text_output_setting")]
    ])],
    [sg.Button("実行",key="do_button",button_color=("white","blue"))],
    [sg.Output(size=(80,20),key="out_block")]
]

window = sg.Window("GFX Outputter",layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "do_button":
        if values["inputFolderPath"] == "" or values["outputFolderPath"] == "":
            sg.popup_error("元画像フォルダ、またはgfxフォルダのパスが指定されていません",title="エラー")
        elif not "gfx" in values["outputFolderPath"]:
            sg.popup_error("/gfx/を含むパスを指定してください",title="エラー")
        else:
            window["out_block"].update("")
            in_path = values["inputFolderPath"]
            out_path = values["outputFolderPath"]
            if values["check_png"]:
                files_png = glob.glob(in_path+"/*.png")
            else:
                files_png = []
            if values["check_jpg"]:
                files_jpg = glob.glob(in_path+"/*.jpg")
            else:
                files_jpg = []
            if values["check_dds"]:
                files_dds = glob.glob(in_path+"/*.dds")
            else:
                files_dds = []
            if values["check_gif"]:
                files_gif = glob.glob(in_path+"/*.gif")
            else:
                files_gif = []
            files = []
            files.extend(files_png)
            files.extend(files_jpg)
            files.extend(files_dds)
            files.extend(files_gif)
            if len(files) == 0:
                sg.popup_error("対象となるファイルが存在しません",title="エラー")
                continue
            print("spriteTypes = {")
            head_tex = values["head"]
            head_tex_f = values["head_f"]
            tail_tex = values["tail"]
            tail_tex_f = values["tail_f"]
            out_path_short = out_path[out_path.index("gfx"):]
            for i in range(len(files)):
                if values["set_delete"]:
                    shutil.move(files[i],out_path+"/"+head_tex_f+files[i][len(in_path)+1:-4]+tail_tex_f+files[i][-4:])
                elif values["set_copy"]:
                    shutil.copy2(files[i],out_path+"/"+head_tex_f+files[i][len(in_path)+1:-4]+tail_tex_f+files[i][-4:])
                print("    SpriteType = {")
                print('        name = "{:s}"'.format(head_tex + head_tex_f + files[i][len(in_path)+1:-4]+tail_tex_f+tail_tex))
                print('        texturefile = "{:s}"'.format(out_path_short + "/" +head_tex_f+files[i][len(in_path)+1:-4]+tail_tex_f+files[i][-4:]))
                print("    }")
            print("}")
            if values["text_output_setting"]:
                f = open(in_path+"/outputfile.txt","w")
                f.write(window.find_element("out_block").Get())
                f.close()
            sg.popup("処理が完了しました",title="インフォ")

window.close()
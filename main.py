# -*- coding= utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pywinauto.application import Application
from pywinauto import clipboard # 채팅창내용 가져오기 위해

from time import sleep
from datetime import datetime
from dateutil.parser import parse
import re

def extract_chat(raw_text):
    line_text = raw_text.replace('\r', '').split('\n')
    date_reg = re.compile(r'^(\d{2,4})년 ?(\d{1,2})월 ?(\d{1,2})일 ?\w요일')
    join_reg = re.compile(r'^.+님이 들어왔습니다')
    out_reg = re.compile(r'^.+님이 나갔습니다')
    msg_reg = re.compile(r'^\[(.+)\] ?\[(.+)\] ?(.+)')

    date = datetime.now().strftime("%Y-%m-%d")

    msg = {"user":"", "time":"", "msg":""}
    proceed = []
    for line in line_text:
        if date_reg.search(line):
            els = date_reg.search(line).groups()
            date = parse(f'{els[0]}-{els[1]}-{els[2]}').strftime("%Y-%m-%d")
        elif join_reg.search(line) or out_reg.search(line):
            continue
        elif msg_reg.search(line):
            els = msg_reg.search(line).groups()
            time_str = els[1].split(' ')
            msg_time = time_str[1]

            ch_time = time_str[1].split(':')
            if time_str[0] == '오후' and int(ch_time[0]) < 12:
                hour = int(ch_time[0]) + 12
                msg_time = ':'.join([str(hour), ch_time[1]])

            msg = {"user": els[0], "time": f"{date} {msg_time}", "msg": els[2]}
            proceed.append(msg)
        else:
            msg["msg"] += f'\n{line}'
    return proceed


if __name__ == "__main__":
    app_path = "C:\\Program Files (x86)\\Kakao\\KakaoTalk\\KakaoTalk.exe"
    app = Application(backend="win32").connect(path=app_path)
    kakao_chatroom_list = app.windows(title_re=".*리니지2[mM].*")

    chat_list = {}
    for kakao_chat in kakao_chatroom_list:
        room_name = kakao_chat.element_info.name
        chat_list[room_name] = []
        chat = [c for c in kakao_chat.Children() if c.element_info.class_name == 'EVA_VH_ListControl_Dblclk'][0]
        chat.type_keys("^a^c")
        sleep(0.1)
        raw_text = clipboard.GetData()
        chat_text = extract_chat(raw_text)
        chat_list[room_name] = chat_text
        print(chat_text)

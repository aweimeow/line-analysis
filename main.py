#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re


def line_type(line):
    content = re.match('(\d{2}:\d{2})\t(.*)\t(.*)', line)
    if content:
        dic = {'date': '', 'time': content.group(1), 
                'name': content.group(2), 'content': content.group(3)}
        return ('content', dic)

    datestamp = re.match('^(\d{4}\/\d{2}\/\d{2})\((週.)\)', line)
    if datestamp:
        return('datestamp', datestamp.group(1), datestamp.group(2))

    invite = re.match('(\d{2}:\d{2})\t(.*)邀請(.*)加入群組。', line)
    if invite:
        dic = {'date': '', 'time': invite.group(1), 
                'inviter': invite.group(2), 'target': invite.group(3)}
        return('invite', dic)

    title = re.match('\[LINE\] (.*)的聊天記錄', line)
    if title:
        return ('title', title.group(1))

    save_date = re.match('儲存日期：(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2})', line)
    if save_date:
        return ('save_date', save_date.group(1))

    if line.strip() == "":
        return ('empty', line)

    return ('multiline', line)
    

def load_file(fname):
    date = str()
    who = str()
    with open(fname, 'r') as f:
        for line in f:
            print(line_type(line))

if __name__ == '__main__':
    load_file('chat_tmp.txt')

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re


def line_type(line):
    """    
    seperate line's msg into many type
    content: normal text
    multiline: is part of last content, because we split log by \n
    datestamp: date for following message
    invite: someone invite others into group
    join: the one was invited join group
    title: Group's name
    savedate: the date user saved log
    """
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
        return ('invite', dic)

    join = re.match('(\d{2}:\d{2})\t(.*)加入聊天', line)
    if join:
        dic = {'date': '', 'time': join.group(1), 'name': join.group(2)}
        return ('join', dic)

    title = re.match('\ufeff\[LINE\] (.*)的聊天記錄', line)
    if title:
        return ('title', title.group(1))

    save_date = re.match('儲存日期：(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2})', line)
    if save_date:
        return ('save_date', save_date.group(1))

    if line.strip() == "":
        return ('empty', line)

    return ('multiline', line)
    

def load_file(fname):
    dic = None
    date = None
    who = str()
    namelog = dict()
    with open(fname, 'r') as f:
        for line in f:
            linetype = line_type(line)
            print(linetype)

            if linetype[0] == 'content':
                dic = linetype[1]
                dic['date'] = date[0]
                if not dic['name'] in namelog:
                    namelog[dic['name']] = list()
                who = dic['name']
                dic.pop('name')
                namelog[who].append(dic)
                continue

            if linetype[0] == 'multiline':
                dic['content'] += linetype[1]

            if linetype[0] == 'datestamp':
                date = (linetype[1], linetype[2])
                continue

    print(namelog)

if __name__ == '__main__':
    load_file('chat_tmp.txt')

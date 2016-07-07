#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sys
import json
import code
import jieba

from models import Content, Invite

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
    content_r = re.match('(\d{2}:\d{2})\t(.*?)\t(.*?)', line)
    if content_r:
        time = content_r.group(1)
        name = content_r.group(2)
        text = content_r.group(3)
        content = Content(time, name, text)
        return content

    datestamp_r = re.match('^(\d{4}\/\d{2}\/\d{2})\((週.)\)', line)
    if datestamp_r:
        return('datestamp', datestamp_r.group(1), datestamp_r.group(2))

    invite_r = re.match('(\d{2}:\d{2})\t(.*)邀請(.*)加入群組。', line)
    if invite:
        time = invite_r.group(1)
        inviter = invite_r.group(2)
        invitee = invite_r.group(3)
        invite = Invite(time, inviter, invitee)
        return invite

    join = re.match('(\d{2}:\d{2})\t(.*)加入聊天', line)
    if join:
        dic = {'time': join.group(1), 'name': join.group(2)}
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
    """ parsing log file """
    dic = None
    date = None
    who = str()
    namelog = dict()
    joinbydate = dict()
    with open(fname, 'r') as f:
        for line in f:
            linetype = line_type(line)

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
                continue

            if linetype[0] == 'datestamp':
                date = (linetype[1], linetype[2])
                continue

            if linetype[0] == 'join':
                if not date[0] in joinbydate:
                    joinbydate[date[0]] = list()
                joinbydate[date[0]].append(linetype[1])

    return namelog

def sortpercent(namelog):
    name_rate_d = dict()
    chat_count = 0
    for name in namelog:
        name_rate_d[name] = {'rate': 0, 'count': len(namelog[name])}
        chat_count += len(namelog[name])

    for name in name_rate_d:
        name_rate_d[name]['rate'] = '%2.2f%%' % (
        name_rate_d[name]['count'] / chat_count * 100 )

    return name_rate_d

def sort(name_rate_d):
    sort_d = sorted(name_rate_d.items(), key=lambda x: x[1]['count'])
    sort_d.reverse()
    return sort_d

def output_sort(sort_d):
    for item in sort_d:
        namelen = 0
        for i in item[0]:
            if re.match('[a-zA-Z0-9!@#$%^&*()]', i):
                namelen += 1
            else:
                namelen += 2
        namelen = namelen // 2
        print('%s' % item[0] + '\t' * ((15-namelen) // 4), end='')
        print('%s\t%s' % (item[1]['count'], item[1]['rate']))
    print(len(sort_d))

def load_json(fname):
    f = open(fname, 'r')
    return json.loads(f.read())

def pre_load_name(name_l):
    for name in name_l:
        jieba.add_word(name)

def cut_word(talks):
    ret_d = dict()
    for talk in talks:
        seg = jieba.cut(talk, cut_all=False)
        for word in set(seg):
            if not word in ret_d:
                ret_d[word] = 0
            ret_d[word] += 1

    empty_keys = [k for k, v in ret_d.items() if v < 10]
    for k in empty_keys:
        del ret_d[k]

    return ret_d

def analysis_word(namelog):
    name_word_feq = dict()
    for name in namelog:
        print("cutting: %s" % name)
        talks = [t['content'] for t in namelog[name]]
        talks = cut_word(talks)
        name_word_feq[name] = talks

    return name_word_feq

def main():
    """
    fname: file name
    namelog: parse log file
    namelist: enhance name
    """
    fname = sys.argv[1]
    #namelist = sys.argv[2]

    # Sorting Rank
    namelog = load_file(fname)
    name_rate_d = sortpercent(namelog)
    sort_d = sort(name_rate_d)
    output_sort(sort_d)

    # Analysis word
    #pre_load_name(load_json(namelist))
    #name_word_feq = analysis_word(namelog)
    #code.interact(local=locals())

if __name__ == '__main__':
    main()

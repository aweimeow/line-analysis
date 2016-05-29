#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re


def line_type(line):
	content = re.match('(\d{2}:\d{2})\t(.*)\t(.*)', line)
	if content:
		dic = {'date': '', 'time': content.group(1), 
				'name': content.group(2), 'content': content.group(3)}
		return ('content', dic)

	title = re.match('\[LINE\] (.*)的聊天紀錄', line)
	if title:
		return ('title', title.group(1))
	save_date = re.match('儲存日期：(\d{4}\/\d{2}\/d{2} \d{2}:\d{2})')
	if save_date:
		return ('save_date', save_date.group(1))
	# multi-content, datestamp not done


def load_file(fname):
	date = str()
	who = str()
	with open(fname, 'r') as f:
		for line in f:
		

if __name__ == '__main__':
	load_file('chat.txt')

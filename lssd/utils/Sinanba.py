#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/18.
from bs4 import BeautifulSoup
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

@staticmethod
def get_nba_data(year, month, day):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    r = requests.get(
        'http://nba.sports.sina.com.cn/live.php?years={0}&months={1}&days={2}&Submit=%B2%E9%D1%AF'.format(year, month,
                                                                                                          day),
        headers=header)
    r.encoding = 'gbk'
    all_text = r.text

    soup = BeautifulSoup(all_text, 'lxml')
    # print soup.find_all('table')[1]
    # 筛选出所有符合条件的table
    all_tables = []
    for table in soup.find_all('table'):
        # print table
        # print table.get('align')
        if table.get('align') == 'center' and table.get('width') == '350' and table.get(
                'border') == '0' and table.get('cellpadding') == '0' and table.get('cellspacing') == '0':
            all_tables.append(table)
    todays_all_match = len(all_tables)
    all_match_infos = []
    for table in all_tables:
        # 获取第一个球队的信息,队名和总得分
        tr1 = table.tr.td.table.find_all('tr')[1]
        for td in tr1.find_all('td'):
            if td.get('height') == '20' and td.get('style') == 'padding-left:10px':
                first_name = td.get_text()
            if td.b:
                first_score = td.b.get_text()
        # 获取第二个球队的信息,队名和总得分
        tr2 = table.tr.td.table.find_all('tr')[2]
        for td in tr2.find_all('td'):
            if td.get('height') == '20' and td.get('style') == 'padding-left:10px':
                second_name = td.get_text()
            if td.b:
                second_score = td.b.get_text()
        match = {'match': first_name + ':' + second_name, 'score': first_score + ':' + second_score}
        all_match_infos.append(match)
    return all_match_infos


if __name__ == '__main__':
    print get_nba_data()

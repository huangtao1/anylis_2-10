#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/18.
from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime
from aip import AipSpeech
from config import Config
import os
from Mydb import Mydb
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def get_nba_data(year, month, day):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    r = requests.get(
        'http://nba.sports.sina.com.cn/live.php?years={0}&months={1}&days={2}&Submit=%B2%E9%D1%AF'.format(year, month,
                                                                                                          day),
        headers=header)
    r.encoding = 'gb2312'
    all_text = r.text

    soup = BeautifulSoup(all_text, 'lxml')
    # 筛选出所有符合条件的table
    all_tables = []
    for table in soup.find_all('table'):
        if table.get('align') == 'center' and table.get('width') == '350' and table.get(
                'border') == '0' and table.get('cellpadding') == '0' and table.get('cellspacing') == '0':
            all_tables.append(table)
    all_match_infos = []
    for table in all_tables:
        # 获取第一个球队的信息,队名和总得分
        tr1 = table.tr.td.table.find_all('tr')[1]
        for td in tr1.find_all('td'):
            if td.get('height') == '20' and td.get('style') == 'padding-left:10px':
                first_name = td.get_text()
                print first_name
            if td.b:
                first_score = td.b.get_text()
        # 获取第二个球队的信息,队名和总得分
        tr2 = table.tr.td.table.find_all('tr')[2]
        for td in tr2.find_all('td'):
            if td.get('height') == '20' and td.get('style') == 'padding-left:10px':
                second_name = td.get_text()
            if td.b:
                second_score = td.b.get_text()
        match = {'match': first_name + ':' + second_name,
                 'score': first_score + ':' + second_score}
        all_match_infos.append(match)
    all_info = json.dumps(all_match_infos)
    print all_match_infos
    print all_info
    mydb = Mydb(host='104.156.251.60', user_name='root', password='huangtao123689', db_name='lssd')
    # 查询是否有记录,有就更新,没有就添加
    search_sql = "SELECT * FROM lssd_nba_daily WHERE competing_time='{0}'".format('-'.join([year, month, day]))
    if mydb.serach_info(search_sql, count='one'):
        update_sql = "UPDATE lssd_nba_daily SET today_content='{0}' WHERE competing_time='{1}'".format(all_info,
                                                                                                       '-'.join(
                                                                                                           [year, month,
                                                                                                            day]))
        mydb.update_data(update_sql)
    else:
        insert_sql = "INSERT INTO lssd_nba_daily(competing_time,today_content) VALUES('{0}','{1}')".format(
            '-'.join([year, month, day]), all_info)
        mydb.insert_data(insert_sql)
    return all_match_infos


def exchange_nba_data():
    year = str(datetime.now().year)
    month = str(datetime.now().month) if datetime.now().month >= 10 else '0' + str(datetime.now().month)
    day = str(datetime.now().day) if datetime.now().day >= 10 else '0' + str(datetime.now().day)

    all_info = get_nba_data(year, month, day)
    # 将all_info转换为对应的语句
    broadcast_str = u'今天是{0}年{1}月{2}日,现在开始播报今天的比赛。'.format(year, month, day)
    for match_info in all_info:
        if match_info.get('score').split(':')[0]:
            broadcast_str += match_info.get('match').split(':')[0] + '对阵' + match_info.get('match').split(':')[1] + \
                             match_info.get('score').split(':')[0] + '比' + \
                             match_info.get('score').split(':')[1] + '。'
        else:
            broadcast_str += match_info.get('match').split(':')[0] + '对阵' + match_info.get('match').split(':')[
                1] + '尚未开始。'

    print broadcast_str
    APP_ID = '10715605'
    API_KEY = '9TpqA6aHGWgxagFFzudebhIj'
    SECRET_KEY = 'spGFcwNwk2OasbGf916idGFA1iQOcQhf'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(broadcast_str, 'zh', 1, {
        'vol': 5,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    # mp3存储地址
    MP3_path = os.path.join(Config.NBA_SCORE_MP3, 'nba.mp3')
    if not os.path.exists(Config.NBA_SCORE_MP3):
        os.makedirs(Config.NBA_SCORE_MP3)
    if not isinstance(result, dict):
        with open(MP3_path, 'wb') as f:
            f.write(result)


if __name__ == '__main__':
    exchange_nba_data()

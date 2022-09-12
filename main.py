# -*- coding: utf-8 -*-
"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: main.py
@Author: Jiabao Lin
@Date: 2020/1/27

@modify by peikai
@ on Wed May 25 17:02:09 2022
"""
from service.crawler import Crawler
import time  # 导入此模块，获取当前时间


def timed_start(my_hour = '11',my_minute = '35'):
    flag = 1
    while flag:
        t = time.localtime()  # 当前时间的纪元值
        fmt = "%H %M"
        now = time.strftime(fmt, t)  # 将纪元值转化为包含时、分的字符串
        now = now.split(' ') #以空格切割，将时、分放入名为now的列表中
    
        hour = now[0]
        minute = now[1]
        print(hour,minute)
        print(f'waiting...{my_hour}:{my_minute}')
        time.sleep(55)
        if hour == my_hour and minute == my_minute:
            music = 'it is time to start'
            print(music)
            flag = 0


if __name__ == '__main__':
    """
    地方疫情病例数量
    加总
    可能不等于总体病例数量
    的原因是因为
    如境外输入，省级（湖北输入） ，外地来津，外地来沪等，或其他的非官方地区单位
    """
    # crawler = Crawler(just_run_once = False)
    n_hour = 8
    crawler = Crawler(just_run_once = False, freq=3600*n_hour) # freq unit is second
    timed_start("21","11")
    crawler.run()

import time
import requests
import re
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler

def get_text(url):
    # 下载JS信息
    response = requests.get(url)
    text = response.text
    return text

def text_to_json(text):
    # 过滤为json格式
    string = re.sub('.*?f\":','',text)
    string_1 = re.sub('}}\);$','',string)
    string_2 = re.sub(',\"f204\":\"-\",\"f205\":\"-\",\"f206\":\"-\"','',string_1)
    string_3 = re.sub('\"f1\":2,','',string_2)
    string_4 = re.sub('\"f13\":[01],','',string_3)
    return string_4

def title_substitution(json):
    print("===>>正在替换标题")
    json_title_f2 = re.sub('\"f2\"','\"最新价\"',json)
    json_title_f13 = re.sub('\"f3\"','\"今日涨跌幅\"',json_title_f2)
    json_title_f12 = re.sub('\"f12\"','\"代码\"',json_title_f13)
    json_title_f14 = re.sub('\"f14\"','\"名称\"',json_title_f12)
    json_title_f62 = re.sub('\"f62\"','\"今日主力净流入-净额\"',json_title_f14)
    json_title_f66 = re.sub('\"f66\"','\"今日超大单净流入-净额\"',json_title_f62)
    json_title_f69 = re.sub('\"f69\"','\"今日超大单净流入-净占比\"',json_title_f66)
    json_title_f72 = re.sub('\"f72\"','\"今日大单净流入-净额\"',json_title_f69)
    json_title_f75 = re.sub('\"f75\"','\"今日大单净流入-净占比\"',json_title_f72)
    json_title_f78 = re.sub('\"f78\"','\"今日中单净流入-净额\"',json_title_f75)
    json_title_f81 = re.sub('\"f81\"','\"今日中单净流入-净占比\"',json_title_f78)
    json_title_f84 = re.sub('\"f84\"','\"今日小单净流入-净额\"',json_title_f81)
    json_title_f87 = re.sub('\"f87\"','\"今日小单净流入-净占比\"',json_title_f84)
    json_title_f184 = re.sub('\"f184\"','\"今日主力净流入-净占比\"',json_title_f87)
    return json_title_f184 


def filter(json_title):
    ## 客户要求
    # 筛选N开头的字符串
    string_N  = re.search('\"N.+?\"',json_title)  
    if string_N == None:
        print("===>>没有以N开头的信息")
        string_N = json_title
    else:
        string_N = re.sub('\"N.+?\"','\"无参考价值\"',json_title)
    # 筛选C开头的字符串
    string_C  = re.search('\"C.+?\"', string_N)
    if string_C == None:
        print("===>>没有以C开头的信息")
        string_C = string_N
    else:
        string_C = re.sub('\"C.+?\"','\"无参考价值\"',string_N)
    # 筛选ST开头的字符串
    string_ST  = re.search('\"ST.+?\"', string_N)
    if string_ST == None:
        print("===>>没有以ST开头的信息")
        string_ST = string_C
    else:
        string_ST = re.sub('\"ST.+?\"','\"无参考价值\"',string_N)
    return string_ST

def to_execl(filtered_json):
    # 导出为execl
    Now_time = time.strftime('%Y-%m-%d-%H-%M')
    df = pd.read_json(filtered_json)
    df.to_excel("date_"+Now_time+".xlsx")

def main():
    # 主函数
    url = "URL"
    print("现在时间是：",time.strftime('%Y-%m-%d-%H-%M'))
    text = get_text(url)
    print("===>>爬取完成")
    json = text_to_json(text)
    print("===>>过滤为json")
    json_title = title_substitution(json)
    filtered_json = filter(json_title)
    print("===>>筛选完股票信息")    
    print("===>>正在导出为execl")
    to_execl(filtered_json)
    ### 调试用
    # print("===>>正在导出为json")
    # with open('cache_data.json ', 'w', encoding='utf-8') as f:
    #    f.write(filtered_json)

# 定时任务
sched = BlockingScheduler()
sched.add_job(main, 'interval', minutes=30)
sched.start()
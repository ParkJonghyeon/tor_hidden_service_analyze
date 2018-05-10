from bs4 import BeautifulSoup
import os
from pandas import DataFrame
import pandas as pd
import operator
import re

# openweb과의 연계를 알아보기 위해서 .onion 이 포함되지 않은 일반 주소들은 따로 파일 만들어서 분류 할 것
# 데이터 형식은 발견된 사이트 주소 - 발견한 주소 - 발견된 사이트의 발견 날짜로 구성

top_dir_route = '/media/lark/extra_storage/onion_link_set/result_html/html_total'
output_file_name = 'address_set/link_count.csv'

def get_all_html_route(html_total_dir):
    date_list = os.listdir(html_total_dir)
    html_files = {}
    for sub_dir in date_list:
        html_files[sub_dir] = os.listdir(html_total_dir+'/'+sub_dir)
    all_html_route = []
    for sub_dir in date_list:
        for html_file in html_files[sub_dir]:
            all_html_route.append(html_total_dir+'/'+sub_dir+'/'+html_file)
    return all_html_route


def dir_route_to_onion_html(dir_route):
    return dir_route.split('/')[-1]


def onion_html_to_16char(onion_html):
    return onion_html.split('.')[0]


temp_link_list = []
all_file_route = get_all_html_route(top_dir_route)

link_count_dic = {}

for html_route in all_file_route:
    current_onion_html = dir_route_to_onion_html(html_route)
    current_onion_address = onion_html_to_16char(current_onion_html)
    if current_onion_address in link_count_dic.keys():
        continue;
    with open(html_route,'r') as target_html:
        soup = BeautifulSoup(target_html,'html.parser')
    is_crashed = soup.find(class_='title-text')
    if is_crashed is not None and is_crashed.text == 'Gah. Your tab just crashed.':
        continue;
    link_counter = 0
    counted_link = []
    for href in soup.find_all('a'):
        link = href.get('href')
        if link is not None and current_onion_address not in link:
            re_link = re.search('((http[s]?)?(://)?(www\.)?([A-Za-z0-9-.]+(\.[A-Za-z]{2,5})))', link) # 동일 사이트의 하위 페이지로의 링크를 동일한 링크로 계산
            if re_link is not None and re_link.group(1) not in counted_link:
                if re_link.group(1).find('http') > -1 or re_link.group(1).find('https') > -1 or re_link.group(1).find('.onion') > -1:
                    counted_link.append(re_link.group(1))
                    link_counter = link_counter+1
    link_count_dic[current_onion_address] = link_counter
        
link_count_df = pd.DataFrame(list(link_count_dic.items()), columns=['OnionAddress','LinkCount'])
link_count_df = link_count_df.sort_values(by='LinkCount')
link_count_df.to_csv(output_file_name, index=None)
sum_by_value = pd.value_counts(link_count_df['LinkCount'].values, sort=True)
pd.DataFrame({'LinkCount':sum_by_value.index, 'PageNum':sum_by_value.values}).sort_values(by='LinkCount').to_csv('address_set/link_count_sum.csv', index=None)

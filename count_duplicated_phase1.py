from bs4 import BeautifulSoup
import os
from pandas import DataFrame
import pandas as pd
import operator

# 타이틀을 기준으로 중복 된 페이지와 아닌 페이지의 분류 작업
# 페이즈 2에서 중복 된 페이지가 있는 주소에 한정해서 유사도 비교 처리함

top_dir_route = '/media/lark/extra_storage/onion_link_set/html_171001_to_180327/shared_dir'
output_file_name = 'address_set/duplicated_count.txt'


def get_all_html_route(html_total_dir):
    date_list = sorted(os.listdir(html_total_dir), reverse=True)
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

onion_title_dic = {}
onion_html_dir_dic = {}
orig_page_title_count = {}
title_onion_dic = {}
title_html_dir_dic = {}

for html_route in all_file_route:
    current_onion_html = dir_route_to_onion_html(html_route)
    current_onion_address = onion_html_to_16char(current_onion_html)
    with open(html_route,'r') as target_html:
        soup = BeautifulSoup(target_html,'html.parser')
    is_crashed = soup.find(class_='title-text')
    if is_crashed is not None and is_crashed.text == 'Gah. Your tab just crashed.':
        continue;
    try:
        page_title = soup.find('title').text
    except:
        page_title = "No Title"
    onion_title_dic[current_onion_address] = page_title
    onion_html_dir_dic[current_onion_address] = html_route

for onion in onion_title_dic:
    try:
        title_onion_dic[onion_title_dic[onion]].append(onion)
        title_html_dir_dic[onion_title_dic[onion]].append(onion_html_dir_dic[onion])
    except:
        title_onion_dic[onion_title_dic[onion]]=[onion]
        title_html_dir_dic[onion_title_dic[onion]]=[onion_html_dir_dic[onion]]

for title in title_onion_dic:
    orig_page_title_count[title] = len(title_onion_dic[title])

duplicated_page_output = open(output_file_name, 'w')

for title in orig_page_title_count:
    duplicated_page_output.write('[Title]'+title+'\n[Count]'+str(orig_page_title_count[title])+'\n[ADDRESS_SET]'+str(title_onion_dic[title])+'\n[HTML_DIR]'+str(title_html_dir_dic[title])+'\n')

duplicated_page_output.close()

title_count_df = pd.DataFrame(list(orig_page_title_count.items()), columns=['Title','DuplicateCount'])
title_count_df = title_count_df.sort_values(by='DuplicateCount')
sum_by_value = pd.value_counts(title_count_df['DuplicateCount'].values, sort=True)
pd.DataFrame({'DuplicateCount':sum_by_value.index, 'PageNum':sum_by_value.values}).sort_values(by='DuplicateCount').to_csv('address_set/duplicated_count_sum.csv', index=None)

from bs4 import BeautifulSoup
import os
from pandas import DataFrame
import pandas as pd

# openweb과의 연계를 알아보기 위해서 .onion 이 포함되지 않은 일반 주소들은 따로 파일 만들어서 분류 할 것
# 데이터 형식은 발견된 사이트 주소 - 발견한 주소 - 발견된 사이트의 발견 날짜로 구성

top_dir_route = '/media/lark/extra_storage/onion_link_set/result_html/html_total'
output_file_name = 'address_set/inner_onion_address_list.tsv'

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


temp_link_list = []
all_file_route = get_all_html_route(top_dir_route)

for html_route in all_file_route:
    target_html = open(html_route,'r')
    soup = BeautifulSoup(target_html,'html.parser')
    for href in soup.find_all('a'):
        link = href.get('href')
        if link is not None and '.onion' in link:
            temp_link_list.append(link)

link_dataframe = pd.DataFrame(temp_link_list, columns=['Link'])

link_dataframe['Link'] = link_dataframe['Link'].str.extract("([A-Za-z0-9]{16,16})", expand=False)
link_dataframe = link_dataframe.drop_duplicates(['Link'], keep='first')
link_dataframe = link_dataframe.dropna()

link_dataframe['Link'] = 'http://' + link_dataframe['Link'].astype(str) + '.onion'

link_dataframe.to_csv(output_file_name, sep='\t', index=False)

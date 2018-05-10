import os
import re
from hashlib import sha256

# rosettacode btc add validator
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

top_dir_route = '/media/lark/extra_storage/onion_link_set/result_html/html_total'
output_file_name = 'address_set/bitcoin_wallet_list.txt'

# bitcoin address extract methods
# rosettacode btc add validator
def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')


# rosettacode btc add validator
def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]


def extract_wallet_address(sorce, result_set):
    btc_find = False

    # max length btc add math
    regex = re.compile("([13]{1}[A-HJ-NP-Za-km-z1-9]{25,33})")
    wallet_address_set = regex.findall(sorce)

    if len(wallet_address_set) > 0:
        for wallet_address in wallet_address_set:
            if check_bc(wallet_address) is True:
                btc_find = True
                result_set.append(wallet_address)
    # min length btc add match
    regex_lazy = re.compile("([13]{1}[A-HJ-NP-Za-km-z1-9]{25,33}?)")
    wallet_address_set_lazy = regex_lazy.findall(sorce)

    if len(wallet_address_set_lazy) > 0:
        for wallet_address in wallet_address_set_lazy:
            if check_bc(wallet_address) is True:
                btc_find = True
                result_set.append(wallet_address)
    return btc_find


# source html load method
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


def main():
    find_wallet_address = []
    btc_find_html = open('address_set/btc_find_html_list.txt','w')

    all_file_route = get_all_html_route(top_dir_route)

    # loop one html file open then find btc add to set
    for html_route in all_file_route:
        target_html = open(html_route, 'r')

        html_text = target_html.read()
        btc_find = extract_wallet_address(html_text, find_wallet_address)
        target_html.close()

        if btc_find == True:
            btc_find_html.write(dir_route_to_onion_html(html_route) + "\n")

    # address set to list
    # set으로 정리하기 이전에 기존에 파일에 있던 값도 리스트화 필요
    find_wallet_address = list(set(find_wallet_address))
    btc_find_html.close()

    # write address list
    wallet_address_list_output = open(output_file_name, 'w')
    for address_item in find_wallet_address:
        wallet_address_list_output.write(address_item + "\n")

    wallet_address_list_output.close()


if __name__ == '__main__':
    main()

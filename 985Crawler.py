from bs4 import BeautifulSoup
import requests
from functools import reduce
from time import sleep
from mypackage.timer import Timer

def add(a,b):
    return a+b

def ExtString(string, char):
    strList = list(string)
    charlist = list(char)
    strList.extend(charlist)
    n_string = reduce(add, strList)
    return n_string

UnivList = ['清华', '北京大学', '北航', '人大', '北师大', '北理工']
UnivUrls = ['http://www.dianping.com/search/keyword/2/10_{}'.format(univ) for univ in UnivList]
# print(urls)

def get_restaurants(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # print(soup)
    names    = soup.select('#shop-all-list > ul > li > div.txt > div.tit > a > h4')
    rates    = soup.select('#shop-all-list > ul > li > div.txt > div.comment > span')
    cates = soup.select('#shop-all-list > ul > li > div.txt > div.tag-addr > a:nth-of-type(1)')
    com_nums = soup.select('#shop-all-list > ul > li > div.txt > div.comment > a.review-num > b')
    prices   = soup.select('#shop-all-list > ul > li > div.txt > div.comment > a.mean-price > b')
    tastes   = soup.select('#shop-all-list > ul > li > div.txt > span > span:nth-of-type(1) > b')
    envs     = soup.select('#shop-all-list > ul > li > div.txt > span > span:nth-of-type(2) > b')
    services = soup.select('#shop-all-list > ul > li > div.txt > span > span:nth-of-type(3) > b')

    # print(names, rates, prices, tastes, envs, services, sep='\n-----------------------\n')
    li = []
    for name, rate, cate, com_num, price, taste, env, service in zip(names, rates, cates, com_nums, prices, tastes, envs, services):
        data = {
            'name': name.get_text().encode("GBK", 'ignore').decode("GBK"),
            'rate': rate.get("title").encode("GBK", 'ignore').decode("GBK"),
            'cate': cate.get_text().encode("GBK", 'ignore').decode("GBK"),
            'comm_num': com_num.get_text().encode("GBK", 'ignore').decode("GBK"),
            'price': price.get_text().encode("GBK", 'ignore').decode("GBK"),
            'taste': taste.get_text().encode("GBK", 'ignore').decode("GBK"),
            'env': env.get_text().encode("GBK", 'ignore').decode("GBK"),
            'service': service.get_text().encode("GBK", 'ignore').decode("GBK")
        }
        li.append(data)
        print(data)
    return li

# print(get_restaurants('http://www.dianping.com/search/keyword/2/10_清华'))

for i, UnivUrl in enumerate(UnivUrls):
    univname = UnivList[i]
    f = open(univname+'.csv', 'a+')
    f.write('店铺名')
    f.write(',')
    f.write('星级')
    f.write(',')
    f.write('种类')
    f.write(',')
    f.write('点评数量')
    f.write(',')
    f.write('人均')
    f.write(',')
    f.write('口味')
    f.write(',')
    f.write('环境')
    f.write(',')
    f.write('服务')
    f.write('\n')
    url = UnivUrl
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    pages = soup.select('body > div.section.Fix.J-shop-search > div.content-wrap > div.shop-wrap > div.page')
    pglist = []
    for page in pages:
        pglist.append(page.get_text())
    page_nums = int(pglist[0].split('\n')[-3])
    # print(page_nums)
    urls = []
    for k in range (page_nums):
        raw_url = url
        char = '/p' + str(k+1)
        if k != 0:
            raw_url = ExtString(raw_url, char=char)
        urls.append(raw_url)
    for j, url2 in enumerate(urls):
        List = get_restaurants(url=url2)
        for restaurant in List:
            print(restaurant)
            f.write(restaurant['name'])
            f.write(',')
            f.write(restaurant['rate'])
            f.write(',')
            f.write(restaurant['cate'])
            f.write(',')
            f.write(restaurant['comm_num'])
            f.write(',')
            f.write(restaurant['price'])
            f.write(',')
            f.write(restaurant['taste'])
            f.write(',')
            f.write(restaurant['env'])
            f.write(',')
            f.write(restaurant['service'])
            f.write('\n')
        print('-' * 20)
        print(univname, 'Page', str(j + 1), 'has been crawled.', sep=' ')
        sleep(1)
    f.close()

    # print(urls)




'''
店名 #shop-all-list > ul > li:nth-child(1) > div.txt > div.tit > a:nth-child(1) > h4
body > div.section.Fix.J-shop-search > div.content-wrap > div.shop-wrap > div.page > a:nth-child(12)
body > div.section.Fix.J-shop-search > div.content-wrap > div.shop-wrap > div.page
种类#shop-all-list > ul > li:nth-child(1) > div.txt > div.tag-addr > a:nth-child(1) > span
#shop-all-list > ul > li:nth-child(1) > div.txt > div.tag-addr > a:nth-child(1)
#shop-all-list > ul > li:nth-child(1) > div.txt > div.tag-addr
'''
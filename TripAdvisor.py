from bs4 import BeautifulSoup
import requests
from functools import reduce
from time import sleep
from mypackage.timer import Timer

timer = Timer()
timer.start()


def add(a, b):
    return a+b

def replace(seq, x, y):
    seq1 = list(seq)
    for i in range (len(seq)):
        if seq[i] == x:
            seq1[i] = y
    return reduce(add, seq1)

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html#ATTRACTION_LIST'
# urls = []
urls = ['https://cn.tripadvisor.com/Attractions-g60763-Activities-oa{}-New_York_City_New_York.html#ATTRACTION_LIST'.format(str(i)) for i in range(30,1110,30)]
urls.insert(0, url)


def get_attractions(url):
    li = []
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_title > a')
    cates = soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.tag_line > div')
    comment_nums = soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_rating > div > div > span.more > a')
    rates = soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_rating > div > div > span.ui_bubble_rating')
    for title, cate, comment_num, rate in zip(titles, cates, comment_nums, rates):
        data = {
            'title': title.get_text(),
            'cate': replace([item for item in cate.get_text().split('\n') if item != '' and item != ' '], ', ', '&'),
            'comment_num': reduce(add, comment_num.get_text().split('\n')[1].split('条点评')[0].split(',')),
            'rate': rate.get("alt").split('，')[0]
        }
        li.append(data)
    return li

# get_attractions(url=url)
f = open('DataExtracted.csv', 'a+')
f.write('景点')
f.write(',')
f.write('类型')
f.write(',')
f.write('评论数量')
f.write(',')
f.write('评分')
f.write('\n')

DataBase = []
for i, url in enumerate(urls):
    data = get_attractions(url=url)
    DataBase.extend(data)
    for place in data:
        print(place)
        f.write(str(replace(place['title'].encode("GBK", 'ignore').decode("GBK"), ',', '')))
        f.write(',')
        f.write(place['cate'])
        f.write(',')
        f.write(place['comment_num'])
        f.write(',')
        f.write(place['rate'])
        f.write('\n')
    print('-'*10)
    print('Page',str(i+1),'has been crawled.',sep=' ')
    sleep(2)

f.close()


timer.end()

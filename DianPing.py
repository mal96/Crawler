from bs4 import BeautifulSoup
import requests
from time import sleep
from mypackage.timer import Timer

timer = Timer()
timer.start()

url = 'http://www.dianping.com/search/category/2/10/g110'
urls = ['http://www.dianping.com/search/category/2/10/g110p{}?aid=6232395%2C56637267%2C74597797%2C38230595%2C514849%2C65721252%2C76854650%2C67056533%2C90036247%2C32489357%2C76936209%2C92617912%2C92617929%2C65483113%2C65602343%2C45314401%2C94317424%2C93509565%2C21139015%2C96448104%2C3566815&cpt=6232395%2C56637267%2C74597797%2C38230595%2C514849%2C65721252%2C76854650%2C67056533%2C90036247%2C32489357%2C76936209%2C92617912%2C92617929%2C65483113%2C65602343%2C45314401%2C94317424%2C93509565%2C21139015%2C96448104%2C3566815&tc=3'.format(str(i)) for i in range(2, 51, 1)]
# urls = []
urls.insert(0, url)

# print(len(urls))


def get_restaurants(url):
    wb_data = requests.get(url)
    soup =  BeautifulSoup(wb_data.text, 'lxml')
    names        = soup.select('#shop-all-list > ul > li > div.txt > div.tit > a > h4')
    rates        = soup.select(('#shop-all-list > ul > li > div.txt > div.comment > span'))
    comment_nums = soup.select('#shop-all-list > ul > li > div.txt > div.comment > a.review-num > b')
    prices       = soup.select('#shop-all-list > ul > li > div.txt > div.comment > a.mean-price > b')
    tastes       = soup.select('#shop-all-list > ul > li > div.txt > span > span:nth-of-type(1) > b')
    envs         = soup.select('#shop-all-list > ul > li > div.txt > span > span:nth-of-type(2) > b')
    services     = soup.select('#shop-all-list > ul > li > div.txt > span > span:nth-of-type(3) > b')

    li = []
    for name,rate,comment_num,price,taste,env,service in zip(names,rates,comment_nums,prices,tastes,envs,services):
        data = {
            'name':name.get_text().encode("GBK", 'ignore').decode("GBK"),
            'rate':rate.get("title").encode("GBK", 'ignore').decode("GBK"),
            'comment_num':comment_num.get_text().encode("GBK", 'ignore').decode("GBK"),
            'price':price.get_text().encode("GBK", 'ignore').decode("GBK"),
            'taste':taste.get_text().encode("GBK", 'ignore').decode("GBK"),
            'env':env.get_text().encode("GBK", 'ignore').decode("GBK"),
            'service':service.get_text().encode("GBK", 'ignore').decode("GBK")
        }
        li.append(data)
    return li

f = open('DataExtracted_DianPing.csv', 'a+')
f.write('店铺名')
f.write(',')
f.write('星级')
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

for i, url in enumerate(urls):
    List = get_restaurants(url=url)
    for restaurant in List:
        print(restaurant)
        f.write(restaurant['name'])
        f.write(',')
        f.write(restaurant['rate'])
        f.write(',')
        f.write(restaurant['comment_num'])
        f.write(',')
        f.write(restaurant['price'])
        f.write(',')
        f.write(restaurant['taste'])
        f.write(',')
        f.write(restaurant['env'])
        f.write(',')
        f.write(restaurant['service'])
        f.write('\n')
    print('-'*20)
    print('Page',str(i+1),'has been crawled.',sep=' ')
    sleep(2)

f.close()

timer.end()



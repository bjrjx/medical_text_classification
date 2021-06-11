import requests
import urllib.request
import urllib.parse
from time import time, sleep
from lxml import etree

# 通过百度搜索，得到相关词语（爬虫得到结果）
page_buffer = []

department_index_dic = {
    "内科": {
        "心血管内科":237,
        "神经内科": 35,
        "内分泌科": 279,
        "血液科": 281,
        "风湿免疫科": 39,
        "呼吸内科": 280
    },
    "外科": {
        "骨科": 47,
        "胃肠外科": 201,
        "烧伤科": 285,
        "血管外科": 181,
        "神经外科": 232,
        "普外科": 304,
        "肝胆外科": 284,
        "乳腺外科": 286,
        "肛肠外科": 283,
        "泌尿外科": 163,
        "心胸外科": 21
    },
    "妇产科": {
        "不孕不育": 3157,
        "产科": 229,
        "妇科": 44
    },
    "儿科": {
        "小儿精神科": 3159,
        "新生儿科": 319,
        "小儿外科": 231,
        "小儿内科": 45
    },
    "其他": {
        "整形美容": 3165,
        "精神心理科": 3166,
        "肿瘤科": 3162,
        "皮肤性病科": 319465592,
        "五官科": 323,
        "中医科": 3163,
        "减肥科": 27,
        "男科": 322,
        "传染病科": 311
    }
}

def getHTML():
    # 通过关键词keyword，得到百度搜索后的html结果
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }  # 定义头文件，伪装成浏览器
    # 编码关键词

    # url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=' + keyword + \
    #     '%2B装修%7C建材%7C装饰&tn=news&rsv_bp=1&rsv_sug3=6&oq=&rsv_sug2=0&rsv_btype=t&f=8&inputT=1203&rsv_sug4=1930'
    for key,value in department_index_dic.items():
        for department,index in value.items():
            path_name = key + "_" + department + ".txt"
            url_home = 'http://ask.39.net/news/' + str(index) + '-'
            for i in range(1,1001):
                try:
                    sleep(0.125)
                    url = url_home + str(i) + '.html'
                    request = requests.get(url, headers = headers)
                    data = request.content
                    data = data.decode("utf-8")
                    page = etree.HTML(data)
                    print(page, 'page')
                    href_list = page.xpath('//*[@id="list_tag"]/ul//a/@href')
                    for href in href_list:
                        print('文本不够。找具体描述')
                        detail_url = 'http://ask.39.net/'
                        detail_url = detail_url + href
                        request = requests.get(detail_url, headers=headers)
                        data = request.content
                        data = data.decode("utf-8")
                        page = etree.HTML(data)
                        ask_text = page.xpath('//p[@class="txt_ms"]/text()')[0].rstrip().replace(' ','').replace('\n','')
                        ask_title = page.xpath('//p[@class="ask_tit"]/text()')[0].rstrip().replace(' ','').replace('\n','')
                        final_text = ask_text if len(ask_text) >= len(ask_title) else ask_title
                        print(final_text,'=======ask_text======')
                        with open(path_name,'a',encoding='utf-8') as f:
                            f.write(str(final_text))
                            f.write('\n')
                except:
                    with open('fail_case.txt','a',encoding='utf-8') as w:
                        w.write(department)
                        w.write(str(i))
                        w.write('\n')








def processData(data):
    # 处理data，得到所需结果
    res = []
    html = etree.HTML(data)
    html_data = html.xpath('/html/body/div[1]/div[3]/div[1]/div[4]/div[2]')  # 大的定位
    tmp = []  # 用来存相关词的element
    for item in html_data:
        # 一个item里面包括4个(一行)
        four = item.xpath('./div')
        # 每一个里面又包含3个div，第2个是我们要的。分别是[图片，名词，描述]
        for one in four:
            tmp.append(one.xpath('./div[2]')[0])
    res = [x.xpath('./a/text()')[0] for x in tmp]
    return res

if __name__ == '__main__':
    getHTML()

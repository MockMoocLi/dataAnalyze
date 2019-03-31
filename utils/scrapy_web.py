# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :19-3-30
import asyncio
import math
import multiprocessing
import re
import subprocess
from pyecharts import Line3D, Pie, WordCloud

from taobao.models import JDProductsItem, JDCommentItem, ProductName, JDHotCommentTagItem
import requests
from scrapy.selector import Selector

REMOTE_HOST = "https://pyecharts.github.io/assets/js"


class ScrapyInfo:
    def __init__(self,**kwargs):
        # self.web = self.web
        self.jdid = kwargs['jdid']
        # self.taobaoid = kwargs['taobaoid']
        self.keyword = kwargs['keyword']
        self.piename = []
        self.piecount = []
        self.woldname = []
        self.worldcount = []


    def scrapy_JDinfo(self):
        comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(self.jdid)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
                   'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
        taobao_comurl = 'https://rate.tmall.com/list_detail_rate.htm?itemId=587578411300&spuId=1152764912&sellerId=2024314280&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098'
        response = requests.get(url=comment_url, headers=headers)
        # response.encoding = 'utf8'
        # print('-------------'+response.text)
        data = response.json()
        commentSummary = data.get('productCommentSummary')
        self.piename = ['追评人数', '中评', '好评', '差评']
        self.piecount.append(commentSummary['showCount'])
        # v1.append(json2['defaultGoodCount'])
        self.piecount.append(commentSummary['generalCount'])
        self.piecount.append(commentSummary['goodCount'] - commentSummary['defaultGoodCount'])
        self.piecount.append(commentSummary['poorCount'])
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for hotComment in data['hotCommentTagStatistics']:
            name = hotComment['name']
            count = hotComment['count']
            self.woldname.append(name)
            self.worldcount.append(count)
            pool.apply_async(saveJDhotTag, (self.keyword, self.jdid, name, count))

        pool.close()
        pool.join()

        pool2 = multiprocessing.Pool(multiprocessing.cpu_count())
        for comment_item in data['comments']:
            if (comment_item.get('content') == '此用户未及时填写评价内容，系统默认评价！') or comment_item.get('content' == '此用户未填写评价内容'):
                pass
            if (len(comment_item.get('content')) <= 6):
                pass
            else:
                content = comment_item.get('content')
                nickname = comment_item.get('nickname')
                score = comment_item.get('score')
                userLevelName = comment_item.get('userLevelName')
                days = comment_item.get('days')
                firstCategory= comment_item.get('firstCategory')
                imageCount = comment_item.get('imageCount')
                productColor = comment_item.get('productColor')
                productSize = comment_item.get('productSize')
                referenceId = comment_item.get('referenceId')
                referenceName = comment_item.get('referenceName')
                secondCategory = comment_item.get('secondCategory')
                thirdCategory = comment_item.get('thirdCategory')
                userLevelId = comment_item.get('userLevelId')
                pool.apply_async(saveJDhotTag, (self.keyword, self.jdid, name, count))

                jdcomment = JDCommentItem.objects.create(productid=self.jdid, content=content,
                                                         nickname=nickname, days=days, firstCategory=firstCategory,
                                                         imageCount=imageCount, productColor=productColor,
                                                         productSize=productSize, referenceId=referenceId,
                                                         referenceName=referenceName, secondCategory=secondCategory,
                                                         thirdCategory=thirdCategory, userLevelId=userLevelId,
                                                         score=score, userLevelName=userLevelName, productname_id=self.keyword)
                jdcomment.save()


    def scrapy_taobaoinfo(self):
        pass


    # 元饼图
    def pie(self):

        pie = Pie("")
        # 传入两个列表
        pie.add("", self.piename, self.piecount, is_label_show=True)
        pi = dict(
            mypie=pie.render_embed(),
            host=REMOTE_HOST,
            script_list=pie.get_js_dependencies()
        )
        return pi

    # 云词
    def worldcloud(self):
        wordcloud = WordCloud(width=1300, height=620)
        # 传入两个列表
        wordcloud.add("", self.woldname, self.worldcount, word_size_range=[20, 100])
        word = dict(
            myworldcloud=wordcloud.render_embed(),
            host=REMOTE_HOST,
            script_list=wordcloud.get_js_dependencies()
        )
        return word

    def line3d(self):
        _data = []
        for t in range(0, 25000):
            _t = t / 1000
            x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
            y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
            z = _t + 2.0 * math.sin(75 * _t)
            _data.append([x, y, z])
        range_color = [
            '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
            '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        line3d = Line3D("3D line plot demo", width=1200, height=600)
        line3d.add("", _data, is_visualmap=True,
                   visual_range_color=range_color, visual_range=[0, 30],
                   is_grid3D_rotate=True, grid3D_rotate_speed=180)
        return line3d

# 搜索时调用
def scrapy_JD(keyword):
    try:
        product = ProductName.objects.create(name=keyword)
        product.save()
    except Exception as e:
        print(e)

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0','authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
    response = requests.get(url='https://search.jd.com/Search?keyword={}&enc=utf-8&spm=2.1.0'.format(keyword), headers=headers)
    response.encoding = 'utf8'

    selector = Selector(response)
    # productsItem = ProductsItem()
    price = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div/strong/i/text()').extract()[0]
    name = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div/a/em/font/text()').extract()[0]
    desc = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div/a/em/text()').extract()[0]
    # // *[ @ id = "J_goodsList"] / ul / li[1] / div / div[1] / a / img
    imgurl = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/img/@source-data-lazy-img').extract()[0]
    idurl = selector.xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/@href').extract()[:1]
    id = [re.compile('com/(.*?).html').findall(i)[0] for i in idurl]
    url = ['https:' + i for i in idurl]
    category = selector.xpath('//*[@id="J_selector"]/div[1]/div/div[2]/div[1]/ul/li[1]/a/text()').extract()
    print(price)
    # print(selector.xpath('//*[@id="J_goodsList"]/ul/li[1]/div/div[4]/a/em/text()').extract())
    # print(name)
    # for i in range(len(price)):
    #     if name[i] == keyword:
    try:
        ProductName.objects.filter(name=keyword).update(jdProductId=id[0])

        product = JDProductsItem.objects.create(name_id=keyword,productid=id[0], category=category[0], description=desc,
                                                          imgurl=imgurl, reallyPrice=price, url=url[0])
        product.save()
            #     product.save()
    except Exception as e:
        print(e)

# 搜索时调用
def scrapy_taobao(keyword):
    taobao_sumtagurl = 'https://rate.tmall.com/listTagClouds.htm?itemId=587578411300&isAll=true&isInner=true&t=&groupId=&_ksTS='
    taobao_search_url = 'https://s.taobao.com/search?q=' + keyword
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0','authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
    response = requests.get(url=taobao_search_url, headers=headers)
    response.encoding = 'utf8'
    # productsItem = ProductsItem()
    tlist = re.findall('"raw_title":"(.*?)",', response.text)  # 正则提取商品名称
    plist = re.findall('"view_price":"(.*?)",', response.text)  # 正则提示商品价格
    nid = re.findall('"nid":"(.*?)"', response.text)  # 正则提示商品价格
    # print(response.content)
    # print(response.text)
    # print(price)

def saveJDhotTag(*args):
    JDHotCommentTagItem.objects.create(productname_id=args[0], name=args[2], productid=args[1], count=args[3]).save()

def saveJDcomment():
    pass


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import pymysql
# from myFirstScrapy.myFirstScrapy.items import *
from spider.items import *


class MySqlPipeline(object):
    def __init__(self):
        # 实例变量
        self.mydb = 'spider'
        # 打开数据库连接
        self.conn = pymysql.connect(host="localhost", port=3306, user="spideruser", password="159874xzh", db="spider", charset="utf8")


    def process_item(self, item, spider):
        # 先插入商店信息
        if isinstance(item, ShopItem):
            try:
                cur = self.conn.cursor()
                sql = '''insert into shop values (%s,%s,%s,%s,%s,%s)'''
                self.conn.ping(reconnect=True)
                cur.execute(sql,(item['_id'],item['name'],item['shopId'],item['url1'],item['url2'],item['venderId']))
                cur.close()
                self.conn.commit()
                self.conn.close()
            except Exception as e:
                print(e)
        elif isinstance(item, ProductLink):
            try:
                cur = self.conn.cursor()
                sql = '''insert into productlink values (%s,%s)'''
                self.conn.ping(reconnect=True)
                cur.execute(sql,(item['id'], item['imgurl']))
                cur.close()
                self.conn.commit()
                self.conn.close()
            except Exception as e:
                print(e)
        # # 插入产品信息
        # elif isinstance(item, ProductsItem):
        #     try:
        #         cur = self.conn.cursor()
        #         sql = '''insert into product(_id, category, description, name, originalPrice, reallyPrice, url, favourableDesc1, shopId_id)
        #          values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        #         # list = [value for value in item.values()]
        #         self.conn.ping(reconnect=True)
        #
        #         cur.execute(sql,(item['_id'],item['category'],item['description'],item['name'],
        #                          item['originalPrice'],item['reallyPrice'],item['url'],item['favourableDesc1'],item['shopId']))
        #         cur.close()
        #         self.conn.commit()
        #         self.conn.close()
        #     except Exception as e:
        #         print(e)
        # 插入评论总和
        # elif isinstance(item, CommentSummaryItem):
        #     try:
        #         cur = self.conn.cursor()
        #         sql = '''insert into commentsummary
        #         (afterCount,averageScore,commentCount,defaultGoodCount,generalCount,generalRate,
        #         goodCount,goodRate,imageListCount,poorCount,poorRate,score,showCount,soType,_id_id) values
        #         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        #
        #         self.conn.ping(reconnect=True)
        #
        #         cur.execute(sql,(item['afterCount'],item['averageScore'],item['commentCount'],
        #                          item['defaultGoodCount'],item['generalCount'],item['generalRate'],
        #                          item['goodCount'],item['goodRate'],item['imageListCount'],
        #                          item['poorCount'],item['poorRate'],item['score'],item['showCount'],item['soType'],item['_id']))
        #         cur.close()
        #         self.conn.commit()
        #         self.conn.close()
        #         # self.Comment.insert(dict(item))
        #     except Exception as e:
        #         print(e)
        # elif isinstance(item, HotCommentTagItem):
        #     try:
        #         cur = self.conn.cursor()
        #         sql = '''insert into hotcomment(_id, name, productId_id, count ,type) values
        #             (%s,%s,%s,%s,%s)'''
        #         self.conn.ping(reconnect=True)
        #
        #         cur.execute(sql,(item['_id'],item['name'],item['productId'],item['count'],item['type']))
        #         cur.close()
        #         self.conn.commit()
        #         self.conn.close()
        #         # self.Comment.insert(dict(item))
        #     except Exception as e:
        #         print(e)

        elif isinstance(item, CommentItem):
            if ((item['content'] == '此用户未及时填写评价内容，系统默认评价！' ) or item['content'] == '此用户未填写评价内容'):
                pass
            elif (len(item['content']) <= 6):
                pass
            else:
                if item['score'] == 5:
                    with open('pos.txt', 'a') as f:
                        f.write(item['content']+'\n')
                elif item['score'] == 1:
                    with open('neg.txt', 'a') as f:
                        f.write(item['content']+'\n')
            # elif item['content'] == '此用户未及时填写评价内容，系统默认评价！':
            #     pass
            # else:
            # try:
            #     cur = self.conn.cursor()
            #     sql = '''insert into comment(_id, content, creationTime,days,firstCategory,
            #     imageCount,nickname,productColor,productSize,referenceId,referenceName,
            #     score,secondCategory,thirdCategory,userLevelId,userLevelName,productId_id,shop_id_id) values
            #             (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            #     self.conn.ping(reconnect=True)
            #
            #     cur.execute(sql,(item['_id'],item['content'],item['creationTime'],item['days'],item['firstCategory'],item['imageCount'],
            #                       item['nickname'],item['productColor'], item['productSize'],item['referenceId'],item['referenceName'],item['score'],
            #                       item['secondCategory'],item['thirdCategory'],item['userLevelId'],item['userLevelName'],item['productId'],item['shop_id']))
            #     cur.close()
            #     self.conn.commit()
            #     self.conn.close()
            #     # self.Comment.insert(dict(item))
            # except Exception as e:
            #     print(e)
        # elif isinstance(item, AfterCommentItem):
        #     try:
        #         cur = self.conn.cursor()
        #         sql = '''insert into aftercomment(commentid, content, product_id) VALUES (%s, %s, %s)'''
        #         self.conn.ping(reconnect=True)
        #         # cur.execute(sql, (value for value in item))
        #         cur.execute(sql, (item['commentid'], item['content'], item['product_id']))
        #         cur.close()
        #         self.conn.commit()
        #         self.conn.close()
        #     except Exception as e:
        #         print(e)
        return item

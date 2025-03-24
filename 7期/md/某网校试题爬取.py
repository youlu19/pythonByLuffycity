'''
    目标网址：https://ks.wangxiao.cn/
    需求：将首页中每一个一级类目下对应的所有二级类目下的每日一练中所有的试题
        和试题对应的选项和正确答案进行数据爬取，最后将爬取到的数据进行持久化存储。

    分析步骤：
        1. 先爬取一级类目标题和二级类目标题+详情页链接
        2.注意：想要爬取的是每一个二级类目下对应的【每日一练】板块下的内容，但是
          直接解析到的是【模拟考试】板块链接。需要将模拟考试的链接修改成每日一练的链接
          两个链接的区别如下：
          https://ks.wangxiao.cn/TestPaper/list?sign=jzs1       【模拟考试】
          https://ks.wangxiao.cn/practice/listEveryday?sign=jzs1【每日一练】
          只需要将模拟考试链接中的sign=jzs1拼接到每日一练的链接中即可。
        3.分析点击【开始做题】对应的链接：点击【开始做题】后需要进行登录。
            登录的目的是什么？为了产生对身份验证的cookie
            发现：试题数据是通过另一个数据包动态请求到的，而不是直接通过浏览器地址栏的url请求到的

        4.确定试题数据对应的数据包是哪一个？
            在抓包工具里进行全局搜索：最后发现试题数据出现在了listQuestion数据包中
            在该数据包中可以提取：
                - 请求的url
                - 请求方式
                - 请求参数：包含了两个动态变化的请求参数sign和subsign
                    变化的请求参数分析后得知是和二级类目是相关的
                    再次经过分析查证发现：这两个动态变化的请求参数出现在了点击【开始做题】
                    对应的url中。因此就可以将该url中包含的两个参数提取作用到listQuestion
                    数据包的请求中。
                - 请求头（cookie）
'''
import requests
from lxml import etree
import pandas as pd
import time
table = pd.DataFrame(columns=['一级类目','二级类目','题目','A选项','B选项','C选项','D选项','答案'])
row_index = 0 #Excel的行号
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie':'autoLogin=null; userInfo=%7B%22userName%22%3A%22pc_426029864%22%2C%22token%22%3A%22f65eaaa4-b2aa-479d-a0dd-d322fa08f533%22%2C%22headImg%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2Fz42pAjBPMUt45Q5O9xyvXlQASPKJhdO7bGraYFEyyX29KbR39GotHOddnQa5eN4Rib3foUdH3a8ibl842yK0uYLA%2F132%22%2C%22nickName%22%3A%22150****0535%22%2C%22sign%22%3A%22fangchan%22%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22cB1eRc1MclcnoVHZWhUk%2BA%3D%3D%22%2C%22passwordCookies%22%3A%22I%2FkEnX2w1ijTM59lRNF4q05CAUTGjdkx%22%7D; token=f65eaaa4-b2aa-479d-a0dd-d322fa08f533; UserCookieName=pc_426029864; OldUsername2=cB1eRc1MclcnoVHZWhUk%2BA%3D%3D; OldUsername=cB1eRc1MclcnoVHZWhUk%2BA%3D%3D; OldPassword=I%2FkEnX2w1ijTM59lRNF4q05CAUTGjdkx; UserCookieName_=pc_426029864; OldUsername2_=cB1eRc1MclcnoVHZWhUk%2BA%3D%3D; OldUsername_=cB1eRc1MclcnoVHZWhUk%2BA%3D%3D; OldPassword_=I%2FkEnX2w1ijTM59lRNF4q05CAUTGjdkx; pc_426029864_exam=fangchan'
}
#首页对应的url
main_url = 'https://ks.wangxiao.cn/'
#对首页的url进行请求发送，获取页面源码数据
page_text = requests.get(url=main_url,headers=headers).text
#数据解析：一级类目标题和二级类目标题+详情页的链接
tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@class="first-title"]/li')
for li in li_list: #该循环是用来解析所有的一级类目标题
    #解析出了一级类目的标题
    c1_title = li.xpath('./p/span/text()')[0]
    #解析二级类目标题和二级类目标题对应的链接
    a_list = li.xpath('./div/a')
    for a in a_list: #解析一级类目对应的所有二级类目标题+链接
        #二级类目对应的详情页的url链接
        c2_url = 'https://ks.wangxiao.cn'+a.xpath('./@href')[0]
        #二级类目标题
        c2_title = a.xpath('./text()')[0]
        #获取c2_url链接中的sign请求参数
        sign = c2_url.split('?')[1]
        #动态生成【每日一练】的链接
        c2_url = 'https://ks.wangxiao.cn/practice/listEveryday?'+sign
        #对每日一练的链接进行请求发送，目的是为了解析出【开始做题】的链接，将其中的
        #sign和subsign的值解析提取出来，日后作用到listQuestion中
        c2_page_text = requests.get(url=c2_url,headers=headers).text
        time.sleep(2)
        #解析开始做题的链接
        c2_tree = etree.HTML(c2_page_text)
        #获取了所有开始做题的链接
        start_test_list = c2_tree.xpath('//div[@class="test-panel"]/div/ul/li[4]/a/@href')
        if start_test_list:
            #经过测试发现指定的二级类目页面下所有的开始做题链接中的sign和subsign的值都是一样
                #因此只需要任意将其中的一个开始做题链接中的sign和subsign的值提取即可
            start_test_url = start_test_list[0] #某一个开始做题的链接
            ret = start_test_url.split('?')[1].split('&')
            sign = ret[1]
            subsign = ret[2]
            #至此，动态获取了sign和subsign的值，接下来就可以使用这两个动态的参数值作用到
                #listQuestion数据包中提取考试的试题数据了
            #捕获试题数据：分析后发现试题数据是存在listQuestion数据包中
            post_url = 'https://ks.wangxiao.cn/practice/listQuestions'
            data = {
                "practiceType": "1",
                "sign": sign,
                "subsign": subsign,
                "day": "20240704"
            }
            response_ret = requests.post(url=post_url,headers=headers,json=data).json()
            time.sleep(2)
            #解析出所有试题信息对应的列表
            question_list = response_ret['Data'][0]['questions']
            for item in question_list:
                question = item['content'] #题目
                options_list = [] #四个选项的内容
                right_anser_list = [] #四个选项对应的答案
                for option in item['options']: #item['options']是四个选项
                    option_choose = option['content']
                    options_list.append(option_choose)
                    anser = option['isRight']
                    right_anser_list.append(anser)
                #将将四个选项和ABCD结合一下，组成4个字符串
                A = 'A.'+ str(options_list[0])
                B = 'B.' + str(options_list[1])
                C = 'C.' + str(options_list[2])
                D = 'D.' + str(options_list[3])
                #index(1)找到列表元素为1的下标是多少
                anser_index = right_anser_list.index(1)
                dic = {
                    0:'A',
                    1:'B',
                    2:'C',
                    3:'D'
                }
                #获取了正确选项
                anser = dic[anser_index]
                #批量向数据表格中进行行数据的插入
                table.loc[row_index] = [c1_title,c2_title,question,A,B,C,D,anser]
                row_index += 1
            break
        break
table.to_excel('data.xlsx',index=None)
'''
    python语法回顾：4期
    自动化框架selenium、Playwright：5期
    scrapy框架&异步爬虫：3，4期
    mysql数据库：6期
    1期python语法
'''



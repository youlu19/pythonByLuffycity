## 爬虫初始

### 爬虫相关介绍

- 什么是爬虫
  - 就是通过编写程序，“模拟”浏览器上网，然后让其在互联网中“抓取”数据的过程。
    - 模拟：浏览器本身就是一个纯天然的爬虫工具。爬虫相关的操作都是模拟/基于浏览器为基础开发实现出来的。
    - 抓取：
      - 一种是抓取一张页面中所有的数据
      - 一种是抓取页面中局部的数据

  - 提问：如果日后你的爬虫程序没有爬取到你想要的数据，why？
    - **你的程序模拟浏览器的力度不够！**
- 爬虫在应用场景的分类
  - 通用爬虫：将一整张页面源码数据进行爬取。
  - 聚焦爬虫：将一张页面中局部/指定的数据进行抓取。建立在通用爬虫的基础上。
- 爬虫的矛与盾（重点）
  - 反爬机制：对应门户网站，网站可以指定相关的机制阻止爬虫对其网站数据的采集
  - 反反爬策略：对应爬虫程序，爬虫可以制定相关的策略将网站的反爬机制破解，从而爬取到指定的数据

### requests基础操作

- 基本介绍
  - requests是一个基于网络请求的模块。可以使用程序模拟浏览器上网。

- 环境安装
  - pip install requests

- 编码流程
  - 指定url（输入一个网址）
  - 发起请求（按下回车）
  - 获取响应数据（请求到的数据）
  - 持久化存储


### 案例应用

#### 东方财富首页数据爬取

- https://www.eastmoney.com/

- ```python
  import requests
  
  #1.指定url
  main_url = 'https://www.eastmoney.com/'
  
  #2.发起请求:
  #get函数可以根据指定的url发起网络请求
  #get函数会返回一个响应对象:
  response = requests.get(url=main_url)
  
  #3.获取响应数据
  page_text = response.text #text是可以返回字符串形式的响应数据/爬取到的数据
  
  #4.持久化存储
  with open('dongfang.html','w') as fp:
      fp.write(page_text)
  ```

​     发现：爬取的页面数据出现了中文乱码。

#### 中文乱码解决

- ```python
  import requests
  
  #1.指定url
  main_url = 'https://www.eastmoney.com/'
  
  #2.发起请求:
  #get函数可以根据指定的url发起网络请求
  #get函数会返回一个响应对象:
  response = requests.get(url=main_url)
  
  #设置响应对象的编码格式(处理中文乱码)
  response.encoding = 'utf-8'
  
  #3.获取响应数据
  page_text = response.text #text是可以返回字符串形式的响应数据/爬取到的数据
  
  #4.持久化存储
  with open('dongfang.html','w') as fp:
      fp.write(page_text)
  
  ```

#### 爬取51游戏中任何游戏对应的搜索结果页面数据

- url：https://www.51.com/

- ```python
  import requests
  
  #1.指定url
  game_title = input('enter a game name:')
  params = { #字典是用于封装请求参数
      'q':game_title
  }
  url = 'https://game.51.com/search/action/game/'
  
  #2.发起请求
      #get是基于指定的url和携带了固定的请求参数进行请求发送
  response = requests.get(url=url,params=params)
  
  #3.获取响应数据
  page_text = response.text #text表示获取字符串形式的响应数据
  # print(page_text)
  
  #4.持久化存储
  fileName = game_title + '.html'
  with open(fileName,'w') as fp:
      fp.write(page_text)
  ```

#### 中国人事考试网

- url：http://www.cpta.com.cn/

  - 爬虫模拟浏览器主要是模拟请求参数和主要的请求头。
    - User-Agent:请求载体的身份标识。
      - 使用浏览器发请求，则请求载体就是浏览器
      - 使用爬虫程序发请求，则请求载体就是爬虫程序
  - 反爬机制：UA检测
    - 网站后台会检测请求的载体是不是浏览器，如果是则返回正常数据，不是则返回错误数据。
  - 反反爬机制：UA伪装
    - 将爬虫发起请求的User-Agent伪装成浏览器的身份。

- ```python
  import requests
  
  url = 'http://www.cpta.com.cn/'
  
  #User-Agent:请求载体（浏览器，爬虫程序）的身份表示
  header = {
      'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
  }
  #伪装了浏览器的请求头
  response = requests.get(url=url,headers=header)
  
  page_text = response.text
  
  with open('kaoshi.html','w') as fp:
      fp.write(page_text)
  
  #程序模拟浏览器的力度不够
  ```

#### 中国人事考试网---站内搜索

- ```python
  import requests
  url = 'http://www.cpta.com.cn/category/search'
  param = {
      "keywords": "人力资源",
      "搜 索": "搜 索"
  }
  header = {
      'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
  }
  #发起了post请求：通过data参数携带了请求参数
  response = requests.post(url=url,data=param,headers=header)
  
  page_text = response.text
  
  with open('renshi.html','w') as fp:
      fp.write(page_text)
  
  #通过抓包工具定位了指定的数据包：
      #提取：url，请求方式，请求参数，请求头信息
  ```

  

#### 智慧职教（动态加载数据爬取）**(重点)**

- 抓取智慧职教官网中的【专业群板块下】的所有数据

  - url : https://www.icve.com.cn/portal_new/course/course.html

- 测试：直接使用浏览器地址栏中的url，进行请求发送查看是否可以爬取到数据？

  - 不用写程序，基于抓包工具测试观察即可。

- 经过测试发现，我们爬取到的数据并没有包含详情数据，why？

- 动态加载数据：

  - 在一个网页中看到的数据，并不一定是通过浏览器地址栏中的url发起请求请求到的。如果请求不到，一定是基于其他的请求请求到的数据。
  - 动态加载数据值的就是：
    - 不是直接通过浏览器地址栏的url请求到的数据，这些数据叫做动态加载数据。
  - 如何获取动态加载数据？
    - 确定动态加载的数据是基于哪一个数据包请求到的？
    - 数据包数据的全局搜索：
      - 点击抓包工具中任何一个数据包
      - control+f进行全局搜索（弹出全局搜索框）
        - 目的：定位动态加载数据是在哪一个数据包中
      - 定位到动态加载数据对应的数据包，模拟该数据包进行请求发送即可：
        - 从数据包中提取出：
          - url
          - 请求参数   

  注意：请求头中需要携带Referer。（体现模拟浏览器的力度）

- ```python
  import requests
  import time
  fp = open('data.txt','w')
  for page in range(1,6):
      time.sleep(1)
      url = 'https://www.icve.com.cn/portal/course/getNewCourseInfo?page='+str(page)
      headers = {
          'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
          'Referer':'https://www.icve.com.cn/portal_new/course/course.html'
      }
      dic = {
          "order": "",
          "kczy": "",
          "keyvalue": "",
          "printstate": ""
      }
      response = requests.post(url=url,headers=headers,data=dic)
      dic = response.json()
      for item_dic in dic['list']:
          course_title = item_dic['Title']
          teacher_name = item_dic['TeacherDisplayname']
          school_title = item_dic['UnitName']
          print(course_title,teacher_name,school_title)
          fp.write(course_title+'-'+teacher_name+'-'+school_title+'\n')
  
  fp.close()
  ```


#### 图片数据爬取

- ```python
  #方式1：
  import requests
  url = 'https://img0.baidu.com/it/u=540025525,3089532369&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500'
  response = requests.get(url=url)
  #content获取二进制形式的响应数据
  img_data = response.content
  with open('1.jpg','wb') as fp:
      fp.write(img_data)
  ```

- ```python
  #方式2
  from urllib.request import urlretrieve
  #图片地址
  img_url = 'https://img0.baidu.com/it/u=4271728134,3217174685&fm=253&fmt=auto&app=138&f=JPEG?w=400&h=500'
  #参数1：图片地址
  #参数2：图片存储路径
  #urlretrieve可以根据图片地址将图片数据请求到直接存储到参数2表示的图片存储路径中
  urlretrieve(img_url,'1.jpg')
  ```
  
- 爬取图片的时候需要做UA伪装使用方式1，否则使用方式2




### 作业

#### 肯德基（POST请求、动态加载数据、UA检测）

- http://www.kfc.com.cn/kfccda/storelist/index.aspx

  - 将餐厅的位置信息进行数据爬取


    - 爬取多页数据

#### 小试牛刀：

- url：https://www.xiachufang.com/
- 实现爬取下厨房网站中任意菜谱搜索结果数据爬取










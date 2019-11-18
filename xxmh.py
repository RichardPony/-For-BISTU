# import json
# import requests
# from bs4 import BeautifulSoup
# import Img
# from urllib import request
# from urllib import error
# from urllib import parse
# from http import cookiejar
#
# login_head = '''Accept:text/html, */*; q=0.01
# Origin:http://info.bistu.edu.cn
# X-DevTools-Emulate-Network-Conditions-Client-Id:d60c23d8-a98a-44b0-b690-3e27d2fe33f1
# X-Requested-With:XMLHttpRequest
# User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36
# Content-Type:application/x-www-form-urlencoded; charset=UTF-8
# Referer:http://info.bistu.edu.cn/
# Accept-Encoding:gzip, deflate
# Accept-Language:zh-CN,zh;q=0.9'''
#
# def getHeaders(raw_head):
#     headers = {}
#     for raw in raw_head.split('\n'):
#         headerkey, headerValue = raw.split(':', 1)
#         headers[headerkey] = headerValue
#     return headers
# header = getHeaders(login_head)
#
# s = requests.session()
# page_url = 'http://info.bistu.edu.cn'
# login_url = 'http://info.bistu.edu.cn/syt/login/Login.htm'
# card_url = 'http://192.168.240.58:8088/WebQueryUI/card/selfTrade.html'
# formtable = {
#     'password':'',
#     'username':'',
#     'verification':''
# }
#
# formtable['password'] = '791579'
# formtable['username'] = '2017011398'
#
# login_page = s.get(page_url)
# soup = BeautifulSoup(login_page.text,'lxml')
#
# pic_url = soup.find('img',attrs={'id':'code'}).get('src')
# pic = requests.get(pic_url).content
# with open('xxmh.png', 'wb') as f:
#     f.write(pic)
#
# code = Img.ImgToText('xxmh.png')
# print(code)
# formtable['verification'] = code
# # logingpostdata = parse.urlencode(formtable).encode('utf-8')
# #
# # #声明一个CookieJar对象实例来保存cookie
# # cookie = cookiejar.CookieJar()
# # #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
# # cookie_support = request.HTTPCookieProcessor(cookie)
# # #通过CookieHandler创建opener
# # opener = request.build_opener(cookie_support)
# # #创建Request对象
# # req1 = request.Request(url=login_url, data=logingpostdata, headers=header)
#
# res = s.post(login_url,formtable,headers=header)
# print(res)
#
# page = s.get('http://info.bistu.edu.cn/user/index.htm')
# print(page.text)
#
#
# page = s.get("http://info.bistu.edu.cn:80//syt/home/grxx.htm?action=grxx&amp;_t=971623&amp;_winid=w6832" )
#
# #   http://info.bistu.edu.cn/syt/appletLink/querylist.htm?id=4028ee816488419a0164887d32ee0000
# page = s.get("http://info.bistu.edu.cn/syt/appletLink/index.htm?id=4028ee816488419a0164887d32ee0000&_t=996948&_winid=w6579")
# # page = s.get(" http://info.bistu.edu.cn/syt/appletLink/querylist.htm?id=4028ee816488419a0164887d32ee0000")
# # page = s.get("http://info.bistu.edu.cn:80/core/boot.js")
# print(page.text)

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import Img
from PIL import Image
#获取的数据转为二维数组，并去重
def str_toList(str):
    list1 = str.split("\n")
    del list1[0]
    for i in range(11):
        list1.pop()
    print(list1)
    for i in range(len(list1)):
        list1[i] = list1[i].split()
    list2 = list(set([tuple(t) for t in list1]))
    list3 = list([list(t) for t in list2])
    # print(list3)
    return list3
#通过执行JS进行查询，并获得数据
def Query():
    data=[]
    for i in range(1,11):
        driver.execute_script("querySelfTrade("+ str(i) +",false);")
        tr = driver.find_element_by_xpath("//table[@id='gird']/tbody").text
        list = str_toList(tr)
        data = data + list
    print(data)
    return data
#设置浏览器的位置和保存验证码的位置
chromedriver = "D:\常用程序\Google\Chrome\Application\chromedriver"
screenImg = 'D:\数据采集\JwcCrawl\XXMH\code.png'
#打开浏览器
driver = webdriver.Chrome(chromedriver)
#打开网站
login_url = 'https://info.bistu.edu.cn/'
driver.get(login_url)

#填入用户名和密码
time.sleep(2)
user = driver.find_element_by_id("username")
user.send_keys("2017011398")
driver.find_element_by_id("password").send_keys("mcy200091")

#保存浏览器截图，并截取验证码图片
driver.get_screenshot_as_file(screenImg)
location = driver.find_element_by_id('code').location
size = driver.find_element_by_id('code').size
left = location['x'] + 190
top =  location['y'] + 85
right = left + size['width'] + 30
bottom = top + size['height'] + 20
img = Image.open(screenImg).crop((left,top,right,bottom))
img.save(screenImg)
#填入验证码
code =  Img.ImgToText('XXMH/code.png')
driver.find_element_by_id("verification").send_keys(code)

# code = driver.find_element_by_id("code")
# pic_url = str(code.get_attribute("src"))
# print(pic_url)
#点击登录
driver.find_element_by_xpath("//button").click()

#进入一卡通的iframe
# time.sleep(5)
# driver.switch_to.frame(0)
# driver.switch_to.frame(2)
#进入一卡通查询页面
time.sleep(2)
driver.get("https://info.bistu.edu.cn/sytsso/other.htm?appId=DKYKT&uuid=ff8080816651b0ea016657b4abd50002")
time.sleep(1)
driver.find_element_by_xpath("//li[@id='label77']/span[3]/a").click()
# #通过执行JS进行查询
# driver.execute_script("querySelfTrade(1,false);")
# #获得数据表格
# tr = driver.find_element_by_xpath("//table[@id='gird']/tbody").text
Query()

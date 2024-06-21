import requests
import json
import m_constant
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

loginUrl = 'http://zhjw.scu.edu.cn/login'
bookUrl = 'http://zhjw.scu.edu.cn/student/courseSelect/books/dealBooks/queryList/0'
cookies = m_constant.cookies
headers = m_constant.headers
token = ''

# 获取token
autoLogin = str(input("1.手动登陆获取token 2.粘贴浏览器的token："))
if autoLogin == '1':
    drivers = webdriver.Edge()
    drivers.get(loginUrl)
    WebDriverWait(drivers, 120, 0.5).until(lambda
                                               driver: driver.current_url == "http://zhjw.scu.edu.cn/index" or driver.current_url == "http://zhjw.scu.edu.cn/",
                                           "Please check your Internet and rerun the program!")
    token = drivers.get_cookies()[0]['value']
    cookies['student.urpSoft.cn'] = token
elif autoLogin == '2':
    token = str(input("请输入token(前面不要有空格):\n"))
    cookies['student.urpSoft.cn'] = token

# 获取当前教材信息
response = requests.post(url=bookUrl, cookies=cookies, headers=headers, verify=False)
bookList = json.loads(response.text)
# 拼接退教材字符串
postData = 'tokenValue=' + token + '&param='
for book in bookList:
    postData += book[-3] + ',' + book[-2] + ',' + book[-1] + ',0' + '|'

postData = postData[:-1]
# 发生请求退订所有教材
response = requests.post(
    'http://zhjw.scu.edu.cn/student/courseSelect/books/dealBooks/saveJc',
    cookies=cookies,
    headers=headers,
    data=postData,
    verify=False,
)
# 打印返回结果
print(response.text)
# 再次获取教材信息
response = requests.post(url=bookUrl, cookies=cookies, headers=headers, verify=False)
bookList = json.loads(response.text)
for book in bookList:
    print(book)

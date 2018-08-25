import requests
import re
from bs4 import BeautifulSoup
import os
# 全局session
rq = requests.Session()
# 文章id
cartoon_id = None



# 登录
def login(username, password, cartoonUrl):
    pattern = re.compile(r'[a-z 0-9]{32}')
    id = pattern.search(cartoonUrl)
    if id:
        global cartoon_id
        cartoon_id = id.group(0)
        print('获取到的id为:'+cartoon_id)
        payload = {'name': username, 'password': password}
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                   'Host': 'www.weehui.com', 'Origin': 'http://www.weehui.com', 'Referer': 'http://www.weehui.com/login/login'}
        rq.post('http://www.weehui.com/login/login',
                    data=payload, headers=headers)
        global cartoonStartIndex
        get(cartoonStartIndex)
    else:
        print('no match')


def get(index):
    print("正在下载第"+str(index)+'章内容..')
    global cartoon_id
    url = 'http://www.weehui.com/cartoon/read/' + \
        cartoon_id+'/'+str(index)
    r = rq.get(url)
    print(r)
    soup = BeautifulSoup(r.text, 'html5lib')
    # print(soup.prettify())
    div = soup.findAll('div', attrs={"class": 'contentNovel'})[0]
    # print(div)
    soup = BeautifulSoup(str(div), 'html5lib')
    i = 0
    for src in soup.findAll("img"):
        data_original = src.get('data-original')
        if(data_original == None):
            data_original = src.get('src')
        print(data_original)
        i = i + 1
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                   'Referer': url}
        ir = requests.get(data_original, headers=headers)
        global save_url
        if ir.status_code == 200:
            open(save_url +
                 str(index)+"_"+str(i)+".jpg", 'wb').write(ir.content)

    index = index+1
    global cartoonEndIndex
    if(index < cartoonEndIndex):
        get(index)

# 用户名
username = input('漫小说用户名:')
# 密码
password = input('漫小说密码:')
# 漫画链接地址
cartoonUrl = input('漫画链接地址:')
# 漫画总章数
cartoonPagesNum = input('漫画总章数(比如一共有57话,那么输入57)):')
# 漫画存放的地址 "/Users/hdy/Desktop/pic/"
save_url = input('漫画存放地址(必须为文件夹):')
# 第几话开始下载
cartoonStartIndex = input('从第几话开始?如果不输入默认为1:')
if(cartoonStartIndex):
    cartoonStartIndex = int(cartoonStartIndex)
else:
    cartoonStartIndex = 1

# 第几话结束
cartoonEndIndex = input('从第几话结束?如果不输入默认为到底:')
if(cartoonEndIndex):
    cartoonEndIndex = int(cartoonEndIndex)
else:
    cartoonEndIndex = int(cartoonPagesNum)

# 开始下载
login(username, password, cartoonUrl)
